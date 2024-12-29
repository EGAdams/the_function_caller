import os
import sys
import json

home_directory = os.path.expanduser("~")
sys.path.append( home_directory + '/the_function_caller' )

from agents.base_agent.base_agent import BaseAgent

class FileManagerAgent(BaseAgent):
    def __init__(self, agent_id, server_port, mcp_server_command):
        super().__init__(agent_id, server_port, communication_mode="stdio", mcp_server_command=mcp_server_command)

    def process_message(self, message):
        """Handle incoming requests."""
        operation = message.get("operation")
        params = message.get("params", {})

        if operation == "create_file":
            return self.send_mcp_request("write_file", params)
        elif operation == "read_file":
            return self.send_mcp_request("read_file", params)
        elif operation == "list_directory":
            return self.send_mcp_request("list_directory", params)
        elif operation == "delete_file":
            return self.send_mcp_request("delete_file", params)
        else:
            return {"error": f"Unknown operation: {operation}"}

    def send_mcp_request(self, method, params):
        """Send a request to the MCP server via stdio."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        self.mcp_process.stdin.write(json.dumps(payload) + "\n")
        self.mcp_process.stdin.flush()
        response_str = self.mcp_process.stdout.readline().strip()
        return json.loads(response_str)

