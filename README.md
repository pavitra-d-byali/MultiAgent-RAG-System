# 🤖 Multi-Agent RAG System

A production-grade, self-correcting Multi-Agent Retrieval-Augmented Generation (RAG) system powered by local LLMs (Ollama/Llama-3). This project demonstrates a pipeline of autonomous agents working together to retrieve context, generate an answer, and independently review it for hallucinations.

## 🏗️ Architecture

The system uses three coordinated agents:
1. **RetrieverAgent**: Embeds documents into a FAISS vector store using local HuggingFace embeddings (`all-MiniLM-L6-v2`) and retrieves context chunks based on semantic similarity.
2. **GeneratorAgent**: Interfaces with a local Ollama instance (e.g., `llama3.2` or `llama-3`) to synthesize an answer grounded strictly in the retrieved context.
3. **ReviewerAgent**: A self-correction agent that independently checks the Generator's draft against the context to detect hallucinations before showing the final output.

## 🚀 Quick Start

Ensure you have Python 3.9+ and [Ollama](https://ollama.com) installed.

### 1. Setup Local LLM

Pull a local model via Ollama (e.g., `llama3.2`):
```bash
ollama pull llama3.2
```
*Ensure the Ollama server is running in the background.*

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend API (FastAPI)
```bash
uvicorn backend.main:app --reload --port 8000
```

### 4. Run the Frontend Dashboard (Streamlit)
In a new terminal:
```bash
streamlit run frontend/app.py
```
Navigate to `http://localhost:8501` to view the interactive dashboard.

## 📂 Project Structure

```text
├── backend/
│   ├── main.py                 # FastAPI core backend
│   └── agents/
│       ├── retriever.py        # VectorDB and retrieval logic
│       ├── generator.py        # Generation via local LLM
│       └── reviewer.py         # Output verification logic
├── frontend/
│   └── app.py                  # Streamlit Chat interface
├── requirements.txt            # Dependency graph
└── README.md
```
