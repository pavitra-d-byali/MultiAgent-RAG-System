# 🤖 Multi-Agent RAG System

A production-grade, self-correcting Multi-Agent Retrieval-Augmented Generation (RAG) system powered by **Groq API** (Llama-3). This project demonstrates a pipeline of autonomous agents working together to retrieve context, generate an answer, and independently review it for hallucinations.

## 🏗️ Architecture

The system uses three coordinated agents:
1. **RetrieverAgent**: Embeds documents into a FAISS vector store using local HuggingFace embeddings (`all-MiniLM-L6-v2`) and retrieves context chunks based on semantic similarity.
2. **GeneratorAgent**: Interfaces with the **Groq API** (`llama3-8b-8192`) to synthesize an answer grounded strictly in the retrieved context.
3. **ReviewerAgent**: A self-correction agent that independently checks the Generator's draft against the context to detect hallucinations before showing the final output.

## 🚀 Quick Start

Ensure you have **Python 3.9+** and a **Groq API key** (free at [console.groq.com](https://console.groq.com)).

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/MultiAgent-RAG-System.git
cd MultiAgent-RAG-System
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Backend API (FastAPI)
```bash
uvicorn backend.main:app --reload --port 8000
```

### 5. Run the Frontend Dashboard (Streamlit)
In a new terminal:
```bash
streamlit run frontend/app.py
```
Navigate to `http://localhost:8501` to view the interactive dashboard.

---

## 🐳 Docker (Full Stack)

Run the entire system with a single command:
```bash
docker-compose up --build
```
- Backend API → `http://localhost:8000`
- Frontend UI → `http://localhost:8501`

> Make sure your `.env` file is configured before running Docker.

---

## 📂 Project Structure

```text
├── backend/
│   ├── main.py                 # FastAPI core backend
│   ├── Dockerfile              # Backend Docker image
│   └── agents/
│       ├── retriever.py        # VectorDB and retrieval logic (FAISS)
│       ├── generator.py        # Generation via Groq API
│       └── reviewer.py         # Hallucination verification logic
├── frontend/
│   ├── app.py                  # Streamlit Chat interface
│   └── Dockerfile              # Frontend Docker image
├── docker-compose.yml          # Full-stack orchestration
├── requirements.txt            # Dependency graph
├── .env.example                # Environment variable template
└── README.md
```

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com) |

## 🧠 How It Works

```
User Query
    │
    ▼
RetrieverAgent  ──►  FAISS Vector Store (HuggingFace Embeddings)
    │
    ▼  (top-k context chunks)
GeneratorAgent  ──►  Groq API (llama3-8b-8192)
    │
    ▼  (draft answer)
ReviewerAgent   ──►  Groq API (hallucination check)
    │
    ▼
Final Response (with confidence score)
```

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq API (llama3-8b-8192) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS (with disk persistence) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Containerization | Docker + Docker Compose |
