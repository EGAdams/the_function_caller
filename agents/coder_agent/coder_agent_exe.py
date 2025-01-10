# The Coder Agent
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_MGrsitU5ZvgY530WDBLK3ZaS
import sys, os
import json
import xmlrpc.client
from time import sleep
from openai import OpenAI

import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
from commands.process_message_command.process_message_command import ProcessMessageCommand

PORT                = 8003
CHEAP_GPT_MODEL     = "gpt-3.5-turbo-0125"
GPT_MODEL           = "gpt-4o-mini"

home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )

from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent
from agents.base_agent.base_agent import RPCCommunicationStrategyFactory
from agents.base_agent.base_agent import ConsoleLogger

class CoderAgent( BaseAgent ):
    def __init__( self, agent_id: str, strategy_factory, agent_url: str, logger=None ):
        super().__init__( agent_id, strategy_factory, logger or ConsoleLogger())
        self.url                = agent_url
        self.client             = OpenAI()                                  # Create the OpenAI client
        self.pretty_print       = PrettyPrint()
        self.assistant_factory  = AssistantFactory()
        self.assistant          = self.assistant_factory.getExistingAssistant( assistant_id="asst_MGrsitU5ZvgY530WDBLK3ZaS" )
        self.run_spinner        = RunSpinner( self.client )
        self.thread             = self.client.beta.threads.create()         # Create a thread
        self.message            = self.client.beta.threads.messages.create( # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="Make sure to write testable, modular, reusable code for our project." )
        
        self.register_command( "process_message", ProcessMessageCommand( self )) # Register the command to process incoming messages

    def show_json( self, obj ):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads( obj.model_dump_json())
        pretty_json = json.dumps( json_obj, indent=4 )
        print( pretty_json )


def main():
    """
    Main entry point for the CoderAgent.
    """
    agent_url = "http://localhost:" + str( PORT )
    logger = ConsoleLogger()
    strategy_factory = RPCCommunicationStrategyFactory( port=PORT, logger=logger )

    coder_agent = CoderAgent(
        agent_id="coder_agent",
        strategy_factory=strategy_factory,
        agent_url=agent_url,
        logger=logger )

    try:
        coder_agent.logger.info( f"CoderAgent is starting on port {PORT}..." )
        coder_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        coder_agent.logger.info( "Shutting down..." )

if __name__ == "__main__":
    main()
