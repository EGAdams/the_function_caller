# Who you are
You are a world-class Python Developer and a seasoned user of the Gang of Four Design patterns and the many Principles of Software Design that the designs help enforce.
You are my excellent Teacher and mentor
You are also an expert at simplifying problems by breaking them up into smaller, more manageable parts.

# Some background information
I am trying to learn how OpenAI uses function calling.  I need a plan to learn how to use the OpenAI Function Calling API.  I started giving the model read and write capabilities and I am trying to figure out how to use the API.  I have been able to get the model to write to a file and read from my local hard drive with the Python code that I am about to show you.  I want to incrementally build on this design.  Maybe add a directory searching tool, a change directory tool, and then maybe a tool that will be able to search the web using Google's SERP API and Pupppeteer.  I'm trying to give you the whole picture of the challenges that I am facing so that you can help me more effectively.

# Source Code for you to analyze
```python
import json
import time
from time import sleep
from openai import OpenAI
GPT_MODEL = "gpt-3.5-turbo-0125"
from AssistantFactory import AssistantFactory
from HandleActionRequired import HandleActionRequired

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
    
    # morph the file name since the assistant seems to be looking in it's sandbox
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
    while run.status == "queued" or run.status == "in_progress":
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
            }
            messages = client.beta.threads.messages.list( thread_id=thread.id )
            handleActionRequired = HandleActionRequired( messages, available_functions, run )
            return handleActionRequired.execute( thread.id ) # returns run for now...
    
    print(f"Run {run.id} is {run.status}.")
    return run

run = wait_on_run( run, thread )
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
    # Add a message to a thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=new_message )
   
    run = client.beta.threads.runs.create( # create a run
    thread_id=thread.id,                   # that we will
    assistant_id=assistant.id )            # be waiting on.
    
    # get the run steps so that we can look at them
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id, run_id=run.id, order="asc" )
    
    for step in run_steps.data:
        step_details = step.step_details                        # look at them
        print(json.dumps(show_json(step_details), indent=4))

    wait_on_run( run, thread )   # we will be back...
    messages = client.beta.threads.messages.list( thread_id=thread.id )
    # reverse the order so that the most recent message is at the top of the list
    # Convert to list if it's not already one, assuming messages is iterable
    messages_list = list(messages)
    reversed_messages = messages_list[::-1] # Reverse the list
    pretty_print( reversed_messages )

# EOF
```
# Your Task
Kindly explain to me what you think about the code above.  Do we need to use design patterns yet, or would that be overkill at this point?  What incremental thing should we build next?  Do you see anywhere in the code where the responsibilities should be broken up into different objects?  Can you make simplifications anywhere?     Answer with 25 words or less, what do you think we should do next?
