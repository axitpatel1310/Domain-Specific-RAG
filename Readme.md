# Educational RAG Chatbot for Personalized Learning

## Overview

This project is an AI-powered Educational Retrieval-Augmented Generation (RAG) chatbot designed to help learners study technical subjects such as Machine Learning, Deep Learning, Artificial Intelligence, and Large Language Models.

Unlike a traditional chatbot, this system combines:

* Document-based knowledge retrieval
* Conversational memory
* Personalized learning support
* User learning analytics
* Future recommendation systems

The long-term goal is to build an intelligent learning companion capable of understanding what a learner knows, what they struggle with, and what they should learn next.

---

## Current Features

### 1. Document Ingestion

The system can ingest educational resources such as:

* PDF files
* Research papers
* Text documents

Documents are processed, chunked, embedded, and stored inside a vector database for semantic retrieval.

---

### 2. Retrieval-Augmented Generation (RAG)

When a user asks a question:

1. Relevant document chunks are retrieved.
2. Context is sent to the LLM.
3. The model generates an answer grounded in the uploaded learning material.

This reduces hallucinations and improves factual accuracy.

---

### 3. Conversational Memory

The chatbot stores user conversations locally.

This allows the assistant to:

* Remember previous discussions
* Maintain context across sessions
* Personalize future interactions

---

### 4. User Profiles

Each user has a dedicated conversation history.

The chatbot can use this information to:

* Track learning progress
* Understand recurring interests
* Provide more personalized responses

---

## Tech Stack

### Language

* Python

### LLM

* Ollama
* Llama Models

### Embeddings

* Ollama Embeddings

### Vector Database

* ChromaDB

### Frameworks

* LangChain

### Storage

* Local JSON Memory
* Chroma Vector Store

---

## Project Structure

```text
project/
│
├── chatbot.py
├── ingest.py
├── vectorstore/
├── data/
├── conversations/
│
├── README.md
│
└── requirements.txt
```

### Folder Description

| Folder         | Purpose                            |
| -------------- | ---------------------------------- |
| data/          | Source PDFs and learning materials |
| vectorstore/   | Chroma vector database             |
| conversations/ | User conversation history          |
| ingest.py      | Document ingestion pipeline        |
| chatbot.py     | Main chatbot application           |

---

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>

cd project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ollama

```bash
ollama serve
```

Pull the required models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 4. Ingest Documents

Place PDFs inside:

```text
data/
```

Run:

```bash
python ingest.py
```

### 5. Start Chatbot

```bash
python chatbot.py
```

---

## Example Questions

```text
What is gradient descent?

Explain the attention mechanism.

What are the limitations of RNNs?

Compare CNNs and Vision Transformers.

Summarize the chapter I uploaded.
```

---

## Roadmap

### Phase 1 — Core RAG System ✅

* [x] Document ingestion
* [x] Vector database
* [x] Retrieval pipeline
* [x] Conversational memory

---

### Phase 2 — Conversational Summaries 🚧

Goal:

Compress long conversation histories into learning summaries.

Example:

```text
User learned:
- Neural Networks
- Backpropagation
- Attention Mechanisms

User struggles with:
- Vanishing gradients
- Sequence modeling
```

Benefits:

* Better long-term memory
* Reduced token usage
* Improved personalization

---

### Phase 3 — Learning Analytics Dashboard 📋

Goal:

Create a learner profile that tracks:

* Topics studied
* Learning depth
* Knowledge progression
* Areas requiring revision

Example:

```text
Machine Learning: 80%
Deep Learning: 55%
Transformers: 40%
LLMs: 25%
```

---

### Phase 4 — Learning Path Recommendations 📋

Goal:

Recommend what the learner should study next.

Examples:

```text
You have mastered RNNs.

Suggested next topic:
→ Attention Mechanisms

You understand Transformers.

Suggested next topic:
→ Retrieval-Augmented Generation
```

---

### Phase 5 — Intelligent Educational Assistant 📋

Future vision:

An AI tutor that can:

* Remember long-term learning history
* Track knowledge growth
* Recommend study plans
* Generate quizzes
* Identify knowledge gaps
* Act as a personalized AI mentor

---

## Research Objective

This project investigates how Retrieval-Augmented Generation, conversational memory, and learning analytics can be combined to create more personalized educational AI systems.

The aim is to move beyond simple question-answering and towards adaptive AI tutoring systems that support long-term learning.

---

## Author

Axit Patel
MSc Final Year Project
Educational AI & Retrieval-Augmented Generation Systems
