import requests

class AnswerLLM:
    def __init__(self, model_name="mistral"):
        self.model = model_name

    def answer(self, question, context, citations):
        prompt = f"""
Use the context to answer the question.
Only rely on the provided context. If the answer is not present, say "Not present in document".
Add citations like (Page X) after each factual statement.

Context:
{context}

Question:
{question}

Answer:
"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=payload)
        output = response.json().get("response", "")
        output += "\n\nSources: " + ", ".join(citations)
        return output
