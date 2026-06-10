# Enterprise RAG Multi-Agent System

A production-grade AI research assistant built with LangGraph, LangChain, and FastAPI. The system uses a **supervisor agent pattern** to intelligently route queries between a PDF research agent and a web search agent, then synthesizes a final answer combining both sources.

## Architecture
User Query → Supervisor Agent → PDF Agent (ChromaDB + HyDE + MMR)
→ Web Agent (Tavily Search)
→ Synthesis Agent → Final Answer

## Features

- **Supervisor Agent Pattern** — LLM-powered router decides which agent handles each query
- **PDF Research Agent** — Advanced RAG with HyDE, MMR retrieval, and persistent ChromaDB
- **Web Search Agent** — Real-time web search using Tavily
- **Synthesis Agent** — Combines research from both agents into one coherent answer
- **FastAPI** — Production REST API with Swagger UI

## Tech Stack

- LangGraph — Multi-agent orchestration
- LangChain — LLM chains and RAG pipeline
- FastAPI — REST API
- ChromaDB — Vector database
- Groq LLaMA 3.1 8B — LLM
- Google Gemini Embeddings — Text embeddings
- Tavily — Web search

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file with your API keys:
GROQ_API_KEY=your_key
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
4. Run the app:
```bash
   uvicorn main:app --reload
```
5. Visit `http://localhost:8000/docs` to test the API

## API

**POST** `/ask`

```json
{
  "question": "What is Charles Bridge?"
}
```

**Response:**

```json
{
  "answer": "Charles Bridge is a medieval stone arch bridge..."
}
```

## Live Demo

https://enterprise-rag-production-fb2e.up.railway.app/docs
