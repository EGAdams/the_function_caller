#
# Message Collaborator Agent
#
import sys
sys.path.append('/home/adamsl/the_function_caller')
from agents.base_agent import BaseAgent
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
PORT = 8001

class MessageCollaboratorAgent(BaseAgent):
    def __init__(self, agent_id: str, server_port: int, agents_urls: dict):
        """
        Initializes the MessageCollaboratorAgent with a unique ID, server port, and agent URLs.
        :param agent_id: Unique identifier for this agent.
        :param server_port: Port on which this agent's XML-RPC server will run.
        :param agents_urls: Dictionary mapping agent IDs to their XML-RPC URLs.
        """
        super().__init__(agent_id, server_port)
        self.agents_urls = agents_urls  # Dictionary of other agents' RPC endpoints
        self.message_logs = []  # Maintain a log of all messages for auditing

    def send_message(self, recipient_id: str, message: dict):
        """
        Sends a message to the specified recipient via their RPC URL.
        :param recipient_id: ID of the recipient agent.
        :param message: The message content to be sent.
        """
        recipient_url = self.agents_urls.get(recipient_id)
        if recipient_url:
            try:
                with xmlrpc.client.ServerProxy(recipient_url) as proxy:
                    print(f"Sending message to {recipient_id}: {message}")
                    response = proxy.receive_message(message)
                    self.logger.info(f"Message sent to {recipient_id}: {message}")
                    self.message_logs.append({"to": recipient_id, "message": message})
                    return response  # Return the response from the recipient
            except Exception as e:
                self.logger.error(f"Failed to send message to {recipient_id}: {e}")
                return f"Error: {str(e)}"
        else:
            self.logger.error(f"Unknown recipient: {recipient_id}")
            return f"Error: Unknown recipient {recipient_id}"

    def process_message( self, message: dict ):
        """
        Processes incoming messages and routes commands to other agents.
        :param message: Incoming message dictionary containing the "command" key.
        """
        try:
            command = message.get( "command" )
            if not command:
                self.logger.error("Invalid message format. Missing 'command'.")
                return "Invalid message format. Missing 'command'."
            
            # Coder Agent
            if command.startswith("coder:"):
                response = self.send_message("coder", {"message": command[len("coder:"):].strip()})
                return response
            
            # Planner Agent
            elif command.startswith("planner:"):
                response = self.send_message("planner", {"message": command[len("planner:"):].strip()})
                return response
            
            # Unknown Agent
            else:
                # Handle other commands or respond directly
                self.logger.info(f"Unknown command: {command}")
                return "Unknown command"
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"

    def log_message_activity(self):
        """
        Logs all incoming and outgoing messages for debugging and auditing.
        Stub: Expand to store logs persistently (e.g., in a database or file).
        """
        self.logger.info(f"Message log: {self.message_logs}")

    def interact_with_user(self, user_input: str):
        """
        Allows direct interaction with the agent to handle user questions.
        :param user_input: A command or query from the user.
        """
        try:
            # Process the input as a message
            self.process_message({"command": user_input})
        except Exception as e:
            self.logger.error(f"Error interacting with user: {e}")

    def monitor_agent_health(self):
        """
        Monitors the health of connected agents.
        Stub: Implement periodic checks of agent availability via their RPC endpoints.
        """
        pass


def main():
    """
    Main entry point for the MessageCollaboratorAgent.
    """
    # Define RPC URLs for other agents
    agents_urls = {
        "collaborator"  : "http://localhost:8001",
        "planner"       : "http://localhost:8002",
        "coder"         : "http://localhost:8003",
    }

    # Create the MessageCollaboratorAgent
    collaborator = MessageCollaboratorAgent(agent_id="collaborator_agent", server_port=PORT, agents_urls=agents_urls)

    # Start the RPC server for the collaborator
    try:
        collaborator.logger.info("MessageCollaboratorAgent is starting in port " + str( PORT ) + "...")
        collaborator.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        collaborator.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
