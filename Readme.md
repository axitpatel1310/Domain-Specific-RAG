# DS-RAG: Educational Retrieval-Augmented Generation System

## Overview

DS-RAG is an AI-powered Educational Retrieval-Augmented Generation (RAG) system designed to provide personalized learning experiences for students studying technical subjects such as:

* Machine Learning
* Deep Learning
* Artificial Intelligence
* Large Language Models
* Data Science
* Software Engineering

Unlike traditional chatbots that simply answer questions, DS-RAG aims to become an intelligent educational assistant capable of:

* Understanding learning materials
* Remembering previous conversations
* Tracking learning progress
* Generating personalized insights
* Recommending future study topics

This project is being developed as an MSc Final Year Project exploring how Retrieval-Augmented Generation, conversational memory, and learning analytics can be combined to create adaptive educational AI systems.

---

# Features

## 1. User Authentication

The platform supports user registration and login.

Features:

* User registration
* User login
* Session management
* Individual learning profiles

Each learner has a dedicated account and personalized learning history.

---

## 2. Document Ingestion Pipeline

The system can ingest educational resources such as:

* PDF textbooks
* Research papers
* Lecture notes
* Technical documentation

The ingestion pipeline:

1. Loads documents
2. Splits content into chunks
3. Generates embeddings
4. Stores embeddings inside ChromaDB

This creates a searchable knowledge base for learning.

---

## 3. Retrieval-Augmented Generation (RAG)

When a learner asks a question:

1. Relevant document chunks are retrieved.
2. Retrieved context is provided to the language model.
3. The model generates a grounded response.

Benefits:

* Reduced hallucinations
* Higher factual accuracy
* Answers based on uploaded learning material

---

## 4. Conversational Memory

The chatbot stores conversation history for each learner.

This allows the system to:

* Maintain context across sessions
* Remember previous discussions
* Provide personalized responses
* Support long-term learning interactions

Conversation histories are stored locally and linked to user profiles.

---

## 5. Personalized Learning Profiles

Each learner develops a unique educational profile over time.

The system can identify:

* Topics studied
* Recurring interests
* Learning patterns
* Areas requiring further practice

Example:

```text
Profile: akky

Topics Discussed:
- Neural Networks
- Backpropagation
- RNNs
- Attention Mechanisms
- Transformers
```

---

## 6. Web-Based Interface

The application includes a Flask frontend that provides:

* User authentication pages
* Chat interface
* Session support
* Personalized interactions

Current Pages:

* Login Page
* Registration Page
* Chat Interface

---

# System Architecture

```text
User
 │
 ▼
Flask Web Interface
 │
 ▼
Authentication Layer
 │
 ▼
Chatbot Engine
 │
 ├── Retrieval System (RAG)
 │
 ├── Conversation Memory
 │
 └── Learning Intelligence
         │
         ▼
      Future Analytics
```

---

# Technology Stack

## Backend

* Python
* Flask

## Language Models

* Ollama
* Llama Models

## Embeddings

* Ollama Embeddings

## Frameworks

* LangChain

## Vector Database

* ChromaDB

## Storage

* SQLite
* JSON Memory Files
* Chroma Vector Store

---

# Project Structure

```text
DS-RAG/
│
├── app.py                 # Flask application
├── chatbot.py             # Main chatbot logic
├── ingest.py              # Document ingestion
├── vectorstore.py         # ChromaDB operations
│
├── auth.py                # Authentication logic
├── database.py            # Database operations
├── init_db.py             # Database initialization
├── config.py              # Configuration settings
│
├── memory.py              # Conversation memory
├── learning.py            # Learning analytics
│
├── database.db            # SQLite database
│
├── data/                  # Source documents
├── vectorstore/           # Chroma storage
├── conversations/         # User histories
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd DS-RAG
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Start Ollama

```bash
ollama serve
```

Pull required models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

---

## 4. Ingest Learning Materials

Place PDF files inside:

```text
data/
```

Run:

```bash
python ingest.py
```

---

## 5. Initialize Database

```bash
python init_db.py
```

---

## 6. Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

# Example Questions

```text
What is gradient descent?

Explain backpropagation.

Why do RNNs struggle with long sequences?

How does self-attention work?

Compare CNNs and Vision Transformers.

Summarize the uploaded chapter.
```

---

# Roadmap

## Phase 1 — Core Educational RAG System ✅

Completed:

* User authentication
* Document ingestion
* Embeddings generation
* ChromaDB integration
* Retrieval pipeline
* Conversational memory
* Flask web interface

---

## Phase 2 — Conversational Summaries 🚧

Goal:

Compress conversation history into educational summaries.

Example:

```text
User Learned:
- Neural Networks
- Gradient Descent
- Backpropagation

Current Difficulties:
- Vanishing Gradients
- Sequence Modeling
```

Benefits:

* Better long-term memory
* Reduced token usage
* Improved personalization

---

## Phase 3 — Learning Analytics Dashboard 🚧

Goal:

Create a learner profile that tracks educational progress.

Metrics:

* Topics studied
* Learning depth
* Knowledge growth
* Revision requirements

Example:

```text
Machine Learning: 85%
Deep Learning: 65%
Transformers: 45%
LLMs: 20%
```

---

## Phase 4 — Recommendation Engine 🚧

Goal:

Recommend future study topics based on learning history.

Example:

```text
Completed:
✓ Neural Networks

Recommended Next:
→ Backpropagation
→ Optimization Algorithms
```

```text
Completed:
✓ RNNs

Recommended Next:
→ Attention Mechanisms
→ Transformers
```

---

## Phase 5 — Intelligent Educational Assistant 🚧

Long-Term Vision:

An AI tutor capable of:

* Remembering long-term learning history
* Tracking learner progress
* Identifying knowledge gaps
* Generating quizzes
* Creating personalized study plans
* Recommending learning paths
* Acting as an adaptive educational mentor

---

# Research Objective

The objective of this project is to investigate how Retrieval-Augmented Generation (RAG), conversational memory, learning analytics, and recommendation systems can be integrated to create adaptive educational AI systems.

The research focuses on moving beyond simple question-answering systems toward intelligent tutoring systems that support long-term learning and skill development.

---

# Author

**Axit Patel**
MSc Final Year Project

Educational AI & Retrieval-Augmented Generation Systems
