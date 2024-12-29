import xmlrpc.client
import sys

def main():
    # Ensure the correct number of arguments are passed
    if len(sys.argv) < 3:
        print("Usage: python3 client.py <operation> <params (JSON format)>")
        print("Example: python3 client.py create_file '{\"path\": \"test.txt\", \"content\": \"Hello, World!\"}'")
        sys.exit(1)

    # Parse operation and params
    operation = sys.argv[1]
    try:
        import json
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"Error parsing params as JSON: {e}")
        sys.exit(1)

    # Connect to the FileManagerAgent
    server_url = "http://localhost:8005"
    try:
        proxy = xmlrpc.client.ServerProxy(server_url)
        print(f"Connected to FileManagerAgent at {server_url}")
    except Exception as e:
        print(f"Error connecting to FileManagerAgent: {e}")
        sys.exit(1)

    # Make the request
    try:
        print(f"Calling operation '{operation}' with params {params}")
        response = proxy.process_message({"operation": operation, "params": params})
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Error making request to FileManagerAgent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
