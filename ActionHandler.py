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
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                arguments = JSONArgumentParser.parse_arguments(tool_call.function.arguments)
                output = self.function_executor.execute_function(function_name, arguments)
                self.run = self.api_client.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=self.run.id,
                    tool_call_id=tool_call.id,
                    output=output )
        return self.run
