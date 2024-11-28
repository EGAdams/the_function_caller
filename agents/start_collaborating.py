import xmlrpc.client

from colorama import Fore, Style  # Add this import

def main():
    # URL of the collaborator's RPC server
    collaborator_url = "http://localhost:8001"

    from colorama import init
    init(autoreset=True)  # Initialize colorama

    try:
        # Create a proxy for the collaborator's server
        with xmlrpc.client.ServerProxy(collaborator_url) as proxy:
            print("Chat client for MessageCollaboratorAgent")
            print("Type your message and press Enter. Type 'exit' to quit.")
            
            while True:
                # Get input from the user
                message = input( "input command for collaborator: " )
                
                if message.lower() == "exit":
                    print("Exiting chat client. Goodbye!")
                    break
                
                # Send the message as a command to the collaborator
                command_packaged_message = {"command": message}
                try:
                    # Capture the response from the collaborator
                    response = proxy.receive_message(command_packaged_message)
                    
                    # Color the response based on the agent
                    print ( "\n" )
                    if message.startswith("coder:"):
                        print(f"{Fore.BLUE}Coder's response: {response}{Style.RESET_ALL}")
                    elif message.startswith("planner:"):
                        print(f"{Fore.YELLOW}Planner's response: {response}{Style.RESET_ALL}")
                    else:
                        print(f"Collaborator's response: {response}")
                    print ( "\n" )
                except Exception as e:
                    print(f"Failed to send message: {e}")
    except Exception as e:
        print(f"Error connecting to collaborator: {e}")

if __name__ == "__main__":
    main()
