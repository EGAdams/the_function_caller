# https://chatgpt.com/share/6778c573-77d0-8006-abe3-e0a7b0512b79
import xmlrpc.client

# Replace with the CoderAgent's server details
CODER_AGENT_URL = "http://localhost:8003"

def chat_with_coder_agent():
    try:
        # Connect to the CoderAgent's XML-RPC server
        remote_agent = xmlrpc.client.ServerProxy( CODER_AGENT_URL )

        print( "Connected to CoderAgent at:", CODER_AGENT_URL )

        while True:
            # Get user input
            user_message = input( "You: " )
            if user_message.lower() in {"exit", "quit"}:
                print( "Exiting chat." )
                break

            # Send the message to the agent
            message = { "command": "process_message", "message": user_message }
            print ( "Sending message:", message )
            response = remote_agent.receive_message( message )

            # Display the agent's response
            print( "CoderAgent:", response.get("response", "No response" ))

    except Exception as e:
        print( "Error during chat:", e )

if __name__ == "__main__":
    chat_with_coder_agent()
