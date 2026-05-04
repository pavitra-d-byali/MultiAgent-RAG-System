import requests
import json

class ReviewerAgent:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"

    def review(self, query: str, draft_response: str, context: str) -> dict:
        prompt = f"""You are an objective AI reviewer. Your task is to evaluate a drafted response against the provided source context. 
Determine if the draft contains hallucinations (information not supported by the context).

Context:
{context}

Drafted Response:
{draft_response}

User Query:
{query}

Reply in strictly JSON format with the following keys:
- "is_hallucination": boolean (true if the draft contains unverified claims, false if it is fully supported by the context)
- "confidence": string (High, Medium, or Low)
- "reasoning": string (brief explanation of your decision)
"""

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            result_text = response.json().get("response", "{}")
            
            try:
                result = json.loads(result_text)
                return {
                    "is_hallucination": result.get("is_hallucination", False),
                    "confidence": result.get("confidence", "Unknown"),
                    "reasoning": result.get("reasoning", "")
                }
            except json.JSONDecodeError:
                return {"is_hallucination": False, "confidence": "Low", "reasoning": "Failed to parse reviewer JSON output."}
                
        except requests.exceptions.RequestException as e:
            return {"is_hallucination": False, "confidence": "Unknown", "reasoning": "Failed to contact reviewer LLM."}
