import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Multi-Agent RAG", page_icon="🤖", layout="wide")

st.title("🤖 Multi-Agent Self-Correcting RAG System")
st.markdown("Upload documents and ask questions. The Multi-Agent system will retrieve context, generate an answer, and self-review for hallucinations.")

# Sidebar for file upload
with st.sidebar:
    st.header("1. Upload Knowledge")
    uploaded_file = st.file_uploader("Upload a text document", type=["txt", "md"])
    if st.button("Ingest Document"):
        if uploaded_file is not None:
            with st.spinner("Ingesting into vector store..."):
                files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
                try:
                    res = requests.post(f"{API_URL}/upload", files=files)
                    if res.status_code == 200:
                        st.success(f"Successfully ingested {uploaded_file.name}!")
                    else:
                        st.error(f"Error: {res.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Is FastAPI running on port 8000?")
        else:
            st.warning("Please upload a file first.")

# Main Chat Interface
st.header("2. Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if query := st.chat_input("Ask about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Process response
    with st.chat_message("assistant"):
        with st.status("Agent Pipeline Running...", expanded=True) as status:
            st.write("🔍 RetrieverAgent finding context...")
            st.write("🧠 GeneratorAgent drafting response (Ollama)...")
            st.write("🕵️ ReviewerAgent checking for hallucinations...")
            
            try:
                res = requests.post(f"{API_URL}/query", json={"query": query})
                if res.status_code == 200:
                    data = res.json()
                    status.update(label="Pipeline Complete!", state="complete", expanded=False)
                    
                    response_text = data["response"]
                    if data["is_hallucination"]:
                        st.error(f"Hallucination detected! Confidence: {data['confidence']}")
                    else:
                        st.success(f"Verified context-grounded response. Confidence: {data['confidence']}")
                        
                    st.markdown("### Answer")
                    st.markdown(response_text)
                    
                    if data["sources"]:
                        st.caption(f"Sources: {', '.join(data['sources'])}")
                    
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    status.update(label="Error in Pipeline", state="error")
                    st.error(f"Backend error: {res.text}")
            except requests.exceptions.ConnectionError:
                status.update(label="Connection Error", state="error")
                st.error("Cannot connect to backend API. Please start FastAPI.")
