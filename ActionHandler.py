from FunctionExecutor import FunctionExecutor
from JsonArgumentParser import JSONArgumentParser
from OAIFunctionCallClient import OAIFunctionCallClient

class ActionHandler:
    def __init__(self, messages, available_functions, run):
        self.messages = messages
        self.run = run
        self.function_executor = FunctionExecutor( available_functions )
        self.api_client = OAIFunctionCallClient()

    def execute(self, thread_id):
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        if tool_calls:
            for tool_call in tool_calls:                 # get the function name
                function_name = tool_call.function.name  # get the function arguments
                arguments = JSONArgumentParser.parse_arguments(tool_call.function.arguments)
                output = self.function_executor.execute_function(function_name, arguments)
                self.run = self.api_client.submit_tool_outputs(
                    thread_id=thread_id,                 # got output from run, now            
                    run_id=self.run.id,                  # submit the output to the API
                    tool_call_id=tool_call.id,           # and continue until all tool
                    output=output )                      # calls are complete
        return self.run          # return the run so that we can monitor its completion status
