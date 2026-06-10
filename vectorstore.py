from langchain_community.vectorstores import Chroma

from config import (
    VECTOR_DB,
    embeddings
)

db = Chroma(
    persist_directory=VECTOR_DB,
    embedding_function=embeddings
)

def retrieve_documents(
    question,
    threshold=0.55
):

    results = db.similarity_search_with_relevance_scores(
        question,
        k=4
    )

    docs = []
    sources = set()

    for doc, score in results:

        if score >= threshold:

            docs.append(doc)

            if "source" in doc.metadata:
                sources.add(
                    doc.metadata["source"]
                )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return docs, context, sources