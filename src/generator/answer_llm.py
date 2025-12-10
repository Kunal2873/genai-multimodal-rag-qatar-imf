import requests

class AnswerLLM:
    def __init__(self, model_name="mistral"):
        self.model = model_name

    def _generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        return response.json().get("response", "")

    def answer(self, question, context, citations):
        prompt = f"""
Extract the exact factual value from the context. Do not generalize.
If the context contains a specific date, number, or timeline, you MUST state it.
Do not say "not specified" if any part of the context contains the answer.

If the answer is not present, say "Not present in document".
Add citations like (Page X) after each factual statement.

Context:
{context}

Question:
{question}

Answer:
"""
        output = self._generate(prompt)
        return output + "\n\nSources: " + ", ".join(citations)

    def summarize(self, context, citations):
        prompt = f"""
Write a concise economic summary of Qatar using ONLY the provided context.
Do NOT add external info.
Mention:
- GDP growth trends
- Fiscal balance
- Inflation path
- LNG expansion impact
- External sector (surplus/deficit)

Add citations like (Page X).

Context:
{context}

Summary:
"""
        output = self._generate(prompt)
        return output + "\n\nSources: " + ", ".join(citations)
