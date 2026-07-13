# Multi-Agent AI Customer Support Assistant

## Project Overview

This project is a web-based AI-powered customer support assistant built using FastAPI, LangChain, ChromaDB, and Large Language Models (LLMs).

Unlike a traditional chatbot, this system uses multiple specialized AI agents to understand customer intent and route requests to the appropriate agent.

---

## Features

- Multi-Agent Architecture
- Intent Detection
- Order Support Agent
- Refund Support Agent
- Payment Support Agent
- Technical Support Agent
- FAQ Agent using RAG
- Escalation Agent
- Conversation Memory
- Conversation Logging
- FastAPI REST API
- ChromaDB Vector Database

---

## Technologies Used

- Python
- FastAPI
- LangChain
- ChromaDB
- Sentence Transformers
- Hugging Face Embeddings
- LM Studio
- Qwen2.5-Coder LLM

---

## Project Structure

```
customer-support-ai/
│
├── agents/
├── services/
├── data/
├── vectorstore/
├── main.py
├── build_db.py
├── requirements.txt
├── README.md
└── chat_logs.json
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Build the vector database:

```bash
python build_db.py
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Future Improvements

- Authentication
- Database Integration
- Email Notifications
- Voice Support
- Dashboard Analytics
- Docker Deployment

---

## Author

Ishu Sharma