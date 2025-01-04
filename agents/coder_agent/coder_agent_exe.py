# The Coder Agent
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_MGrsitU5ZvgY530WDBLK3ZaS
import sys
import json
from time import sleep
from openai import OpenAI
from agents.base_agent.base_agent import BaseAgent, ICommand
import xmlrpc.client
import os

PORT                = 8003
CHEAP_GPT_MODEL     = "gpt-3.5-turbo-0125"
GPT_MODEL           = "gpt-4o-mini"
sys.path.append( '/home/adamsl/the_function_caller' )
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent
from agents.base_agent.base_agent import RPCCommunicationStrategyFactory
from agents.base_agent.base_agent import ConsoleLogger

class ProcessMessageCommand(ICommand):
    def __init__(self, coder_agent):
        self.coder_agent = coder_agent

    def execute(self, message: dict) -> dict:
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        try:
            content = message.get("message", "")
            # Add the incoming message to the thread
            message = self.coder_agent.client.beta.threads.messages.create(
                thread_id=self.coder_agent.thread.id,
                role="user",
                content=content
            )

            # Start a run with the assistant
            run = self.coder_agent.client.beta.threads.runs.create(
                thread_id=self.coder_agent.thread.id,
                assistant_id=self.coder_agent.assistant.id
            )

            # Wait for the run to complete
            self.coder_agent.run_spinner.spin(run, self.coder_agent.thread)

            # Fetch messages from the thread
            messages = self.coder_agent.client.beta.threads.messages.list(thread_id=self.coder_agent.thread.id)
            messages_list = list(messages)
            response = messages_list[-1]  # Get the last message as the response

            # Extract the content from the response
            response_content = response.content[0].text.value
            return {"status": "success", "response": response_content}

        except Exception as e:
            self.coder_agent.logger.error(f"CoderAgent error processing message: {e}")
            return {"status": "error", "message": str(e)}


class CoderAgent(BaseAgent):
    def __init__(self, agent_id: str, strategy_factory, collaborator_url: str, logger=None):
        super().__init__(agent_id, strategy_factory, logger or ConsoleLogger())
        self.collaborator_url = collaborator_url
        self.client = OpenAI()  # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()
        self.assistant = self.assistant_factory.getExistingAssistant(assistant_id="asst_MGrsitU5ZvgY530WDBLK3ZaS")
        self.run_spinner = RunSpinner(self.client)
        self.thread = self.client.beta.threads.create()  # Create a thread
        self.message = self.client.beta.threads.messages.create(  # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="Make sure to write testable, modular, reusable code for our project."
        )

        # Register the command to process incoming messages
        self.register_command("process_message", ProcessMessageCommand(self))

    def show_json(self, obj):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)


def main():
    """
    Main entry point for the CoderAgent.
    """
    collaborator_url = "http://localhost:8001"
    logger = ConsoleLogger()
    strategy_factory = RPCCommunicationStrategyFactory(port=PORT, logger=logger)

    coder_agent = CoderAgent(
        agent_id="coder_agent",
        strategy_factory=strategy_factory,
        collaborator_url=collaborator_url,
        logger=logger
    )

    try:
        coder_agent.logger.info(f"CoderAgent is starting on port {PORT}...")
        coder_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        coder_agent.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
