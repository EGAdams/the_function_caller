import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
import xmlrpc.client
from threading import Thread
from test_agent import run_test_agent  # Import the TestAgent runner

CODER_AGENT_URL = "http://localhost:8003"
TEST_AGENT_URL = "http://localhost:8004"  # URL of the TestAgent

def chat_with_coder_agent():
    """
    Chat with the CoderAgent via XML-RPC and allow receiving messages via TestAgent.
    """
    try:
        # Connect to the CoderAgent's XML-RPC server
        coder_agent = xmlrpc.client.ServerProxy(CODER_AGENT_URL, allow_none=True)
        print(f"Connected to CoderAgent at: {CODER_AGENT_URL}")

        # Start the TestAgent in a separate thread
        test_agent_thread = Thread(target=run_test_agent, daemon=True)
        test_agent_thread.start()
        print(f"TestAgent is running at: {TEST_AGENT_URL}")

        while True:
            # Get user input
            user_message = input("You: ").strip()
            if user_message.lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break

            # Send the message to the CoderAgent
            message = {"command": "process_message", "message": user_message}
            print(f"Sending message: {message}")
            try:
                response = coder_agent.receive_message(message)
                agent_response = response.get("response", "No response")
                print(f"CoderAgent: {agent_response}")
            except xmlrpc.client.Fault as fault:
                print(f"CoderAgent returned an XML-RPC Fault: {fault}")
            except Exception as e:
                print(f"Error while sending message to CoderAgent: {e}")

    except Exception as e:
        print(f"Error during chat setup: {e}")

if __name__ == "__main__":
    chat_with_coder_agent()
