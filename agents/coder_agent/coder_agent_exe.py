# The Coder Agent
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_MGrsitU5ZvgY530WDBLK3ZaS
import sys
import json
from time import sleep
from openai import OpenAI
import xmlrpc.client
import os

# collaborator_url    = "http://localhost:8001" # URL of the collaborator's RPC server

PORT                = 8003
CHEAP_GPT_MODEL     = "gpt-3.5-turbo-0125"
GPT_MODEL           = "gpt-4o-mini"
sys.path.append( '/home/adamsl/the_function_caller' )
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self, agent_id: str, server_port: int, collaborator_url: str):
        super().__init__(agent_id, server_port)
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
            content="Make sure to write testable, modular, reuseable code for our project."
        )

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
            # Add the incoming message to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=new_message["message"]
            )

            # Start a run with the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for the run to complete
            self.run_spinner.spin(run, self.thread)

            # Fetch messages from the thread
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            messages_list = list(messages)
            reversed_messages = messages_list[::-1]
            response = reversed_messages[len(reversed_messages) - 1]

            # Extract the content from the response
            response_content = response.content[0].text.value
            return response_content

        except Exception as e:
            self.logger.error(f"Coder Agent Error processing message: {e}")
            return f"Error: {str(e)}"

def main():
    """
    Main entry point for the CoderAgent.
    """
    collaborator_url = "http://localhost:8001"
    coder_agent = CoderAgent(agent_id="coder_agent", server_port=PORT, collaborator_url=collaborator_url)
    
    try:
        coder_agent.logger.info("CoderAgent is starting in port " + str( PORT ) + "...")
        coder_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        coder_agent.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
