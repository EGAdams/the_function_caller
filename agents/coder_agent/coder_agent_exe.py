#
# The Planner Agent
#
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_MGrsitU5ZvgY530WDBLK3ZaS
#
import sys
import json
from time import sleep
from openai import OpenAI
import xmlrpc.client

# URL of the collaborator's RPC server
collaborator_url = "http://localhost:8001"
PORT = 8003
GPT_MODEL = "gpt-3.5-turbo-0125"
sys.path.append( '/home/adamsl/the_function_caller' )
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
            content="Make sure to write good code for our project."
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
            # print(response.role)
            # self.pretty_print.execute(response)
            # Send the message as a command to the collaborator
            # self.send_message( {"command": command_packaged_message }, collaborator_url )
            with xmlrpc.client.ServerProxy( self.collaborator_url ) as proxy:      
                # Send the message as a command to the collaborator
                command_packaged_message = { "command": response.content[0].text.value }
                try:
                    # invoke the recieving agent's receive_message method `agent.receive_message(message)`  
                    print ( proxy.receive_message( command_packaged_message )) 
                    print(f"Message sent to collaborator: {message}")
                except Exception as e:
                    print(f"Failed to send message: {e}")

            # return response
            # return self.pretty_print.execute( response )
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
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
