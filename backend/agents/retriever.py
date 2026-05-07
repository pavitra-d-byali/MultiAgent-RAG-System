from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

FAISS_INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "./faiss_index")

class RetrieverAgent:
    def __init__(self):
        # Lightweight local embeddings model — no API key needed
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.vectorstore = None
        self._load_index()

    def _load_index(self):
        """Load existing FAISS index from disk if it exists."""
        if os.path.exists(FAISS_INDEX_PATH):
            try:
                self.vectorstore = FAISS.load_local(
                    FAISS_INDEX_PATH,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"[RetrieverAgent] Loaded existing FAISS index from '{FAISS_INDEX_PATH}'")
            except Exception as e:
                print(f"[RetrieverAgent] Warning: Could not load FAISS index: {e}")
                self.vectorstore = None

    def _save_index(self):
        """Persist FAISS index to disk."""
        if self.vectorstore is not None:
            self.vectorstore.save_local(FAISS_INDEX_PATH)

    def add_document(self, text: str, metadata: dict = None):
        if metadata is None:
            metadata = {}

        chunks = self.text_splitter.split_text(text)
        metadatas = [metadata for _ in chunks]

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_texts(
                texts=chunks, embedding=self.embeddings, metadatas=metadatas
            )
        else:
            self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)

        # Persist after every new document
        self._save_index()
        print(f"[RetrieverAgent] Saved FAISS index with {len(chunks)} new chunk(s).")

    def retrieve(self, query: str, top_k: int = 3):
        if self.vectorstore is None:
            return []

        docs = self.vectorstore.similarity_search(query, k=top_k)
        return [{"text": doc.page_content, "metadata": doc.metadata} for doc in docs]
