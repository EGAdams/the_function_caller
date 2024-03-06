#
#
#
import json
from time import sleep
from openai import OpenAI
GPT_MODEL = "gpt-3.5-turbo-0125"
from AssistantFactory import AssistantFactory

def show_json(obj):
    json_obj = json.loads(obj.model_dump_json())
    pretty_json = json.dumps(json_obj, indent=4)  # Pretty print JSON
    print( pretty_json )

# create an assistant asst_Zw3KYZUBFI9jZheRiVLkQAta MemGPT_Coder
assistantFactory = AssistantFactory()

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

# run the assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

# check the run status
import time

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
        print( "done sleeping.")
    print(f"Run {run.id} is {run.status}.")
    return run

run = wait_on_run(run, thread)
show_json(run)


# display the assistant's response
messages = client.beta.threads.messages.list(thread_id=thread.id)
show_json(messages)
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

    # run the assistant
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    )

    wait_on_run(run, thread)

    # display the assistant's response.
    
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    
    # reverse the order
    # so that the most recent message is at the top
    # of the list
    # Convert to list if it's not already one, assuming messages is iterable
    messages_list = list(messages)

    # Reverse the list
    reversed_messages = messages_list[::-1]
    
    pretty_print( reversed_messages )
