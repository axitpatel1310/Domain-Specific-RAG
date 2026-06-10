from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama

ELASTIC_URL = "http://localhost:9200"
VECTOR_DB = "vectorstore"
MEMORY_DIR = "conversations"

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

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

llm = ChatOllama(
    model="llama3.1:8b"
)