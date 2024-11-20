import sys
import json
import time
from time import sleep
from openai import OpenAI


GPT_MODEL = "gpt-3.5-turbo-0125"
sys.path.append( '/home/adamsl/the_function_caller' )
from mailboxes.file_mailbox.file_mailbox import FileMailbox
from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent import BaseAgent

class PlannerAgent( BaseAgent ):
    def __init__(self) -> None:
        self.client           = OpenAI()                              # create the client
        self.pretty_print     = PrettyPrint()
        self.assistantFactory = AssistantFactory()
        self.assistant =  self.assistantFactory.getExistingAssistant( assistant_id="asst_OqWn6Ek5CyYlWUrYJYyhpNQh" )
        self.run_spinner = RunSpinner( self.client )                  # create the wait loop Object
        self.thread           = self.self.client.beta.threads.create()          # create a thread
        self.message          = self.self.client.beta.threads.messages.create(  # Add a message to a thread
            thread_id=self.self.thread.id,
            role="user",
            content="What is on the agenda for today?" )
        self.mailbox = FileMailbox( "planner_agent" )
        pass

    def show_json( self, obj ):
        json_obj = json.loads( obj.model_dump_json())
        pretty_json = json.dumps( json_obj, indent=4 )  # Pretty print JSON
        print( pretty_json )
        # https://platform.openai.com/assistants/asst_OqWn6Ek5CyYlWUrYJYyhpNQh


    # run = self.client.beta.threads.runs.create( thread_id=self.self.thread.id,assistant_id=assistant.id ) # Create the run
    # run = run_spinner.spin( run, thread )                    # wait for the initial run to finish...
    # show_json( run )

    # messages = self.client.beta.threads.messages.list( thread_id=self.thread.id )
    # show_json( messages )                                    # display the assistant's response
    # print ( "\n" )

    def process_message( self, new_message ):
        # new_message = input( "Enter a message to send to the assistant: " ) # get message from user
        message = self.self.client.beta.threads.messages.create(                      # Add a message to a thread
            thread_id=self.thread.id,
            role="user",
            content=new_message )                                           # then run the assistant...
        run       = self.client.beta.threads.runs.create( thread_id=self.thread.id, assistant_id=self.assistant.id )
        run_steps = self.client.beta.threads.runs.steps.list(                    # get the run steps so that 
            thread_id=self.thread.id, run_id=run.id, order="asc" )               # we can look at them
        
        for step in run_steps.data:
            step_details = step.step_details                  
            print( json.dumps( self.show_json( step_details ), indent=4 ))       # look at them

        self.run_spinner.spin( run, self.thread )                                     # run is done.  dropped into bit bucket.
        messages            = self.client.beta.threads.messages.list( thread_id=self.thread.id ) # done waiting.  get messages...
        messages_list       = list( messages )
        reversed_messages   = messages_list[::-1]                           # Reverse the list
        # return the last message
        return reversed_messages[0].content[0].text.value # return the last message
        # pretty_print.execute( reversed_messages )                           # print the conversation so far
