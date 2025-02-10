# https://chatgpt.com/share/6778c573-77d0-8006-abe3-e0a7b0512b79
import xmlrpc.client

# Replace with the CoderAgent's server details
CODER_AGENT_URL = "http://localhost:8003"

def chat_with_coder_agent():
    """
    Chat with the CoderAgent via XML-RPC.
    """
    try:
        # Connect to the CoderAgent's XML-RPC server
        remote_agent = xmlrpc.client.ServerProxy(CODER_AGENT_URL, allow_none=True)
        print(f"Connected to CoderAgent at: {CODER_AGENT_URL}")

        while True:
            # Get user input
            user_message = input("You: ").strip()
            if user_message.lower() in {"exit", "quit", "bye", "kk", "x", "q"}:
                print("Exiting chat.")
                break

            # Send the message to the agent
            message = {"command": "process_message", "message": user_message}
            print(f"Sending message: {message}")

            try:
                # Get and display the response
                response = remote_agent.receive_message(message)
                if isinstance(response, dict):
                    agent_response = response.get("response", "No response")
                else:
                    agent_response = str(response)  # Ensure any unexpected response is displayed as a string
                print(f"CoderAgent: {agent_response}")

            except xmlrpc.client.Fault as fault:
                print(f"CoderAgent returned an XML-RPC Fault: {fault}")
            except Exception as e:
                print(f"Error while sending message to CoderAgent: {e}")

    except xmlrpc.client.Fault as fault:
        print(f"XML-RPC Fault: {fault}")
    except Exception as e:
        print(f"Error during chat setup: {e}")

if __name__ == "__main__":
    chat_with_coder_agent()
