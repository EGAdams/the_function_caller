import os
import sys
import json
from xmlrpc.server import SimpleXMLRPCServer
import requests

home_directory = os.path.expanduser("~")
sys.path.append( home_directory + '/the_function_caller' )
from agents.base_agent.base_agent import BaseAgent

class FileManagerAgent(BaseAgent):
    def __init__(self, agent_id, server_port, mcp_server_url):
        super().__init__(agent_id, server_port)
        self.mcp_server_url = mcp_server_url

    def send_mcp_request(self, method, params):
        """Send a JSON-RPC request to the MCP server."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        try:
            response = requests.post(self.mcp_server_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error communicating with MCP server: {e}")
            return {"error": str(e)}

    def create_file(self, path, content):
        """Create or overwrite a file."""
        params = {"path": path, "content": content}
        return self.send_mcp_request("write_file", params)

    def read_file(self, path):
        """Read a file's content."""
        params = {"path": path}
        return self.send_mcp_request("read_file", params)

    def list_directory(self, path):
        """List contents of a directory."""
        params = {"path": path}
        return self.send_mcp_request("list_directory", params)

    def delete_file(self, path):
        """Delete a file."""
        params = {"path": path}
        return self.send_mcp_request("delete_file", params)

    def process_message(self, message):
        """Handle incoming requests."""
        try:
            operation = message.get("operation")
            params = message.get("params", {})

            if operation == "create_file":
                return self.create_file(params["path"], params["content"])
            elif operation == "read_file":
                return self.read_file(params["path"])
            elif operation == "list_directory":
                return self.list_directory(params["path"])
            elif operation == "delete_file":
                return self.delete_file(params["path"])
            else:
                return {"error": f"Unknown operation: {operation}"}
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    import sys

    # if len(sys.argv) != 4:
    #     print("Usage: python file_manager_agent.py <agent_id> <server_port> <mcp_server_url>")
    #     sys.exit(1)

    # python file_manager_agent.py FileManager 8001 http://localhost:8000
    agent_id        = "FileManager"             # sys.argv[ 1 ]
    server_port     = 8005                      # sys.argv[ 2 ]
    mcp_server_url  = "http://localhost:8005"   # sys.argv[ 3 ]


    agent = FileManagerAgent(agent_id, server_port, mcp_server_url)
    agent.run()
