#
# ProcessMessageCommand( ICommand )
#
import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
from commands.command.i_command import ICommand

class ProcessMessageCommand( ICommand ):  # this is the 1st one.  next time make something like VanillaOpenAIProcessMessageCommand
    def __init__( self, coder_agent ):    # this one is processing messages for an OpenAI assistant
        self.coder_agent = coder_agent

    def execute( self, message: str ):
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        print( "Processing message for the CoderAgent..." )
        try:
            print( f"Received message: {message}" )
            message = self.coder_agent.client.beta.threads.messages.create(     # Add the incoming message to the thread
                thread_id=self.coder_agent.thread.id,
                role="user",
                content=message
            )
            print( f"Added message to thread: {message.id}" )                   # Start a run with the assistant
            run = self.coder_agent.client.beta.threads.runs.create(
                thread_id=self.coder_agent.thread.id,
                assistant_id=self.coder_agent.assistant.id )

            print( f"Started run: {run.id}" )
            self.coder_agent.run_spinner.spin( run, self.coder_agent.thread )   # Wait for the run to complete
            print( f"Run completed: {run.status}" )                             # then etch messages from the thread
            messages = self.coder_agent.client.beta.threads.messages.list( thread_id=self.coder_agent.thread.id )
            messages_list = list( messages )                                    # Get the last message as the response 
            response = messages_list[ 0 ]                                       # now the last message is in the [ 0 ] 
                                                                                # position for some reason
            # Extract the content from the response ## add "command": "process_message" back so that it is routed to the correct command!
            response_content = response.content[ 0 ].text.value
            print( f"send response content back to collaborator, response content: {response_content}" )
            # self.coder_agent.send_message_tool.send_message( "collaborator", response_content )
            print( "finished sending message from coder to collaborator" )
            return { "status": "success", "message": response_content}

        except Exception as e:
            self.coder_agent.logger.error( f"CoderAgent error processing message: {e}" )
            return { "status": "error", "message": str( e )}
