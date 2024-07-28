import json
import time
from time import sleep
from openai import OpenAI
GPT_MODEL = "gpt-3.5-turbo-0125"
from AssistantFactory import AssistantFactory
from ActionHandler import ActionHandler
# from termcolor import colored  

# def pretty_print( messages ):
#     print( "\n\n" )
#     print( "# Messages" )
#     for m in messages:
#         print( f"{ m.role }: { m.content[ 0 ].text.value }" )
#     print()
    
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
            print( colored( f"system: { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
        elif message.role == "user":
            print( colored( f"user: { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
        # elif message.role == "assistant" and message.get( "function_call" ):
        #     print( colored( f"assistant: {message['function_call']}\n", role_to_color[message.role]))
        elif message.role == "assistant": # and not message.get( "function_call" ):
            print( colored( f"assistant: { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
        elif message.role == "function":
            print( colored( f"function ({ message[ 'name' ]}): { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))

def show_json( obj ):
    json_obj = json.loads( obj.model_dump_json())
    pretty_json = json.dumps( json_obj, indent=4 )  # Pretty print JSON
    print( pretty_json )

assistantFactory = AssistantFactory()

# create an assistant asst_Zw3KYZUBFI9jZheRiVLkQAta MemGPT_Coder # assistant = assistantFactory.createAssistant( nameArg="MemGPT_Coder" )
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
    function_data = json.loads( function_json)
    
    # Extract the function name and parameters
    function_name = function_data.get( "function" )
    parameters = function_data.get( "parameters", {})
    
    # Match the function name to the actual function and execute it
    if function_name == "write_file":
        return write_file( parameters.get( "filename" ), parameters.get( "content" ))
    elif function_name == "read_file":
        return read_file( parameters.get( "filename" ))
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
            messages = client.beta.threads.messages.list( thread_id=thread.id )
            # handleActionRequired = HandleActionRequired( messages, available_functions, run )
            # return handleActionRequired.execute( thread.id ) # returns run for now...
            actionHandler = ActionHandler( messages, run )
            actionHandler.execute( thread.id ) # modifies run for now...
    
    print( f"Run { run.id } is { run.status }." )
    return run

run = wait_on_run( run, thread )
show_json( run )

messages = client.beta.threads.messages.list( thread_id=thread.id )
show_json( messages ) # display the assistant's response
print ( "\n" )

while ( True ):
    new_message = input( "Enter a message to send to the assistant: " ) # get message from user
   
    message = client.beta.threads.messages.create(                      # Add a message to a thread
        thread_id=thread.id,
        role="user",
        content=new_message )
   
    run = client.beta.threads.runs.create(                              # run the assistant
    thread_id=thread.id,
    assistant_id=assistant.id )
    run_steps = client.beta.threads.runs.steps.list(                    # get the run steps so that 
        thread_id=thread.id, run_id=run.id, order="asc" )               # we can look at them
    
    for step in run_steps.data:
        step_details = step.step_details                  
        print( json.dumps( show_json( step_details ), indent=4 ))       # look at them

    wait_on_run( run, thread ) 
    messages = client.beta.threads.messages.list( thread_id=thread.id ) # done waiting.  get messages..
    # reverse the order so that the most recent message is at the top of the list
    # Convert to list if it's not already one, assuming messages is iterable
    messages_list = list( messages )
    reversed_messages = messages_list[::-1] # Reverse the list
    pretty_print_conversation( reversed_messages )                      # print the conversation so far
