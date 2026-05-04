from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RetrieverAgent:
    def __init__(self):
        # We use a lightweight local embeddings model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.vectorstore = None

    def add_document(self, text: str, metadata: dict = None):
        if metadata is None:
            metadata = {}
        
        chunks = self.text_splitter.split_text(text)
        metadatas = [metadata for _ in chunks]
        
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_texts(texts=chunks, embedding=self.embeddings, metadatas=metadatas)
        else:
            self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)

    def retrieve(self, query: str, top_k: int = 3):
        if self.vectorstore is None:
            return []
        
        docs = self.vectorstore.similarity_search(query, k=top_k)
        return [{"text": doc.page_content, "metadata": doc.metadata} for doc in docs]
