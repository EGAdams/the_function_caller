10:54 PM 1/16/2025
# Project: "k" is the center of the wheel.
## Goal
Create a system that makes us more efficient.

## The plan
We need to answer questions like:
- What is the fastest way to do this?
- How can we make things easier for us?


## Some things that i have come up with already.
### start with pressing the "k" key.
The first one is easy to remember. for me its the easiest key to press.  That's why the project is named `k is the center of the wheel` because that's where we start. we now want to spiral out from there.  we make this selection because it is the fastest way for me.    some people are different.  so now we have easier and faster. 
what is the next fastest thing to do to make us more efficient? 

### Use a Linux style menu to start the next task, spirialing our way out to more tasks.
We have already created a Linux style menu in Python that helps us quickly start a task.  The main menu that we open will have choice that will have a menu to start another task or another menu.  I'm pretty sure that I am faster on a terminal than i am a gui, that's why we are using this Linux style menu.  Once we get to an Agent menu for example, we would press something like "s" to start the coder agent or "e" to enter a chat with an agent that has already started."

Now we have to ask ourselves, what other traits would there be to have in a system that is supposed to make us more efficient? 

# The Current status of the project
## User Interface
Right now the selections don't really do anything that would be in the interest of starting on the next level of the wheel.
we want to be able to start the planner in a separate process, start the collaborator for smoothing out communication processes.

## Background Processes

### Agents that we have already created

#### The Coder Agent

##### Python Source code for the Coder Agent
```python
# The Coder Agent
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_MGrsitU5ZvgY530WDBLK3ZaS
import sys, os
import json
import xmlrpc.client
from time import sleep
from openai import OpenAI

import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
from commands.process_message_command.process_message_command import ProcessMessageCommand

PORT                = 8003
CHEAP_GPT_MODEL     = "gpt-3.5-turbo-0125"
GPT_MODEL           = "gpt-4o-mini"

home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )

from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent
from agents.base_agent.base_agent import RPCCommunicationStrategyFactory
from agents.base_agent.base_agent import ConsoleLogger

class CoderAgent( BaseAgent ):
    def __init__( self, agent_id: str, strategy_factory, agent_url: str, logger=None ):
        super().__init__( agent_id, strategy_factory, logger or ConsoleLogger())
        self.url                = agent_url
        self.client             = OpenAI()                                  # Create the OpenAI client
        self.pretty_print       = PrettyPrint()
        self.assistant_factory  = AssistantFactory()
        self.assistant          = self.assistant_factory.getExistingAssistant( assistant_id="asst_MGrsitU5ZvgY530WDBLK3ZaS" )
        self.run_spinner        = RunSpinner( self.client )
        self.thread             = self.client.beta.threads.create()         # Create a thread
        self.message            = self.client.beta.threads.messages.create( # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="Make sure to write testable, modular, reusable code for our project." )
        
        self.register_command( "process_message", ProcessMessageCommand( self )) # Register the command to process incoming messages

    def show_json( self, obj ):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads( obj.model_dump_json())
        pretty_json = json.dumps( json_obj, indent=4 )
        print( pretty_json )


def main():
    """
    Main entry point for the CoderAgent.
    """
    agent_url           = "http://localhost:" + str( PORT )
    logger              = ConsoleLogger()
    strategy_factory    = RPCCommunicationStrategyFactory( port=PORT, logger=logger )

    coder_agent = CoderAgent(
        agent_id="coder_agent",
        strategy_factory=strategy_factory,
        agent_url=agent_url,
        logger=logger )

    try:
        coder_agent.logger.info( f"CoderAgent is starting on port {PORT}..." )
        coder_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        coder_agent.logger.info( "Shutting down..." )

if __name__ == "__main__":
    main()
```

This agent has the ability to process messages and send them to the OpenAI API.  It also has the ability to create a thread and add a message to it.  It uses RPC to communicate with other agents that use the same type of communication process.  


## What I need you for
 Can you see how this is all coming together?  I need you to help us build this project.  Many people are counting on us to get this right.  You are going to help us build something that will make us efficient programmers.  We need to be able to write code that is easy to understand, test, debug, deploy and maintain.  We need to be able to write code that is easy to test.

## What I need you to do now
Help me plan the next steps.
