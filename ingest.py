from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

PDF_DIR = "data"
VECTOR_DB = "vectorstore"

# Docker Ollama endpoint
OLLAMA_URL = "http://localhost:11434"

# -----------------------------
# Load PDFs
# -----------------------------

documents = []

for pdf_file in Path(PDF_DIR).glob("*.pdf"):
    print(f"Loading {pdf_file}")

    loader = PyPDFLoader(str(pdf_file))
    docs = loader.load()

    # Add source metadata
    for doc in docs:
        doc.metadata["source"] = pdf_file.name

    documents.extend(docs)

print(f"\nLoaded {len(documents)} pages")

# -----------------------------
# Chunk Documents
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# -----------------------------
# Embedding Model
# -----------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=OLLAMA_URL
)

# -----------------------------
# Batch Insert Into Chroma
# -----------------------------

BATCH_SIZE = 50

vectorstore = None

for i in range(0, len(chunks), BATCH_SIZE):

    batch = chunks[i:i + BATCH_SIZE]

    batch_num = (i // BATCH_SIZE) + 1
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

    print(
        f"Embedding batch {batch_num}/{total_batches} "
        f"({len(batch)} chunks)"
    )

    try:

        if vectorstore is None:

            vectorstore = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=VECTOR_DB
            )

        else:

            vectorstore.add_documents(batch)

    except Exception as e:

        print(f"\nFAILED ON BATCH {batch_num}")
        print(e)
        raise

print("\nSaving Vector Store...")

vectorstore.persist()

print("Done!")
print(
    f"Stored {vectorstore._collection.count()} embeddings"
)