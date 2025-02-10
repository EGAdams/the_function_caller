import sys, os
import json
import xmlrpc.client
from time import sleep
from openai import OpenAI

home_directory = os.path.expanduser("~")
sys.path.append(home_directory + '/the_function_caller')

from commands.process_message_command.process_message_command import ProcessMessageCommand
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent
from agents.base_agent.base_agent import RPCCommunicationStrategyFactory
from agents.base_agent.base_agent import ConsoleLogger

PORT = 8001
GPT_MODEL = "gpt-4o-mini"

class CollaboratorAgent(BaseAgent):
    def __init__(self, agent_id: str, strategy_factory, agent_url: str, logger=None):
        super().__init__(agent_id, strategy_factory, logger or ConsoleLogger())
        self.url = agent_url
        self.client = OpenAI()  # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()
        self.assistant = self.assistant_factory.getExistingAssistant(assistant_id="asst_lRPtbKUVMJPAXt0RttAU8EHg")
        self.run_spinner = RunSpinner(self.client)
        self.thread = self.client.beta.threads.create()  # Create a thread
        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content="How can I assist with collaboration?"
        )
        self.register_command("process_message", ProcessMessageCommand(self))  # Register the message processing command

    def show_json(self, obj):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

    def process_message(self, new_message: dict):
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        try:
            command = new_message.get( "command" )
            print ( "got command in collaborator: ", command )
            if not command:
                self.logger.error("Invalid message format. Missing 'command'.")
                return "Invalid message format. Missing 'command'."
            
            # 'recipient' = {'name': 'coder', 'url': 'http://localhost:8003'}
            # get the recipient name
            recipient_name = new_message.get( "recipient" ).get( "name" )
            # get the recipient url
            recipient_url = new_message.get( "recipient" ).get( "url" )

            # Coder Agent
            if recipient_name == "coder":
                response = self.send_message( new_message, recipient_url )
                return response
            
            # Planner Agent
            elif recipient_name == "planner":
                response = self.send_message("planner", {"message": command[len("planner:"):].strip()})
                return response

            # Prompt Agent
            elif recipient_name == "prompt":
                response = self.send_message("prompt", {"message": command[len("prompt:"):].strip()})
                return response
            
            # Unknown Agent
            else:
                # Handle other commands or respond directly
                self.logger.info(f"Unknown command: {command}")
                return "Unknown command"
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"


def main():
    """
    Main entry point for the CollaboratorAgent.
    """
    agent_url = f"http://localhost:{PORT}"
    logger = ConsoleLogger()
    strategy_factory = RPCCommunicationStrategyFactory(port=PORT, logger=logger)

    collaborator_agent = CollaboratorAgent(
        agent_id="collaborator_agent",
        strategy_factory=strategy_factory,
        agent_url=agent_url,
        logger=logger
    )

    try:
        collaborator_agent.logger.info(f"CollaboratorAgent is starting on port {PORT}...")
        collaborator_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        collaborator_agent.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
