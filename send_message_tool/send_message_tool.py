#
# first friday
# Send Message Tool
#
import xmlrpc.client

class SendMessageTool:
    """
    Provides a tool for sending messages to other agents using their ID.
    The `SendMessageTool` class exposes a `send_message` function that can be used to send a packaged message (Python dict) to another agent.
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
            "description": "Sends a message to a specified agent by recipient URL.",
            "parameters": {
                "type": "object",
                "properties": {
                "recipient_url": {
                    "type": "string",
                    "description": "The URL of the recipient agent."
                },
                "message": {
                    "type": "string",
                    "description": "The content of the message to send."
                },
                "author_url": {
                    "type": "string",
                    "description": "The URL of the author sending the message."
                }
                },
                "required": ["recipient_url", "message", "author_url"]
            }
        }

    def send_message(self, recipient_id: str, packaged_message: dict):
        """
        Sends a packaged message (Python dict) to the specified recipient via their ID.

        Args:
            recipient_id (str): The ID of the recipient agent.
            packaged_message (dict): The packaged message to send.

        Returns:
            str: Success or error message.
        """
        # Lookup recipient URL
        recipient_url = self.agents_urls.get(recipient_id)
        if not recipient_url:
            return f"Error: Unknown recipient ID '{recipient_id}'."

        try:
            # Create an XML-RPC connection to the recipient
            with xmlrpc.client.ServerProxy(recipient_url) as receiving_agent:
                print(f"Sending message to {recipient_id} at {recipient_url}: {packaged_message}")
                
                # Send the message to the recipient
                response = receiving_agent.receive_message(packaged_message)

                # Log the response (for debugging)
                print(f"Received response from {recipient_id}: {response}")

                return f"Message successfully sent to {recipient_id}. Response: {response}"

        except Exception as e:
            return f"Error: Failed to send message to {recipient_id}: {e}"


