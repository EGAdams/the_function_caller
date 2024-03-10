#
#  This object encapsulates the handling of 
#  the actions requred by the run
#
import json
from openai import OpenAI

class HandleActionRequired:
    
    def __init__( self, messagesArg, available_functionsArg, runArg ) -> None:
        self.messages = messagesArg
        self.run = runArg
        self.available_functions = available_functionsArg
        self.client = OpenAI()
        print ( "HandleActionRequired object created."      )
        print ( "set self.run to the run object passed in." )
    
    def execute( self, thread_idArg ):
        
        print ( "HandleActionRequired object executing..." )
        
        # loop through the tool calls and execute them       
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            
            # self.messages.append(response_message)  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                
                # get the function name
                function_name = tool_call.function.name
                
                # get the function arguments
                function_args = json.loads(tool_call.function.arguments)
                
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
                    tool_outputs=[
                        {
                            "tool_call_id": tool_call.id, # call_ids[0],
                            "output": output,
                        }
                        ]
                    )
                
            # client = OpenAI()
            # second_response = client.chat.completions.create(
            #     model="gpt-3.5-turbo-0125",
            #     messages=self.messages,
            # )  # get a new response from the model where it can see the function response
            
            # return second_response # instead, we add second_response to the run and
            # return the run object.
            return self.run
        
