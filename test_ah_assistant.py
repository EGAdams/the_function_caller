import json
import time
from time import sleep
from openai import OpenAI
GPT_MODEL = "gpt-3.5-turbo-0125"
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
    
def show_json( obj ):
    json_obj = json.loads( obj.model_dump_json())
    pretty_json = json.dumps( json_obj, indent=4 )  # Pretty print JSON
    print( pretty_json )

pretty_print     = PrettyPrint()
assistantFactory = AssistantFactory()
assistant        =  assistantFactory.getExistingAssistant( assistant_id="asst_Zw3KYZUBFI9jZheRiVLkQAta" )
client           = OpenAI()                              # create the client
run_spinner      = RunSpinner( client )                  # create the wait loop Object
thread           = client.beta.threads.create()          # create a thread
message          = client.beta.threads.messages.create(  # Add a message to a thread
    thread_id=thread.id,
    role="user",
    content="What do you know about attached files that you have?" )

run = client.beta.threads.runs.create( thread_id=thread.id,assistant_id=assistant.id ) # Create the run
run = run_spinner.spin( run, thread )                    # wait for the initial run to finish...
show_json( run )

messages = client.beta.threads.messages.list( thread_id=thread.id )
show_json( messages )                                    # display the assistant's response
print ( "\n" )

while ( True ):
    new_message = input( "Enter a message to send to the assistant: " ) # get message from user
    message = client.beta.threads.messages.create(                      # Add a message to a thread
        thread_id=thread.id,
        role="user",
        content=new_message )                                           # then run the assistant...
    run       = client.beta.threads.runs.create( thread_id=thread.id, assistant_id=assistant.id )
    run_steps = client.beta.threads.runs.steps.list(                    # get the run steps so that 
        thread_id=thread.id, run_id=run.id, order="asc" )               # we can look at them
    
    for step in run_steps.data:
        step_details = step.step_details                  
        print( json.dumps( show_json( step_details ), indent=4 ))       # look at them

    run_spinner.spin( run, thread )                                     # run is done.  dropped into bit bucket.
    messages            = client.beta.threads.messages.list( thread_id=thread.id ) # done waiting.  get messages...
    messages_list       = list( messages )
    reversed_messages   = messages_list[::-1]                           # Reverse the list
    pretty_print.execute( reversed_messages )                           # print the conversation so far
