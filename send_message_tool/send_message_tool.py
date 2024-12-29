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
            "description": "Allows the AI to send messages to other agents using their ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_id": {
                        "type": "string",
                        "description": "The ID of the recipient agent."
                    },
                    "packaged_message": {
                        "type": "object",
                        "description": "The packaged message (Python dict) containing message details.",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "The content of the message to send."
                            },
                            "author": {
                                "type": "object",
                                "description": "Details of the message's author.",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the author."
                                    },
                                    "url": {
                                        "type": "string",
                                        "description": "The URL of the author."
                                    }
                                },
                                "required": ["name", "url"]
                            },
                            "recipient": {
                                "type": "object",
                                "description": "Details of the message's recipient.",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the recipient."
                                    },
                                    "url": {
                                        "type": "string",
                                        "description": "The URL of the recipient."
                                    }
                                },
                                "required": ["name", "url"]
                            }
                        },
                        "required": ["message", "author", "recipient"]
                    }
                },
                "required": ["recipient_id", "packaged_message"]
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
        recipient_url = self.agents_urls.get(recipient_id)
        if not recipient_url:
            return f"Error: Unknown recipient ID '{recipient_id}'."

        try:
            with xmlrpc.client.ServerProxy(recipient_url) as receiving_agent:
                print(f"Sending message to {recipient_id} at {recipient_url}: {packaged_message}")
                
                # Send the packaged message (Python dict) to the recipient
                receiving_agent_response = receiving_agent.receive_message(packaged_message)
                
                # Send the response to the collaborator, if needed
                with xmlrpc.client.ServerProxy(self.agents_urls["collaborator"]) as collaborator:
                    # Modify the message for the collaborator to include the recipient ID
                    collaborator_message = {
                        **packaged_message,
                        "recipient": {"name": recipient_id, "response": receiving_agent_response}
                    }
                    collaborator.receive_message(collaborator_message)

                return f"Message successfully sent to {recipient_id} and routed to collaborator."

        except Exception as e:
            return f"Error: Failed to send message to {recipient_id}: {e}"

