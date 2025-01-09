import xmlrpc.client

from colorama import Fore, Style  # Add this import

author_name = "Collaborator"
THIS_URL = "http://localhost:8001"
# Mock string_to_function method to resolve class names dynamically
def string_to_function(class_name: str):
    # This would typically use globals() or a registry to find the class dynamically
    return globals().get(class_name)

# Base class for agent-specific handling
class AgentHandler:
    def handle_response(self, response: str):
        raise NotImplementedError("This method should be overridden in subclasses")

class CoderHandler(AgentHandler):
    def handle_response(self, response: str):
        print(f"{Fore.BLUE}Coder's response: {response}{Style.RESET_ALL}")

class PlannerHandler(AgentHandler):
    def handle_response(self, response: str):
        print(f"{Fore.YELLOW}Planner's response: {response}{Style.RESET_ALL}")

class DefaultHandler(AgentHandler):
    def handle_response(self, response: str):
        print(f"Collaborator's response: {response}")

# Main function to send the message
def send_message(collaborator, message: str, author_name: str, recipient_name: str, recipient_url: str):
    try:
        import json

        # Package the message as a Python dictionary
        packaged_message = {
            "message": message,
            "author": {
                "name": author_name,
                "url": THIS_URL
            },
            "recipient": {
                "name": recipient_name,
                "url": recipient_url
            }
        }

        print( "capturing the response from the collaborator..." )
        response = collaborator.receive_message(packaged_message)

        print( "now dynamically resolve and instantiate the appropriate handler." )
        class_name = f"{recipient_name.capitalize()}Handler"
        print( "class_name: ", class_name )
        handler_class = string_to_function(class_name)
        handler = handler_class() if handler_class else DefaultHandler()

        print("\n")
        handler.handle_response(response)
        print("\n")

    except Exception as e:
        print(f"{Fore.RED}Failed to send message: {e}{Style.RESET_ALL}")

def main():
    # URL of the collaborator's RPC server
    collaborator_url = "http://localhost:8001"

    from colorama import init
    init(autoreset=True)  # Initialize colorama

    try:
        # Create the collaborator for the collaborator's server
        with xmlrpc.client.ServerProxy( collaborator_url ) as collaborator:
            print("Chat client for MessageCollaboratorAgent")
            print("Type your message and press Enter. Type 'exit' to quit.")
            
            recipient_url = "http://localhost:8001" # Default recipient is the collaborator itself

            while True:
                print("\nSelect recipient:")  # menu for the user to select the recipient
                print("1. Coder")
                print("2. Planner")
                print("3. ExpertPrompter")
                recipient_choice = input( "Enter the Agent to send the message to: " )
                if recipient_choice == "1":
                    recipient_name = "Coder"
                    recipient_url = "http://localhost:8003"
                elif recipient_choice == "2":
                    recipient_name = "Planner"
                    recipient_url = "http://localhost:8002"
                elif recipient_choice == "3":
                    recipient_name = "ExpertPrompter"
                    recipient_url = "http://localhost:8004"
                else:
                    print("Invalid choice. Please select a valid option.")
                    continue


                # Get input from the user
                message = input( "Enter your message for the " + recipient_name + ": " )
                
                if message.lower() == "exit":
                    print("Exiting chat client. Goodbye!")
                    break
                
                # Send the message as a command to the collaborator
                try:
                    # Capture the response from the collaborator.
                    # calling the receive_message( String message ); method 
                    # in order to invoke the collaborator's receive_message( String message ); method
                    collaborator_id = "collaborator"
                    send_message( collaborator, message, collaborator_id, recipient_name, recipient_url )

                except Exception as e:
                    print( f"{ Fore.RED }Failed to send message: { e }" )

    except Exception as e:
        print(f"Error connecting to collaborator: {e}")

if __name__ == "__main__":
    main()

# Example usage
# class MockCollaborator:
#     def receive_message(self, message: str) -> str:
#         return f"Received: {message}"


# Example messages
# collaborator = MockCollaborator()
# send_message(collaborator, "Implement this feature", "coder", "planner")
# send_message(collaborator, "Create a new plan", "planner", "collaborator")
# send_message(collaborator, "Just a general message", "collaborator", "coder")