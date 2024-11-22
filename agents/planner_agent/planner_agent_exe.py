#
# The Planner Agent
#
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_OqWn6Ek5CyYlWUrYJYyhpNQh
#
import sys
import json
from time import sleep
from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo-0125"
sys.path.append( '/home/adamsl/the_function_caller' )
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent

class PlannerAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int):
        super().__init__(agent_id, server_port)
        self.client = OpenAI()  # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()
        self.assistant = self.assistant_factory.getExistingAssistant(assistant_id="asst_OqWn6Ek5CyYlWUrYJYyhpNQh")
        self.run_spinner = RunSpinner(self.client)
        self.thread = self.client.beta.threads.create()  # Create a thread
        self.message = self.client.beta.threads.messages.create(  # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="What is on the agenda for today?"
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

            # Return the content of the last message
            # Get the last message from reversed messages
            response = reversed_messages[len(reversed_messages) - 1]
            print(response.role)
            self.pretty_print.execute(response)
            return response
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"


def main():
    """
    Main entry point for the PlannerAgent.
    """
    planner_agent = PlannerAgent(agent_id="planner_agent", server_port=8002)

    try:
        planner_agent.logger.info("PlannerAgent is starting...")
        planner_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        planner_agent.logger.info("Shutting down...")


if __name__ == "__main__":
    main()
