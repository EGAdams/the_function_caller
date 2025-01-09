import json
import subprocess
import sys

def main():
    # if len(sys.argv) < 3:
    #     print("Usage: python3 test_client.py <operation> <params (JSON format)>")
    #     print("Example: python3 test_client.py create_file '{\"path\": \"test.txt\", \"content\": \"Hello, World!\"}'")
    #     sys.exit(1)

    operation = "create_file" # sys.argv[1]
    json_params = '{\"path\": \"test.txt\", \"content\": \"Hello, World!\"}'
    try:
        params = json.loads( json_params )
    except json.JSONDecodeError as e:
        print(f"Error parsing params as JSON: {e}")
        sys.exit(1)

    # Start the FileManagerAgent process
    agent_process = subprocess.Popen(
        ["python3", "/home/adamsl/the_function_caller/agents/file_manager_agent/file_manager_agent_exe.py", "FileManagerAgent", "8005", "npx mcp-server-filesystem /home/adamsl/mcp_tools/sand_box/"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send the request
    request = {
        "operation": operation,
        "params": params
    }
    agent_process.stdin.write(json.dumps(request) + "\n")
    agent_process.stdin.flush()

    # Read the response
    response = agent_process.stdout.readline().strip()
    print("Response:", response)

    # Stop the agent process
    agent_process.terminate()

if __name__ == "__main__":
    main()

