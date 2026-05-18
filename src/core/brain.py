import ollama
import json

class ChibiBrain:
    def __init__(self, reasoning_model="qwen:4b", coding_model="codellama:7b"):
        self.reasoning_model = reasoning_model
        self.coding_model = coding_model
        self.current_model = None

    def query(self, prompt, use_coding_model=False):
        target_model = self.coding_model if use_coding_model else self.reasoning_model

        # In an 8GB RAM environment, we explicitly rely on Ollama's model management.
        try:
            response = ollama.chat(model=target_model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            return response['message']['content']
        except Exception as e:
            return f"Thinking error: {e}"

    def reflect_on_error(self, error_message):
        prompt = f"I encountered this error: {error_message}. How can I fix it and what did I learn?"
        return self.query(prompt)
