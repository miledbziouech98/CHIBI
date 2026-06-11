import ollama
import json

class YozuBrain:
    def __init__(self, reasoning_model="dolphin-llama3:8b-v2.9-q4_K_M", coding_model="deepseek-coder:6.7b-instruct-q4_K_M", vision_model="llava:7b-v1.6-mistral-q4_K_M"):
        self.reasoning_model = reasoning_model
        self.coding_model = coding_model
        self.vision_model = vision_model
        self.current_model = None

    def query(self, prompt, use_coding_model=False, tools=None, tool_instances=None):
        target_model = self.coding_model if use_coding_model else self.reasoning_model

        messages = [
            {
                'role': 'user',
                'content': prompt,
            },
        ]

        # In an 8GB RAM environment, we explicitly rely on Ollama's model management.
        try:
            response = ollama.chat(
                model=target_model,
                messages=messages,
                tools=tools
            )

            # Handle tool calls if any
            if response.get('message', {}).get('tool_calls'):
                return self._handle_tool_calls(response['message']['tool_calls'], target_model, messages, tool_instances)

            return response['message']['content']
        except Exception as e:
            return f"Thinking error: {e}"

    def _handle_tool_calls(self, tool_calls, model, messages, tool_instances=None):
        """Execute the tool calls and continue the conversation."""
        if not tool_instances:
            return "[Error: Tools requested but no instances provided to execute them.]"

        messages.append({
            'role': 'assistant',
            'tool_calls': tool_calls
        })

        for tool_call in tool_calls:
            function_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']

            # Map tool name to instance
            result = "Tool not found."
            if function_name in ["read_file", "list_directory", "execute_command"]:
                result = tool_instances['mcp'].call_tool(function_name, **arguments)
            elif function_name in ["trigger_workflow", "list_workflows"]:
                result = tool_instances['n8n'].call_tool(function_name, **arguments)

            messages.append({
                'role': 'tool',
                'content': str(result),
                'name': function_name
            })

        # Final response from model after seeing tool output
        try:
            final_response = ollama.chat(model=model, messages=messages)
            return final_response['message']['content']
        except Exception as e:
            return f"Error after tool execution: {e}"

    def reflect_on_error(self, error_message):
        prompt = f"I encountered this error: {error_message}. How can I fix it and what did I learn?"
        return self.query(prompt)
