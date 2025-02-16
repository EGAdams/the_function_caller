# The Prompt Agent
# first Saturday
# @retry( wait=wait_random_exponential( multiplier=1, max=40 ), stop=stop_after_attempt( 3 ))
import sys, os, json
from openai import OpenAI
sys.path.append( os.path.expanduser( "~" ) + '/the_function_caller' )
from commands.process_with_oai_completion.process_with_oai_completion import ProcessWithOaiCompletion
from func_map_init.file_system_mapped_functions import FileSystemMappedFunctions
from tool_manager.ToolManager import ToolManager
from function_executor import function_executor
from message_factory import MessageFactory
from pretty_print.pretty_print import PrettyPrint
from string_to_function.string_to_function import StringToFunction
from agents.base_agent.base_agent import BaseAgent, ConsoleLogger, RPCCommunicationStrategyFactory
PORT = 8004

class PromptAgent( BaseAgent ):
    def __init__( self, agent_id: str, strategy_factory, agent_url: str, logger=None ):
        print("Initializing PromptAgent...")
        super().__init__( agent_id, strategy_factory, logger or ConsoleLogger())
        self.register_command( "process_message", ProcessWithOaiCompletion( self )) # Register the command to process incoming
                                                                                    # messages. 

    def show_json(self, obj):
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

def main():
    agent_url           = "http://localhost:" + str( PORT )
    logger              = ConsoleLogger()
    strategy_factory    = RPCCommunicationStrategyFactory( port=PORT, logger=logger )
    prompt_agent        = PromptAgent( agent_id="prompt", strategy_factory=strategy_factory, agent_url=agent_url, logger=logger )
    try:
        prompt_agent.logger.info("PromptAgent is starting in port " + str( PORT ) + "...")
        print(f"Starting XML-RPC server on port {PORT}")
        prompt_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
        prompt_agent.logger.info("Shutting down...")
        print("=== PromptAgent shutdown complete ===")

if __name__ == "__main__":
    main()