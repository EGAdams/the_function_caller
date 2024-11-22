import sys
sys.path.append( '/home/adamsl/the_function_caller' )
from agents.base_agent import BaseAgent
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

class MessageCollaboratorAgent(BaseAgent):
    def __init__(self, agent_id: str, server_port: int, agents_urls: dict):
        super().__init__(agent_id, server_port)
        self.agents_urls = agents_urls  # Dictionary mapping agent IDs to their RPC URLs

    def send_message(self, recipient_id: str, message: dict):
        """
        Send a message to the specified recipient via their RPC URL.
        """
        recipient_url = self.agents_urls.get(recipient_id)
        if recipient_url:
            try:
                with xmlrpc.client.ServerProxy(recipient_url) as proxy:
                    proxy.receive_message(message)
                    self.logger.info(f"Message sent to {recipient_id}: {message}")
            except Exception as e:
                self.logger.error(f"Failed to send message to {recipient_id}: {e}")
        else:
            self.logger.error(f"Unknown agent: {recipient_id}")

    def process_message(self, message: dict):
        """
        Process incoming messages. Routes commands to other agents.
        """
        try:
            command = message.get("command")
            if not command:
                self.logger.error("Invalid message format. Missing 'command'.")
                return
            
            if command.startswith("coder:"):
                self.send_message("coder", {"message": command[len("coder:"):].strip()})
            elif command.startswith("planner:"):
                self.send_message("planner", {"message": command[len("planner:"):].strip()})
            else:
                self.logger.info(f"Unknown command: {command}")
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")


def main():
    """
    Main entry point for the MessageCollaboratorAgent.
    """
    # Define RPC URLs for other agents
    agents_urls = {
        "planner":      "http://localhost:8002",
        "coder":        "http://localhost:8003",
        "collaborator": "http://localhost:8001",
    }

    # Create the MessageCollaboratorAgent
    collaborator = MessageCollaboratorAgent(agent_id="collaborator_agent", server_port=8001, agents_urls=agents_urls)

    # Start the RPC server for the collaborator
    try:
        collaborator.logger.info("MessageCollaboratorAgent is starting...")
        collaborator.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        collaborator.logger.info("Shutting down...")


if __name__ == "__main__":
    main()
