import json
import time
from time import sleep
from openai import OpenAI
GPT_MODEL = "gpt-3.5-turbo-0125"
from AssistantFactory import AssistantFactory
from ActionHandler import ActionHandler
from termcolor import colored  

def pretty_print(messages):
    print( "\n\n")
    print( "# Messages" )
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()
    
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
        if message.role == "system":
            print(colored(f"system: { message.content[0].text.value }\n", role_to_color[message.role]))
        elif message.role == "user":
            print(colored(f"user: { message.content[0].text.value }\n", role_to_color[message.role]))
        # elif message.role == "assistant" and message.get("function_call"):
        #     print(colored(f"assistant: {message['function_call']}\n", role_to_color[message.role]))
        elif message.role == "assistant": # and not message.get("function_call"):
            print(colored(f"assistant: { message.content[0].text.value }\n", role_to_color[message.role]))
        elif message.role == "function":
            print(colored(f"function ({message['name']}): { message.content[0].text.value }\n", role_to_color[message.role]))

def show_json(obj):
    json_obj = json.loads(obj.model_dump_json())
    pretty_json = json.dumps(json_obj, indent=4)  # Pretty print JSON
    print( pretty_json )

def write_file( filename, content ):  # write to hard drive
    """Writes content to a specified file.
    
    Args:
        filename (str): The name of the file to write to.
        content (str): The content to write to the file.
    """
    with open( filename, 'w' ) as file:
        file.write( content )
    return "File written successfully."

def read_file( filename ): # read from hard drive
    """Reads content from a specified file.
    
    Args:
        filename (str): The name of the file to read from.
    
    Returns:
        str: The content of the file.
    """
    
    # morph the file name since the assistant seems to be looking at it's sandbox
    filename = filename.replace( '/mnt/data/', '' )
    with open(filename, 'r') as file:
        return file.read()

assistantFactory = AssistantFactory()

# create an assistant asst_Zw3KYZUBFI9jZheRiVLkQAta MemGPT_Coder
# assistant = assistantFactory.createAssistant( nameArg="MemGPT_Coder" )
assistant =  assistantFactory.getExistingAssistant( assistant_id="asst_Zw3KYZUBFI9jZheRiVLkQAta" )

# create a thread
client = OpenAI()
thread = client.beta.threads.create()

# Add a message to a thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What do you know about attached files that you have?"
)

# Create the run
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

def execute_function( function_json ):
    """Parses a JSON object to execute a function based on the name and parameters.
    
    Args:
        function_json (str): A JSON string containing the function name and parameters.
        
    Returns:
        str: The result of the function execution.
    """
    
    # Parse the JSON string into a Python dictionary
    function_data = json.loads(function_json)
    
    # Extract the function name and parameters
    function_name = function_data.get("function")
    parameters = function_data.get("parameters", {})
    
    # Match the function name to the actual function and execute it
    if function_name == "write_file":
        return write_file(parameters.get("filename"), parameters.get("content"))
    elif function_name == "read_file":
        return read_file(parameters.get("filename"))
    else:
        return "Function not recognized."

def wait_on_run( run, thread ):
    print ( "entering while.  run status is: " + run.status )
    while run.status == "queued" or \
          run.status == "in_progress" or \
          run.status == "requires_action":
              
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep( 0.5 )
        print( "done sleeping.  checking for any action required..." )
        if run.status == "requires_action":
            print( "found action required.  sending the run for processing..." )
            available_functions = {
                "read_file": read_file,
                "write_file": write_file
            }  # only one function in this example, but you can have multiple
            messages = client.beta.threads.messages.list( thread_id=thread.id )
            # handleActionRequired = HandleActionRequired( messages, available_functions, run )
            # return handleActionRequired.execute( thread.id ) # returns run for now...
            actionHandler = ActionHandler( messages, available_functions, run )
            actionHandler.execute( thread.id ) # modifies run for now...
    
    print(f"Run {run.id} is {run.status}.")
    return run

run = wait_on_run( run, thread )
show_json( run )

messages = client.beta.threads.messages.list(thread_id=thread.id)
show_json(messages) # display the assistant's response
print ( "\n" )

while ( True ):
    new_message = input( "Enter a message to send to the assistant: " )
    # Add a message to a thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=new_message )
   
    run = client.beta.threads.runs.create( # run the assistant
    thread_id=thread.id,
    assistant_id=assistant.id )
    
    # get the run steps so that we can look at them
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id, run_id=run.id, order="asc" )
    
    for step in run_steps.data:
        step_details = step.step_details                        # look at them
        print( json.dumps(show_json( step_details ), indent=4 ))

    wait_on_run( run, thread ) 
    messages = client.beta.threads.messages.list( thread_id=thread.id )
    # reverse the order so that the most recent message is at the top of the list
    # Convert to list if it's not already one, assuming messages is iterable
    messages_list = list(messages)
    reversed_messages = messages_list[::-1] # Reverse the list
    # pretty_print( reversed_messages )
    pretty_print_conversation( reversed_messages )
