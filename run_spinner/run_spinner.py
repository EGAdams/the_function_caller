#
# Class RunSpinner
#
from ActionHandler import ActionHandler
import time
from time import sleep

class RunSpinner():
    def __init__( self, client_arg ):
        self.spin_count = 0
        self.client     = client_arg
        self.SLEEP_TIME = 1.0

    def spin( self, run, thread ):
        print ( "entering while.  run status is: " + run.status )
        while run.status == "queued" or \
            run.status == "in_progress" or \
            run.status == "requires_action":
            run = self.client.beta.threads.runs.retrieve( thread_id=thread.id, run_id=run.id )
            time.sleep( self.SLEEP_TIME )  # shhhh... im sleeping...
            print( "done sleeping.  checking for any action required..." )
            if run.status == "requires_action":
                print( "found action required.  sending the run for processing..." )
                messages = self.client.beta.threads.messages.list( thread_id=thread.id )
                actionHandler = ActionHandler( messages, run )
                actionHandler.execute( thread.id ) # modifies run for now...
        
        print( f"Run { run.id } is { run.status }." )

        return run