import xmlrpc.client

def main():
    # URL of the collaborator's RPC server
    collaborator_url = "http://localhost:8001"

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
                    # invoke the recieving agent's receive_message method `agent.receive_message(message)`
                    # in the collaborator's receive_message method, it will unpack the message and call the
                    # process_message method with the message as an argument.
                    proxy.receive_message( command_packaged_message ) # this prints `None` so instead of returning, 
                    print(f"Message sent to collaborator: {message}") # have the proxy ()
                except Exception as e:
                    print(f"Failed to send message: {e}")
    except Exception as e:
        print(f"Error connecting to collaborator: {e}")

if __name__ == "__main__":
    main()
