import requests

class GeneratorAgent:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"

    def generate(self, query: str, context: str) -> str:
        prompt = f"""You are a helpful AI assistant. Answer the user's query based ONLY on the provided context. If the answer is not in the context, say "I don't know based on the provided context."

Context:
{context}

Query: {query}

Answer:"""

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.exceptions.RequestException as e:
            return f"Error communicating with local Ollama instance: {str(e)}\nPlease ensure Ollama is running with the '{self.model_name}' model."
