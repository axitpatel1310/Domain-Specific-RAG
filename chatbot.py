from pathlib import Path
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from langchain_community.vectorstores import Chroma
from config import TONES, llm, ELASTIC_URL, MEMORY_DIR,VECTOR_DB, embeddings
from datetime import datetime
from memory import (
    current_tone,
    chat_history,
    profile_id,
    memory_file,
    memory_data
)
from vectorstore import retrieve_documents,db
from learning import (
    generate_learning_summary,
    save_learning_summary,
    get_learning_summaries
)

es = Elasticsearch(ELASTIC_URL)
SUMMARY_INDEX = "learning_summaries"
Path(MEMORY_DIR).mkdir(exist_ok=True)

print("\nRAG Chatbot Ready")
print(f"Current Tone: {TONES[current_tone]['name']}")
print("Type 'Change-Tone' to change tone")
print("Type 'exit' to quit\n")

while True:
    question = input("You: ").strip()
    if question.lower() == "exit":
        break

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