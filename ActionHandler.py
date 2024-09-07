#
import string_to_function.string_to_function as StringToFunction # for func exec
from function_executor.FunctionExecutor import FunctionExecutor
import func_map_init.file_system_mapped_functions as FileSystemMappedFunctions
from JsonArgumentParser     import JSONArgumentParser
from OAIFunctionCallClient  import OAIFunctionCallClient

class ActionHandler:
    def __init__(self, messages, run):
        self.messages = messages
        self.run = run
        fs_mapped_funcs = FileSystemMappedFunctions.FileSystemMappedFunctions()
        function_map = fs_mapped_funcs.get_function_map()  # populate for file system tools
        string_to_function = StringToFunction.StringToFunction(function_map)
        self.function_executor = FunctionExecutor(string_to_function)
        self.api_client = OAIFunctionCallClient()

    def execute(self, thread_id):
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        tools_outputs_array = []
        if tool_calls:
            for tool_call in tool_calls:  # for each tool call in tool calls
                function_name = tool_call.function.name  # get the function name & arguments
                arguments = JSONArgumentParser.parse_arguments(tool_call.function.arguments)
                output = self.function_executor.execute_function(function_name, arguments)
                tool_output = {"tool_call_id": tool_call.id, "output": output}
                tools_outputs_array.append(tool_output)  # now continue until all tool calls completed

            self.run = self.api_client.return_output_to_caller(  # submit the output to the API
                thread_id=thread_id,
                run_id=self.run.id,
                tools_outputs_array=tools_outputs_array  # Corrected argument name
            )

        return self.run  # return the run so that we can monitor its completion status
