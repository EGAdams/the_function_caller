import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
import xmlrpc.client

def chat_with_agents():
    """
    Chat with the remote CoderAgent or TestAgent via XML-RPC.
    """
    try:
        # Connect to the remote agents
        remote_coder_agent = xmlrpc.client.ServerProxy(CODER_AGENT_URL, allow_none=True)
        remote_test_agent = xmlrpc.client.ServerProxy(TEST_AGENT_URL, allow_none=True)

        print(f"Connected to CoderAgent at: {CODER_AGENT_URL}")
        print(f"Connected to TestAgent at: {TEST_AGENT_URL}")

        while True:
            # Get user input for agent selection
            target_agent = input("Select agent (coder/test): ").strip().lower()
            if target_agent not in {"coder", "test"}:
                print("Invalid agent selection. Choose 'coder' or 'test'.")
                continue

            # Get user input for the message
            user_message = input("You: ").strip()
            if user_message.lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break

            # Construct the message
            message = {
                "command": "process_message",
                "author_url": TEST_AGENT_URL if target_agent == "coder" else CODER_AGENT_URL,
                "message": user_message,
            }

            # Send the message to the selected agent
            try:
                target_agent_proxy = remote_coder_agent if target_agent == "coder" else remote_test_agent
                response = target_agent_proxy.receive_message(message)

                if response is None:
                    print("No response from agent.")
                    continue

                agent_response = response.get("response", "No response")
                print(f"{target_agent.capitalize()}Agent: {agent_response}")
            except xmlrpc.client.Fault as fault:
                print(f"{target_agent.capitalize()}Agent returned an XML-RPC Fault: {fault}")
            except Exception as e:
                print(f"Error while sending message to {target_agent.capitalize()}Agent: {e}")

    except Exception as e:
        print(f"Error during chat setup: {e}")

# Constants for agent URLs
CODER_AGENT_PORT    = 8003
TEST_AGENT_PORT     = 8004
CODER_AGENT_URL     = f"http://localhost:{CODER_AGENT_PORT}"
TEST_AGENT_URL      = f"http://localhost:{TEST_AGENT_PORT}"

if __name__ == "__main__":
    chat_with_agents()
