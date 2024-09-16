#
# main - runs the chat completion with functions
#
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
GPT_MODEL = "gpt-3.5-turbo-0125"

client = OpenAI()
from message_factory import MessageFactory
import tool_manager.ToolManager as ToolManager
import function_map.function_map as FunctionMap # to construct STF object below
import string_to_function.string_to_function as StringToFunction # for func exec
import function_executor.function_executor as function_executor
import func_map_init.file_system_mapped_functions as FileSystemMappedFunctions
if __name__ == "__main__":
    message_factory     = MessageFactory()
    tool_manager        = ToolManager.ToolManager()
    fs_mapped_funcs     = FileSystemMappedFunctions.FileSystemMappedFunctions()
    function_map        = fs_mapped_funcs.get_function_map() # populate for file system tools
    string_to_function  = StringToFunction.StringToFunction( function_map )
    function_executor   = function_executor.FunctionExecutor( string_to_function )
    
    @retry( wait=wait_random_exponential( multiplier=1, max=40 ), stop=stop_after_attempt( 3 ))
    def chat_completion_request( messages, tools=None, tool_choice=None, model=GPT_MODEL ):
        try:                                               
            response = client.chat.completions.create(      # define the chat 
                model=model,                                # completion request.
                messages=messages,
                tools=tools,
                tool_choice=tool_choice )
            
            return response
        except Exception as e:
            print( "Unable to generate ChatCompletion response" )
            print( f"Exception: {e}" )
            return e         
            
    messages = message_factory.create_initial_messages_object() # build the messages object.
    tools    = tool_manager.get_tool_schemas()                  # build the tools object array of schemas.
   
    def run_conversation():
        response = client.chat.completions.create(              # get the request from the model
            model=GPT_MODEL,                                    # Step 1: send the conversation 
            messages=messages,                                  # and available functions to the model
            tools=tools,
            tool_choice="auto" )                                # auto is default, but we'll be explicit
        
        response_message = response.choices[ 0 ].message
        tool_calls = response_message.tool_calls
       
        if tool_calls:                              # Step 2: check if the model wanted to call a function
            messages.append( response_message )     # extend conversation with assistant's reply
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads( tool_call.function.arguments )
                function_response = function_executor.execute_function( function_name, function_args ) #3: call func
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                ) # extend conversation with function response
            second_response = client.chat.completions.create(   # Step 4: send the info for each 
                model=GPT_MODEL,                                # function call and function response
                messages=messages,                              # to the model
            ) # get a new response from the model where it can see the function response
            return second_response.choices[ 0 ].message
        else:
            messages.append( response_message )                 # extend conversation with assistant's reply
            return response_message             
        
    messages.append( run_conversation())
    
    while ( True ):
        user_input = input( "Enter your message: " )
        if ( user_input == "q" ):
            break
        messages.append({ "role": "user",   "content": user_input  })
        conversation_run = run_conversation()
        print ( "\n" )
        print( conversation_run.content )
    