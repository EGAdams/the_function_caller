#
# first friday
# Send Message Tool
#
import xmlrpc

class SendMessageTool:
    """
    Provides a tool for sending messages to other agents using their ID.
    The `SendMessageTool` class exposes a `send_message` function that can be used to send a message to another agent.
    The `schema` method returns a JSON schema that describes the parameters expected by the `send_message` function.
    """
    def __init__(self, agents_urls: dict):
        """
        Initialize the SendMessageTool with a dictionary of agent IDs and their corresponding URLs.

        Args:
            agents_urls (dict): A dictionary mapping agent IDs to their RPC URLs.
        """
        self.agents_urls = agents_urls

    def schema(self):
        """
        Returns the JSON schema for the function.

        Returns:
            dict: JSON schema defining the expected parameters for the send_message function.
        """
        return {
            "name": "send_message",
            "description": "Allows the AI to send messages to other agents using their ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_id": {
                        "type": "string",
                        "description": "The ID of the recipient agent."
                    },
                    "message": {
                        "type": "string",
                        "description": "The content of the message to send."
                    }
                },
                "required": ["recipient_id", "message"]
            }
        }

    def send_message(self, recipient_id: str, message: str):
        """
        Sends a message to the specified recipient via their ID.

        Args:
            recipient_id (str): The ID of the recipient agent.
            message (str): The content of the message to send.

        Returns:
            nothing: The function does not return anything.
            
            
        note: the collaborator may get this and route it, we'll see...
        """
        recipient_url = self.agents_urls.get(recipient_id)
        if not recipient_url:
            return f"Error: Unknown recipient ID '{recipient_id}'."

        try:
            with xmlrpc.client.ServerProxy(recipient_url) as receiving_agent: # send the message to the recipient agent
                print(f"Sending message to {recipient_id} at {recipient_url}: {message}")
                receiving_agent_response = receiving_agent.receive_message({"message": message}) # invoke receive_message

                with xmlrpc.client.ServerProxy(self.agents_urls["collaborator"]) as collaborator: # assign collaborator

                    # prepend the message with `{recipient_id}:` so that the collaborator knows who sent the message.
                    message = f"{recipient_id}: { receiving_agent_response }" # it's like putting an address on an envelope
                                                                              # before sending it to the post office
                    collaborator.receive_message( message )                   

        except Exception as e:
            return f"Error: Failed to send message to {recipient_id}: {e}"
