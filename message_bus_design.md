### Core Components

1. **User**: The initiator of actions, interacting with threads and the message bus.
  
2. **Thread**: Manages the conversation or interaction flow between users and agents. It handles creating and retrieving threads, message management, and run statuses.
   
3. **MessageBus**: The central communication system facilitating message passing between various actors (threads, agents, tools). It registers handlers, sends messages, and notifies subscribers of events.

4. **OpenAIClient**: This component retrieves or creates threads based on requests from the MessageBus and manages responses.

5. **Agent**: Executes tools based on received requests and handles different run statuses (e.g., completed, requires action, or failed).

6. **Tool**: Represents executable actions that can process data or perform tasks as instructed by agents.

### Functionalities
- **Thread Creation and Management**: Users can instantiate threads that manage interactions between agents, including sending and receiving messages.
- **Message Handling**: The message bus processes messages from various sources, including requests for completions, tool executions, and error notifications.
- **Tool Execution**: Agents are responsible for executing tools as part of the overall interaction process.
- **Error Management**: The system has mechanisms for notifying users of errors and managing run statuses for threads and tools.

### Object-Oriented Design
The diagrams include a variety of interfaces and classes to define relationships:
- **Interfaces** for messages, message handling, and subscribers ensure that the implementation can be flexible and adhere to the Dependency Inversion Principle.
- **Concrete classes** like `SimpleMessageBus` and `ToolExecutionHandler` implement specific behaviors defined by the interfaces.

This architecture supports a modular and extendable design, allowing for the easy addition of new tools, agents, or message types without significant restructuring.