#
# ProcessMessageCommand( ICommand )
#
import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
from commands.command.i_command import ICommand


class ProcessMessageCommand( ICommand ):
    def __init__( self, coder_agent ):
        self.coder_agent = coder_agent

    def execute( self, message: dict ) -> dict:
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        print( "Processing message for the CoderAgent..." )
        try:
            author_url = message.get( "author_url", "" )
            print( f"Author URL: {author_url}" )

            content = message.get( "message", "" )
            print( f"Received message: {content}" )
            # Add the incoming message to the thread
            message = self.coder_agent.client.beta.threads.messages.create(
                thread_id=self.coder_agent.thread.id,
                role="user",
                content=content
            )
            
            print( f"Added message to thread: {message.id}" )
            # Start a run with the assistant
            run = self.coder_agent.client.beta.threads.runs.create(
                thread_id=self.coder_agent.thread.id,
                assistant_id=self.coder_agent.assistant.id )

            print( f"Started run: {run.id}" )
            # Wait for the run to complete
            self.coder_agent.run_spinner.spin( run, self.coder_agent.thread )

            print( f"Run completed: {run.status}" )
            # Fetch messages from the thread
            messages = self.coder_agent.client.beta.threads.messages.list( thread_id=self.coder_agent.thread.id )
            messages_list = list( messages )    # Get the last message as the response 
            response = messages_list[ 0 ]       # now the last message is in the [ 0 ] position for some reason

            # Extract the content from the response ## add "command": "process_message" back so that it is routed to the correct command!
            response_content = response.content[ 0 ].text.value
            return { "status": "success", "response": response_content, "author_url": author_url, "command": "process_message" }

        except Exception as e:
            self.coder_agent.logger.error( f"CoderAgent error processing message: {e}" )
            return { "status": "error", "message": str( e )}
