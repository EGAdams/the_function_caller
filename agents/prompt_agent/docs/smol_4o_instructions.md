# Task Description: Create an Agent System Orchestration Script

## Overview

We need a Python script, `start_system.py`, that orchestrates the initialization and management of several agents in a distributed system. Each agent should listen on a specific port and perform a distinct role in the system. The script should check if each agent is running and start any missing agents sequentially. When all agents are active, the system should switch to "Collaboration Mode."

## Agents and Their Ports

- **CollaboratorAgent**: Port 8001
- **PlannerAgent**: Port 8002
- **CoderAgent**: Port 8003
- **PromptAgent**: Port 8004

## Script Requirements

The script should reference agent scripts located in specific directories under the user's home folder:

- `CollaboratorAgent`: `~/the_function_caller/agents/message_collaborator_agent/collaborator.py`
- `PlannerAgent`: `~/the_function_caller/agents/planner_agent/planner_agent_exe.py`
- `CoderAgent`: `~/the_function_caller/agents/coder_agent/coder_agent_exe.py`
- `PromptAgent`: `~/the_function_caller/agents/prompt_agent/prompt_agent_exe.py`
- Collaboration Script: `~/the_function_caller/agents/start_collaborating.py`

## Key Functions to Implement

### `is_port_in_use(port)`

- **Purpose**: Check if a specific TCP port is in use on `localhost`.
- **Implementation**: Create a socket, attempt to connect to the specified port, and return `True` if the connection is successful.

## Execution Flow

1. **Open a New Terminal and Run**: `python3 start_system.py`
   - This should start the first available agent based on port checks.
2. **Open Another Terminal and Run**: `python3 start_system.py`
   - This should start the next agent that is not currently running.
3. **Repeat Step 2** until all agents have started in their own terminals.
4. **Final Step**: When all agents are running, the last execution of `python3 start_system.py` should automatically switch to "Collaboration Mode" by running `python3 start_collaborating.py`.
   - This should prompt the user with `input message for collaborator:` and wait for input like a chat room.

## Design Considerations

- **Process Management**: Each agent must run in its own terminal.
- **Startup Order Enforcement**: Agents must be started sequentially to ensure dependencies are met.
- **Port Checking**: A robust mechanism should ensure that agents are only started when necessary.

## Task Summary
- Create the file `start_system.py` with the specified functionality.
