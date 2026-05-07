import requests
import os

class GeneratorAgent:
    def __init__(self, model_name: str = "llama3-8b-8192"):
        self.model_name = model_name
        self.groq_api_key = os.environ.get("GROQ_API_KEY", "")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, query: str, context: str) -> str:
        prompt = f"""You are a helpful AI assistant. Answer the user's query based ONLY on the provided context. If the answer is not in the context, say "I don't know based on the provided context."

Context:
{context}

Query: {query}

Answer:"""

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            err_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                err_msg += f" - {e.response.text}"
            return f"Error communicating with Groq API: {err_msg}"
