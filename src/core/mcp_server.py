import os
import json
import subprocess

class YozuMCP:
    """
    Integration with Model Context Protocol (MCP).
    Allows Yozu to use external tools and access local data securely.
    """
    def __init__(self):
        self.tools = []
        self._load_tools()

    def _load_tools(self):
        # Defining tools in Ollama-compatible format
        self.tools = [
            {
                'type': 'function',
                'function': {
                    'name': 'read_file',
                    'description': 'Read content from a local file',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'filepath': {'type': 'string'}
                        },
                        'required': ['filepath']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'list_directory',
                    'description': 'List files in a directory',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'path': {'type': 'string'}
                        }
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'execute_command',
                    'description': 'Run a bash command (use with caution)',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'command': {'type': 'string'}
                        },
                        'required': ['command']
                    }
                }
            }
        ]

    def call_tool(self, tool_name, **kwargs):
        print(f"MCP calling tool: {tool_name} with {kwargs}")

        if tool_name == "read_file":
            filepath = kwargs.get("filepath")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return f.read()
            return "File not found."

        elif tool_name == "list_directory":
            path = kwargs.get("path", ".")
            if os.path.exists(path):
                return str(os.listdir(path))
            return "Path not found."

        elif tool_name == "execute_command":
            command = kwargs.get("command")
            # Basic security check
            forbidden = [";", "&&", "||", ">", "|", "rm -rf", "sudo"]
            if any(char in command for char in forbidden):
                 return "Error: Command contains restricted characters or keywords for security."

            try:
                # Use shell=False for better security where possible
                import shlex
                cmd_args = shlex.split(command)
                result = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)
                return result.decode()
            except subprocess.CalledProcessError as e:
                return f"Error executing command: {e.output.decode()}"
            except Exception as e:
                return f"System error: {e}"

        return f"Tool {tool_name} not implemented."

    def get_tool_definitions(self):
        return self.tools
