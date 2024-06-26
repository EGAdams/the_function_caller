import json
import time
from time import sleep
from openai import OpenAI
from AssistantFactory import AssistantFactory
from HandleActionRequired import HandleActionRequired

GPT_MODEL = "gpt-3.5-turbo-0125"

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
    """we use JSON objects to hold a name of a function and
    parameters that it will need to execute.  this function
    parses that JSON object to get the name of the function,
    then it calls the function with the parameters.
    
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
    while run.status == "queued" or run.status == "in_progress":    
        run = client.beta.threads.runs.retrieve(    # get the run using the
            thread_id=thread.id,                    # thread id and the run
            run_id=run.id,                          # id
        )
        time.sleep( 0.5 )
        print( "done sleeping.  checking for any action required..." )
        if run.status == "requires_action":
            print( "found action required.  sending the run for processing..." )
            available_functions = {         # create a dictionary of available
                "read_file": read_file,     # functions to be executed.  the
                "write_file": write_file    # har Object will need this below.
            }
            messages = client.beta.threads.messages.list( thread_id=thread.id ) # har next...
            handleActionRequired = HandleActionRequired( messages, available_functions, run )
            return handleActionRequired.execute( thread.id ) # returns run for now...
    
    print(f"Run {run.id} is {run.status}.")
    return run

run = wait_on_run( run, thread ) # we will be back...
show_json( run )

messages = client.beta.threads.messages.list(thread_id=thread.id)
show_json(messages) # display the assistant's response
print ( "\n" )

def pretty_print(messages):
    print( "\n\n")
    print( "# Messages" )
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()
    
while ( True ):
    new_message = input( "Enter a message to send to the assistant: " )
    message = client.beta.threads.messages.create(  # Add a message
        thread_id=thread.id,                        # to the thread
        role="user",
        content=new_message )
   
    run = client.beta.threads.runs.create( # create a run
    thread_id=thread.id,                   # that we will
    assistant_id=assistant.id )            # be waiting on.
    
    run_steps = client.beta.threads.runs.steps.list(        # get the run steps so
        thread_id=thread.id, run_id=run.id, order="asc" )   # we can look at them
    
    for step in run_steps.data:
        step_details = step.step_details                    # look at them
        print(json.dumps(show_json(step_details), indent=4))

    wait_on_run( run, thread )  # we will be back...
                                # there won't be any messages
                                # until the run is finished.
      
    messages = client.beta.threads.messages.list( thread_id=thread.id ) # now we got em.
    messages_list = list(messages)           
    reversed_messages = messages_list[::-1] # Here we reverse the messages to put
    pretty_print( reversed_messages )       # them in an order that makes sense.
