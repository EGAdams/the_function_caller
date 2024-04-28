# Who you are
You are a world-class Python Developer and a seasoned user of the Gang of Four Principles of Software Design.
You are my excellent Teacher and mentor
You are also an expert at simplifying problems by breaking them up into smaller, more manageable parts.

# Some background information
I am trying to build a code-writing Agent.  The Agent will need tools to help me with the following:
- Changing directories
- Moving files
- Searching the web
- Searching the web using Google's SERP API
- Searching the web using puppeteer
- Searching the web using the Google Search API
- Copying files
- Deleting files
- Creating Databases
- Using pExpect to login to a remote server
- Using pExpect install software
- Debug Code
- Write the code for the Mermaid class, sequence, and mind map diagrams.

To build an Agent with all of these capabilities, it is going to need to be able to call functions.  OpenAI has large language models that are trained to recognize when to call functions and how to read the schema of the function so that it can piece together a meaningful function with arguments that will presumably retrieve some type of information needed to solve the problem at hand.  That is why I am trying to learn how OpenAI uses function calling.  I need a plan to learn how to use the OpenAI Function Calling API.  I started giving the model read and write capabilities.  I have been able to get the model to write to a file and also read a file from my local hard drive with the Python code that I am about to show you.  I want to incrementally build on this design.  Maybe add a directory searching tool, a change directory tool, and then maybe a tool that will be able to search the web using Google's SERP API and Pupppeteer.  I don't want you to do any of those things right now, I'm just trying to give you the whole picture of the challenges that I am facing so that you can help me more effectively.

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
# Your task
Before we build the next set of tools, I want us to take a break and start breaking up the preceeding code into many meaningful objects that we can reuse.
We are going to follow the SOLID Principles of software design.  In adherence to the Single Responsibility Principle, the code above should cut way down on the amount of responsibilities that it has.  We need to break it up into smaller pieces.  For starters, we should probably make seperate objects for reading and writing files.  This is probably a huge violation of the SRP.  As for the "Open/Closed Principle", I need you to help me find out where in the code I have provided that there are violations of this Principle.  I want you to ask yourself questions like "Is the code Open for Extention?  Is the code Closed for modification?" and if you find that the code is not extendable, show me how you would make it extendable.  If you find code that is not closed for modification, show me how you would make it closed for modification.  I want you to find the violations and fix them.  As you are fixing the violations using your vast experience in designing software adhering to the Gang of Four Principles, I want you to make sure that you are adhering to the Liskov
 Substitution Principle by making sure the when you make a subclass, that it should always be substitutable for its parent class.  

Now really think about the Gang of Four Patterns and how they help us avoid making SOLID violations while you take another look at the code.

Here is the FileReader class that we have now:
```python
class FileWriter:
    def write(self, filename, content):
        # Implementation for writing to a file
        pass
```
Please implement it to use in the WriteFileCommand class that you just wrote.

I need you to make a set of instructions for another AI to start building the project that we have been working on.  Give step-by-step instructions as to what directories to make where we are going to put the source files.  Use a linux tree output to show the structure of our project.  The other AI has the ability to create the directories and files.

If there are any other tools that you think that we need to build this project, please let me know.





notes:
S.O.L.I.D. stands for:
Single Responsibility Principle - A class should have one, and only one, reason to change.
Open/Closed Principle - A class should be open for extension, but closed for modification.
Liskov Substitution Principle - A subclass should be substitutable for its parent class.

Interface Segregation Principle - A client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use.

Dependency Inversion Principle - Entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions.




Open/Closed Principle
Liskov Substitution Principle
Interface Segregation Principle
Dependency Inversion Principle