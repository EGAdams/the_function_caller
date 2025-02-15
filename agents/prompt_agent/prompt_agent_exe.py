# The Prompt Agent
# first Saturday
# @retry( wait=wait_random_exponential( multiplier=1, max=40 ), stop=stop_after_attempt( 3 ))
import sys, os, json
from openai import OpenAI
sys.path.append( os.path.expanduser( "~" ) + '/the_function_caller' )
from func_map_init.file_system_mapped_functions import FileSystemMappedFunctions
from tool_manager.ToolManager import ToolManager
from function_executor import function_executor
from message_factory import MessageFactory
from pretty_print.pretty_print import PrettyPrint
from string_to_function.string_to_function import StringToFunction
from agents.base_agent.base_agent import BaseAgent
PORT = 8004
GPT_MODEL = "gpt-4o-mini"

class PromptAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int, collaborator_url: str):
        print("Initializing PromptAgent...")
        super().__init__(agent_id, server_port)
        self.collaborator_url   = collaborator_url
        self.client             = OpenAI()  # Create the OpenAI client
        self.pretty_print       = PrettyPrint()
        message_factory         = MessageFactory()
        tool_manager            = ToolManager()
        fs_mapped_funcs         = FileSystemMappedFunctions()
        function_map            = fs_mapped_funcs.get_function_map() # populate for file system tools
        string_to_function      = StringToFunction( function_map )
        self.function_executor  = function_executor.FunctionExecutor( string_to_function )
        self.messages           = message_factory.create_initial_messages_object() # build the messages object.
        self.tools              = tool_manager.get_tool_schemas()                  # build the tools object array of schemas.
        print("PromptAgent initialization complete")
        print(f"Number of tools loaded: {len(self.tools)}")

    def show_json(self, obj):
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

    def process_message(self, new_message: dict):
        print(f"\nProcessing new message: {new_message['role']}")
        self.messages.append( new_message )
        print("Sending request to OpenAI...")

        response = self.client.chat.completions.create(             # get the request from the model
            model=GPT_MODEL,                                        # Step 1: send the conversation 
            messages=self.messages,                                 # and available functions to the model
            tools=self.tools,
            tool_choice="auto" )                                    # auto is default, but we'll be explicit
        
        print("Received response from OpenAI")
        response_message = response.choices[ 0 ].message
        tool_calls = response_message.tool_calls
       
        if tool_calls:              # Step 2: check if the model wanted to call one or more functions
            print(f"Model requested {len(tool_calls)} tool calls")
            self.messages.append( response_message )    # extend conversation with assistant's reply
            for tool_call in tool_calls:                # call all of the tools in tool_calls...
                function_name = tool_call.function.name
                function_args = json.loads( tool_call.function.arguments )
                print(f"Executing function: {function_name}")
                print(f"With arguments: {function_args}")
                function_response = self.function_executor.execute_function( function_name, function_args ) #3: call function
                print(f"Function response received: {function_response[:100]}...")  # Print first 100 chars
                self.messages.append(        # add the result of each tool call to the Prompt Agent's messages
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                ) # extend conversation with function response
            print("Sending second request to OpenAI...")
            second_response = self.client.chat.completions.create(   # Step 4: send the info for all 
                model=GPT_MODEL,                                     # function calls and function responses
                messages=self.messages,                              # to the model.
            )                                                        # get a new response from the model where 
                                                                     # since it has seen the function responses
            print("Received second response from OpenAI")
            return second_response.choices[ 0 ].message
        else:
            print("No tool calls requested by the model")
            self.messages.append( response_message )                 # extend conversation with assistant's reply
            return response_message

def main():
    collaborator_url = "http://localhost:8001"
    prompt_agent = PromptAgent(agent_id="prompt_agent", server_port=PORT, collaborator_url=collaborator_url)
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