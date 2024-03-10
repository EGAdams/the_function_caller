import json
from openai import OpenAI
class HandleActionRequired: #  This object encapsulates the handling of the actions requred by the run
    def __init__( self, messagesArg, available_functionsArg, runArg ) -> None:
        self.messages = messagesArg
        self.run = runArg
        self.available_functions = available_functionsArg
        self.client = OpenAI()
    
    def execute( self, thread_idArg ):      
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        if tool_calls: # Note: the JSON response may not always be valid; be sure to handle errors 
            for tool_call in tool_calls:
                function_name = tool_call.function.name # get the function name
                function_args = json.loads( tool_call.function.arguments ) # get the function arguments
                output = "" # variable that will hold the output of the function call
                # Match the function name to the actual function pointer and execute it
                if function_name == "write_file":
                    output = self.available_functions[ 'write_file' ]( function_args.get( "filename" ), function_args.get( "content" ))
                elif function_name == "read_file": # we won't need the content to read the file
                    output = self.available_functions[ 'read_file' ]( function_args.get( "filename" ))
                else:
                    output = "Function not recognized."
                
                self.run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_idArg, # passed in to execute( ... )
                    run_id=self.run.id,
                    tool_outputs=[{ "tool_call_id": tool_call.id, "output": output }])
            
            return self.run
        