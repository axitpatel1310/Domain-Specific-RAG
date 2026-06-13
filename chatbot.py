from pathlib import Path
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from langchain_community.vectorstores import Chroma
from config import TONES, llm, ELASTIC_URL, MEMORY_DIR,VECTOR_DB, embeddings
from datetime import datetime
from memory import (
    load_profile,
    save_profile
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
print("Type 'Change-Tone' to change tone")
print("Type 'exit' to quit\n")

def ask_question(profile_id, question):
    global chat_history
    global memory_data
    global current_tone
    
    memory_file, memory_data = (load_profile(profile_id))
    chat_history = memory_data["messages"]
    current_tone = memory_data["tone"]
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
            context_parts.append(
                doc.page_content
            )

            if "source" in doc.metadata:
                sources.add(
                    doc.metadata["source"]
                )

    context = "\n\n".join(
        context_parts
    )

    recent_history = chat_history[-10:]

    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in recent_history
    )

    if docs:

        document_instruction = """
        Relevant document context was found.
        Use it when answering.
        """

    else:

        document_instruction = """
        No relevant document context was found.
        Answer normally using your own knowledge.
        """

    tone_prompt = TONES[current_tone]["prompt"]

    try:
        learning_memory = (
            get_learning_summaries(
                profile_id
            )
        )

    except Exception:

        learning_memory = ""

    prompt = f"""
You are a helpful assistant.

{tone_prompt}

{document_instruction}

Learning Profile:
{learning_memory}

Conversation History:
{history_text}

Document Context:
{context}

User Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content

    if sources:

        answer += "\n\nSources:\n"

        for source in sorted(sources):

            answer += f"- {source}\n"

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

    if len(memory_data["messages"]) % 20 == 0:

        recent_messages = (
            memory_data["messages"][-20:]
        )

        summary = (
            generate_learning_summary(
                recent_messages
            )
        )

        if summary:

            save_learning_summary(
                profile_id,
                summary
            )
    save_profile(memory_file, memory_data)
    chat_history = memory_data["messages"]
    return answer