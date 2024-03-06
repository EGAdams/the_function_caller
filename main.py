#
# main - runs the chat completion with functions
#
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored  
GPT_MODEL = "gpt-3.5-turbo-0125"

client = OpenAI()
import MessageManager
import ToolManager

if __name__ == "__main__":
    message_manager = MessageManager.MessageManager()
    tool_manager = ToolManager.ToolManager()
    
    #
    # define the chat completion request
    #
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e
    #
    # Define the pretty print conversation
    #
    def pretty_print_conversation( messages ):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta" }
    
        for message in messages:
            if message == None:
                continue
            if message["role"] == "system":
                print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
            elif message["role"] == "user":
                print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
            elif message["role"] == "assistant" and message.get("function_call"):
                print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
            elif message["role"] == "assistant" and not message.get("function_call"):
                print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
            elif message["role"] == "function":
                print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))
                
    #
    # write to hard drive
    #
    def write_file(filename, content):
        """Writes content to a specified file.
        
        Args:
            filename (str): The name of the file to write to.
            content (str): The content to write to the file.
        """
        with open(filename, 'w') as file:
            file.write(content)
        return "File written successfully."

    #
    # read from hard drive
    #
    def read_file(filename):
        """Reads content from a specified file.
        
        Args:
            filename (str): The name of the file to read from.
        
        Returns:
            str: The content of the file.
        """
        with open(filename, 'r') as file:
            return file.read()
            
    #
    # build the messages object
    #
    messages = message_manager.create_initial_messages_object()
    
    #
    # build the tools object
    #
    tools = tool_manager.get_tools()
    
    #
    # get the request from the model
    #
    def run_conversation():
        # Step 1: send the conversation and available functions to the model
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "read_file": read_file,
                "write_file": write_file,
            }  # only one function in this example, but you can have multiple
            messages.append(response_message)  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = ""
                if ( function_name == "write_file" ):
                    function_response = function_to_call(
                        filename=function_args.get("filename"),
                        content=function_args.get("content"))
                if( function_name == "read_file" ):
                    function_response = function_to_call( filename=function_args.get( "filename" ))
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            return second_response.choices[0].message
        else:
            return response_message
        
    messages.append( run_conversation())
    
    while ( True ):
        user_input = input("Enter your message: ")
        if ( user_input == "q" ):
            break
        messages.append({ "role": "user",   "content": user_input  })
        conversation_run = run_conversation()
        print ( "\n" )
        print( conversation_run.content )
    
    
    
    
    