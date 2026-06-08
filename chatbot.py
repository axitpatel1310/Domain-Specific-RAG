from pathlib import Path
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama


ELASTIC_URL = "http://localhost:9200"
es = Elasticsearch(ELASTIC_URL)
SUMMARY_INDEX = "learning_summaries"
VECTOR_DB = "vectorstore"
MEMORY_DIR = "conversations"

Path(MEMORY_DIR).mkdir(exist_ok=True)

TONES = {
    "1": {
        "name": "Professional",
        "prompt": """
Provide concise and direct answers.
Focus on accuracy.
Avoid unnecessary explanations.
"""
    },
    "2": {
        "name": "Friendly",
        "prompt": """
Be conversational and engaging.
Use simple language.
Keep answers approachable.
"""
    },
    "3": {
        "name": "Teacher",
        "prompt": """
Explain concepts step-by-step.
Use examples and analogies.
Prioritize learning and understanding.
"""
    }
}

# ----------------------------------
# Profile
# ----------------------------------

profile_id = input("Enter profile name: ").strip()

memory_file = Path(MEMORY_DIR) / f"{profile_id}.json"

if memory_file.exists():

    with open(memory_file, "r", encoding="utf-8") as f:
        memory_data = json.load(f)

    print(
        f"\nLoaded "
        f"{len(memory_data['messages'])} "
        f"previous messages for '{profile_id}'"
    )

else:

    memory_data = {
        "tone": "1",
        "messages": []
    }

    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(
            memory_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nCreated new profile '{profile_id}'")

chat_history = memory_data["messages"]
current_tone = memory_data["tone"]

# ----------------------------------
# Embeddings
# ----------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma(
    persist_directory=VECTOR_DB,
    embedding_function=embeddings
)

retriever = db.as_retriever(
    search_kwargs={"k": 4}
)

# ----------------------------------
# LLM
# ----------------------------------

llm = ChatOllama(
    model="llama3.1:8b"
)

def generate_learning_summary(messages):

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in messages
    )

    prompt = f"""
You are an educational learning analyst.

Analyze this conversation.

Return JSON only.

Required format:

{{
  "summary": "...",
  "learned_topics": [],
  "struggling_topics": [],
  "learning_stage": ""
}}

Conversation:

{conversation_text}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)

    except Exception:
        return None

def save_learning_summary(profile_id, summary_data):

    doc = {
        "user_id": profile_id,
        "date": datetime.now().isoformat(),
        **summary_data
    }

    es.index(
        index=SUMMARY_INDEX,
        document=doc
    )

def get_learning_summaries(profile_id):

    query = {
        "query": {
            "term": {
                "user_id": profile_id
            }
        },
        "size": 5,
        "sort": [
            {
                "date": {
                    "order": "desc"
                }
            }
        ]
    }

    result = es.search(
        index=SUMMARY_INDEX,
        body=query
    )

    summaries = []

    for hit in result["hits"]["hits"]:

        source = hit["_source"]

        summaries.append(
            source["summary"]
        )

    return "\n".join(summaries)

print("\nRAG Chatbot Ready")
print(f"Current Tone: {TONES[current_tone]['name']}")
print("Type 'Change-Tone' to change tone")
print("Type 'exit' to quit\n")

# ----------------------------------
# Chat Loop
# ----------------------------------

while True:

    question = input("You: ").strip()

    # ------------------------------
    # Exit
    # ------------------------------

    if question.lower() == "exit":
        break

    # ------------------------------
    # Change Tone
    # ------------------------------

    if question.lower() == "change-tone":

        print("\nSelect Tone")
        print("1. Professional")
        print("2. Friendly")
        print("3. Teacher")

        choice = input("\nChoice: ").strip()

        if choice in TONES:

            current_tone = choice
            memory_data["tone"] = choice

            with open(
                memory_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    memory_data,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                f"\nTone changed to "
                f"{TONES[choice]['name']}\n"
            )
        else:
            print("\nInvalid option\n")
        continue

# ----------------------------------
# Retrieve PDF Context
# ----------------------------------

    RELEVANCE_THRESHOLD = 0.55

    results = db.similarity_search_with_relevance_scores(
        question,
        k=4
    )

    docs = []
    sources = set()
    context_parts = []

    for doc, score in results:

        if score >= RELEVANCE_THRESHOLD:

            docs.append(doc)
            context_parts.append(doc.page_content)

            if "source" in doc.metadata:
                sources.add(doc.metadata["source"])
    context = "\n\n".join(context_parts)
    has_docs = len(docs) > 0
    
    # -------------
    # -----------------
    # Recent Conversation History
    # ------------------------------
    recent_history = chat_history[-10:]
    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in recent_history
    )
    has_docs = len(docs) > 0
    has_history = len(recent_history) > 0
    if has_docs:
        document_instruction = """
        Relevant document context was found.
        Use it when answering.
        """
    else:
        document_instruction = """
        No relevant document context was found.
        Answer normally using your own knowledge.
        Do not mention documents.
        """
    
    # ------------------------------
    # Prompt
    # ------------------------------
    tone_prompt = TONES[current_tone]["prompt"]
    memory_keywords = [
    "remember",
    "earlier",
    "before",
    "previous",
    "last time",
    "we discussed",
    "you said"
]

    using_memory = any(
        keyword in question.lower()
        for keyword in memory_keywords
    )
    try:
        learning_memory = get_learning_summaries(profile_id)
    except Exception:
        learning_memory = ""
    prompt = f"""
    You are a helpful assistant.
    {tone_prompt} 
    {document_instruction}
    
    Learning Profile: {learning_memory}

    Conversation History: {history_text}

    Document Context: {context}

    User Question: {question}

Answer:
"""    

# ------------------------------
# LLM Response
# ------------------------------
    response = llm.invoke(prompt)
    answer = response.content
    citation_lines = []

    if sources:
        citation_lines.append("\n\nSources:")
        for source in sorted(sources):
            citation_lines.append(f"- {source}")
        answer += "\n".join(citation_lines)

    if using_memory:
        answer += "\n\nSources:\n- Conversation History"

    elif has_docs and sources:
        answer += "\n\nSources:\n"
        for source in sorted(sources):
            answer += f"- {source}\n"
                    
    print("\nBot:")
    print(answer)
    print()

    # ------------------------------
    # Save Memory
    # ------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    memory_data["messages"].append(
        {
            "role": "user",
            "content": question,
            "timestamp": timestamp
        }
    )

    memory_data["messages"].append(
        {
            "role": "assistant",
            "content": answer,
            "timestamp": timestamp
        }
    )
    message_count = len(memory_data["messages"])
    if message_count % 20 == 0:
        recent_messages = memory_data["messages"][-20:]

        summary = generate_learning_summary(
        recent_messages
    )

        if summary:
            save_learning_summary(
            profile_id,
            summary
        )

            print(
                "\n[Learning Summary Saved]"
            )
    chat_history = memory_data["messages"]

    with open(
        memory_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory_data,
            f,
            indent=4,
            ensure_ascii=False
        )

print("\nGoodbye!")