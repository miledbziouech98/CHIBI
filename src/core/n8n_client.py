import os
import requests
from dotenv import load_dotenv

load_dotenv()

class Yozun8n:
    """
    Integration with n8n for workflow automation.
    """
    def __init__(self):
        self.api_url = os.getenv("N8N_API_URL", "http://localhost:5678/api/v1")
        self.api_key = os.getenv("N8N_API_KEY")

    def trigger_workflow(self, workflow_id, data=None):
        if not self.api_key:
            return "n8n API key not configured."

        endpoint = f"{self.api_url}/workflows/{workflow_id}/run"
        headers = {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(endpoint, json=data or {}, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"n8n trigger failed: {e}"

    def list_workflows(self):
        if not self.api_key:
            return "n8n API key not configured."

        endpoint = f"{self.api_url}/workflows"
        headers = {"X-N8N-API-KEY": self.api_key}

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"n8n list failed: {e}"

    def call_tool(self, tool_name, **kwargs):
        if tool_name == "trigger_workflow":
            return self.trigger_workflow(kwargs.get("workflow_id"), kwargs.get("data"))
        elif tool_name == "list_workflows":
            return self.list_workflows()
        return "n8n tool not implemented."

    def get_tool_definitions(self):
        return [
            {
                'type': 'function',
                'function': {
                    'name': 'trigger_workflow',
                    'description': 'Run a specific n8n workflow',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'workflow_id': {'type': 'string'},
                            'data': {'type': 'object'}
                        },
                        'required': ['workflow_id']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'list_workflows',
                    'description': 'List all available n8n workflows',
                    'parameters': {'type': 'object', 'properties': {}}
                }
            }
        ]
