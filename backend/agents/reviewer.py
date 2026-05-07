import requests
import json
import os

class ReviewerAgent:
    def __init__(self, model_name: str = "llama3-8b-8192"):
        self.model_name = model_name
        self.groq_api_key = os.environ.get("GROQ_API_KEY", "")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

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

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result_text = response.json()["choices"][0]["message"]["content"]
            
            try:
                result = json.loads(result_text)
                return {
                    "is_hallucination": result.get("is_hallucination", False),
                    "confidence": result.get("confidence", "Unknown"),
                    "reasoning": result.get("reasoning", "")
                }
            except json.JSONDecodeError:
                return {"is_hallucination": False, "confidence": "Low", "reasoning": "Failed to parse reviewer JSON output."}
                
        except Exception as e:
            err_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                err_msg += f" - {e.response.text}"
            return {"is_hallucination": False, "confidence": "Unknown", "reasoning": f"Failed to contact reviewer LLM: {err_msg}"}
