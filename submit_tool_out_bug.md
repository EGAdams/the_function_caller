In a certain class, there are different versions of the same tool.
Here are the definitions:
```python
@overload
    def submit_tool_outputs(
        self,
        run_id: str,
        *,
        thread_id: str,
        tool_outputs: Iterable[run_submit_tool_outputs_params.ToolOutput],
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Run:
        """
        When a run has the `status: "requires_action"` and `required_action.type` is
        `submit_tool_outputs`, this endpoint can be used to submit the outputs from the
        tool calls once they're all completed. All outputs must be submitted in a single
        request.

        Args:
          tool_outputs: A list of tools for which the outputs are being submitted.

          stream: If `true`, returns a stream of events that happen during the Run as server-sent
              events, terminating when the Run enters a terminal state with a `data: [DONE]`
              message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def submit_tool_outputs(
        self,
        run_id: str,
        *,
        thread_id: str,
        stream: Literal[True],
        tool_outputs: Iterable[run_submit_tool_outputs_params.ToolOutput],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[AssistantStreamEvent]:
        """
        When a run has the `status: "requires_action"` and `required_action.type` is
        `submit_tool_outputs`, this endpoint can be used to submit the outputs from the
        tool calls once they're all completed. All outputs must be submitted in a single
        request.

        Args:
          stream: If `true`, returns a stream of events that happen during the Run as server-sent
              events, terminating when the Run enters a terminal state with a `data: [DONE]`
              message.

          tool_outputs: A list of tools for which the outputs are being submitted.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def submit_tool_outputs(
        self,
        run_id: str,
        *,
        thread_id: str,
        stream: bool,
        tool_outputs: Iterable[run_submit_tool_outputs_params.ToolOutput],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Run | Stream[AssistantStreamEvent]:
        """
        When a run has the `status: "requires_action"` and `required_action.type` is
        `submit_tool_outputs`, this endpoint can be used to submit the outputs from the
        tool calls once they're all completed. All outputs must be submitted in a single
        request.

        Args:
          stream: If `true`, returns a stream of events that happen during the Run as server-sent
              events, terminating when the Run enters a terminal state with a `data: [DONE]`
              message.

          tool_outputs: A list of tools for which the outputs are being submitted.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["thread_id", "tool_outputs"], ["thread_id", "stream", "tool_outputs"])
    def submit_tool_outputs(
        self,
        run_id: str,
        *,
        thread_id: str,
        tool_outputs: Iterable[run_submit_tool_outputs_params.ToolOutput],
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Run | Stream[AssistantStreamEvent]:
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        if not run_id:
            raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
        extra_headers = {"OpenAI-Beta": "assistants=v2", **(extra_headers or {})}
        return self._post(
            f"/threads/{thread_id}/runs/{run_id}/submit_tool_outputs",
            body=maybe_transform(
                {
                    "tool_outputs": tool_outputs,
                    "stream": stream,
                },
                run_submit_tool_outputs_params.RunSubmitToolOutputsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Run,
            stream=stream or False,
            stream_cls=Stream[AssistantStreamEvent],
        )
```

Here is the Python class that is using the needed submit_tool_outputs method:
```python
from openai import OpenAI
class OAIFunctionCallClient:
    def __init__(self):
        self.client = OpenAI()

    # returns a run object
    def return_output_to_caller( self, thread_id, run_id, tool_call_id, tools_outputs_array ):
        return self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tools_outputs_array )
```

Here is the Python class that is using the OAIFunctionCallClient:
```python
class ActionHandler:
    def __init__( self, messages, run ):
        self.messages           = messages
        self.run                = run
        fs_mapped_funcs         = FileSystemMappedFunctions.FileSystemMappedFunctions()
        function_map            = fs_mapped_funcs.get_function_map() # populate for file system tools
        string_to_function      = StringToFunction.StringToFunction( function_map )
        self.function_executor  = FunctionExecutor( string_to_function )
        self.api_client         = OAIFunctionCallClient()

    def execute( self, thread_id ):
        tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
        tools_outputs_array = []
        if tool_calls:
            for tool_call in tool_calls:                 # for each tool call in tool calls
                function_name = tool_call.function.name  # get the function name & arguments
                arguments = JSONArgumentParser.parse_arguments( tool_call.function.arguments )
                output = self.function_executor.execute_function( function_name, arguments   )
                tool_output = {"tool_call_id":tool_call.id, "output": output}
                tools_outputs_array.append(tool_output) # now continue until all tool calls completed

            self.run = self.api_client.return_output_to_caller( # submit the output to the API
                thread_id=thread_id,                 
                run_id=self.run.id,                 
                output=tools_outputs_array )                    
                
        return self.run # return the run so that we can monitor its completion status
```

Here is the error that I am getting:
```bash
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/test_ah_assistant.py", line 49, in <module>
    run_spinner.spin( run, thread )                                     # run is done.  dropped into bit bucket.
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/eg1972/the_function_caller/run_spinner/run_spinner.py", line 26, in spin
    actionHandler.execute( thread.id ) # modifies run for now...
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/eg1972/the_function_caller/ActionHandler.py", line 29, in execute
    self.run = self.api_client.return_output_to_caller( # submit the output to the API
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: OAIFunctionCallClient.return_output_to_caller() got an unexpected keyword argument 'output'
```

Please help me fix this error.
