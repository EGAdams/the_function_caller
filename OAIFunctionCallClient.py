#
# OAIFunctionCallClient class
# methods:
#
#     submit_tool_outputs( thread_id, run_id, tool_call_id, output )
#
from openai import OpenAI
class OAIFunctionCallClient:
    def __init__(self):
        self.client = OpenAI()

    # returns a run object
    def return_output_to_caller( self, thread_id, run_id, tool_call_id, output ):
        return self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=[{ "tool_call_id": tool_call_id, "output": output }])
            