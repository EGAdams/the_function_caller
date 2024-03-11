```mermaid
sequenceDiagram
    participant AH as ActionHandler
    participant RP as run.required_action.submit_tool_outputs
    participant JAP as JSONArgumentParser
    participant FE as FunctionExecutor (Context)
    participant ES as ExecutionStrategy (Strategy Interface)
    participant CES as ConcreteExecutionStrategy
    participant OAI as OAIFunctionCallClient

    AH->>RP: Get tool_calls
    loop for each tool_call in tool_calls
        AH->>JAP: parse_arguments(tool_call.function.arguments)
        JAP-->>AH: arguments

        AH->>FE: set_strategy(ConcreteExecutionStrategy)
        FE->>ES: execute_function(function_name, arguments)
        ES->>CES: execute(function_name, arguments)
        CES-->>FE: output

        AH->>OAI: submit_tool_outputs(thread_id, run_id, tool_call_id, output)
        OAI-->>AH: Update self.run
    end
    AH-->>AH: return self.run
```
