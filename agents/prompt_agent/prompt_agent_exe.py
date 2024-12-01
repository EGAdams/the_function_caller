# The Prompt Agent
# first Saturday
# @retry( wait=wait_random_exponential( multiplier=1, max=40 ), stop=stop_after_attempt( 3 ))
import sys
import json
from time import sleep
from openai import OpenAI
import xmlrpc.client

from func_map_init.file_system_mapped_functions import FileSystemMappedFunctions
from function_executor import function_executor
from message_factory import MessageFactory
from string_to_function.string_to_function import StringToFunction
from tool_manager import ToolManager

collaborator_url = "http://localhost:8001" # URL of the collaborator's RPC server
PORT = 8003
GPT_MODEL = "gpt-3.5-turbo-0125"
sys.path.append( '/home/adamsl/the_function_caller' )
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent

class PromptAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int, collaborator_url: str):
        super().__init__(agent_id, server_port)
        self.collaborator_url   = collaborator_url
        self.client             = OpenAI()  # Create the OpenAI client
        self.pretty_print       = PrettyPrint()
        message_factory         = MessageFactory()
        tool_manager            = ToolManager.ToolManager()
        fs_mapped_funcs         = FileSystemMappedFunctions.FileSystemMappedFunctions()
        function_map            = fs_mapped_funcs.get_function_map() # populate for file system tools
        string_to_function      = StringToFunction.StringToFunction( function_map )
        self.function_executor  = function_executor.FunctionExecutor( string_to_function )
        self.messages           = message_factory.create_initial_messages_object() # build the messages object.
        self.tools              = tool_manager.get_tool_schemas()                  # build the tools object array of schemas.

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
        self.messages.append( new_message )

        response = self.client.chat.completions.create(             # get the request from the model
            model=GPT_MODEL,                                        # Step 1: send the conversation 
            messages=self.messages,                                 # and available functions to the model
            tools=self.tools,
            tool_choice="auto" )                                    # auto is default, but we'll be explicit
        
        response_message = response.choices[ 0 ].message
        tool_calls = response_message.tool_calls
       
        if tool_calls:                                              # Step 2: check if the model wanted to call a function
            self.messages.append( response_message )                # extend conversation with assistant's reply
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads( tool_call.function.arguments )
                function_response = function_executor.execute_function( function_name, function_args ) #3: call func
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                ) # extend conversation with function response
            second_response = self.client.chat.completions.create(   # Step 4: send the info for each 
                model=GPT_MODEL,                                # function call and function response
                messages=self.messages,                              # to the model
            ) # get a new response from the model where it can see the function response
            return second_response.choices[ 0 ].message
        else:
            self.messages.append( response_message )                 # extend conversation with assistant's reply
            return response_message

def main():
    """
    Main entry point for the PromptAgent.
    """
    collaborator_url = "http://localhost:8001"
    prompt_agent = PromptAgent(agent_id="prompt_agent", server_port=PORT, collaborator_url=collaborator_url)
    
    try:
        prompt_agent.logger.info("PromptAgent is starting in port " + str( PORT ) + "...")
        prompt_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        prompt_agent.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
