import sys
import json
from time import sleep
from openai import OpenAI

PORT = 8001
GPT_MODEL = "gpt-3.5-turbo-0125"
sys.path.append('/home/adamsl/the_function_caller')
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent

class CollaboratorAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int):
        super().__init__(agent_id, server_port)
        self.client = OpenAI()                                      # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()                 # This is an OpenAI Assistant
        self.assistant = self.assistant_factory.getExistingAssistant( assistant_id="asst_lRPtbKUVMJPAXt0RttAU8EHg" )
        self.run_spinner = RunSpinner(self.client)                  # this "absorbs" the messages and/or tool calls
        self.thread = self.client.beta.threads.create()             # Create a thread so that we can use the id
        self.message = self.client.beta.threads.messages.create(    # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="How can I assist with collaboration?"
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

        note Error: Failed to send message: <Fault 1: "<class 'TypeError'>:string indices must be integers"> means
        that new_message["message"] is not a string, but a dict.
        """
        print( f"Collaborator Agent received message: {new_message}" )
        # try:
        #     message = self.client.beta.threads.messages.create(
        #         self.thread.id,
        #         role="user",
        #         content=new_message["message"] 
        #     )

        #     print ( "Start a run with the assistant" )
        #     run = self.client.beta.threads.runs.create(
        #         thread_id=self.thread.id,
        #         assistant_id=self.assistant.id
        #     )

        #     print( "Wait for the run to complete..." )
        #     self.run_spinner.spin(run, self.thread)

        #     print( "Fetch messages from the thread..." )
        #     messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        #     messages_list = list(messages)
        #     reversed_messages = messages_list[::-1]
        #     response = reversed_messages[len(reversed_messages) - 1]
        #     response_content = response.content[0].text.value           # Extract the content from the response
        #     return response_content

        # except Exception as e:
        #     self.logger.error(f"Collaborator Error processing message: {e}")
        #     print (f"Collaborator Error processing message: {e}")
        #     return f"Error: {str(e)}"

def main():
    """
    Main entry point for the CollaboratorAgent.
    """
    # Define RPC URLs for other agents
    agents_urls = {
        "collaborator"  : "http://localhost:8001",
        "planner"       : "http://localhost:8002",
        "coder"         : "http://localhost:8003",
        "prompt"        : "http://localhost:8004",
    }

    try:
        collaborator_agent.logger.info("CollaboratorAgent is starting on port " + str(PORT) + "...")
        collaborator_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        collaborator_agent.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
