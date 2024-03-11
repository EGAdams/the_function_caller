```mermaid
classDiagram
    class ActionHandler
    ActionHandler : -messages
    ActionHandler : -run
    ActionHandler : function_executor
    ActionHandler : api_client

    ActionHandler : +execute(thread_id)
```