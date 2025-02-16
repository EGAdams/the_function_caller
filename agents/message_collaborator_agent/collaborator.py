#
# https://platform.openai.com/assistants/asst_klrcTdNwmeEXJPRx2LT7CRJY
#
import sys, os, json
from openai import OpenAI
sys.path.append( os.path.expanduser( "~" ) + '/the_function_caller' )
from agents.agent_urls import AgentUrlProvider
from send_message_tool.send_message_tool import SendMessageTool
from commands.process_message_command.process_message_command import ProcessMessageCommand
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import RPCCommunicationStrategyFactory
from agents.base_agent.base_agent import BaseAgent
from agents.base_agent.base_agent import ConsoleLogger
PORT = 8001

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
            content="How can I assist with collaboration?" )
        self.register_command("process_message", ProcessMessageCommand(self))       # Register the message processing command
        self.send_message_tool = SendMessageTool( AgentUrlProvider.get_agent_urls()) # Create an instance of the send message tool just like we do
                                                                                    # when we initialize the file system mapped functions.

    def show_json(self, obj):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

    def process_message( self, new_message ):
        try:
            
            # find out who to send the message to if it is not for the collaborator agent
            # for now, just send it to the coder agent
            print ( "sending message to prompt agent for testing." )
            response = self.send_message( "prompt", new_message )
            print( "returning response: ", response )
            return response
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"

def main():
    agent_url = f"http://localhost:{PORT}"
    logger = ConsoleLogger()
    strategy_factory = RPCCommunicationStrategyFactory(port=PORT, logger=logger)
    collaborator_agent = CollaboratorAgent( agent_id="collaborator_agent", strategy_factory=strategy_factory,
                                            agent_url=agent_url, logger=logger )
    try:
        collaborator_agent.logger.info(f"CollaboratorAgent is starting on port {PORT}...")
        collaborator_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        collaborator_agent.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
