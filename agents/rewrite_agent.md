Here is the Planner Agent that works by itself without the subprocess library:
```python
#
# The Planner Agent
#
# OpenAI Assistant address:
# https://platform.openai.com/assistants/asst_OqWn6Ek5CyYlWUrYJYyhpNQh
#
import sys
import json
from time import sleep
from openai import OpenAI

PORT = 8002
GPT_MODEL = "gpt-3.5-turbo-0125"
sys.path.append( '/home/adamsl/the_function_caller' )
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# from agents.planner_agent.AssistantFactory import AssistantFactory

from AssistantFactory import AssistantFactory
from run_spinner.run_spinner import RunSpinner
from pretty_print.pretty_print import PrettyPrint
from agents.base_agent.base_agent import BaseAgent

class PlannerAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int):
        super().__init__(agent_id, server_port)
        self.client = OpenAI()  # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()
        self.assistant = self.assistant_factory.getExistingAssistant(assistant_id="asst_OqWn6Ek5CyYlWUrYJYyhpNQh")
        self.run_spinner = RunSpinner(self.client)
        self.thread = self.client.beta.threads.create()  # Create a thread
        self.message = self.client.beta.threads.messages.create(  # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="What is on the agenda for today?"
        )

    def show_json(self, obj):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

    def process_message(self, new_message: dict):
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        try:
            # Add the incoming message to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=new_message["message"]
            )

            # Start a run with the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for the run to complete
            self.run_spinner.spin(run, self.thread)

            # Fetch messages from the thread
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            messages_list = list(messages)
            reversed_messages = messages_list[::-1]
            response = reversed_messages[len(reversed_messages) - 1]

            # Extract the content from the response
            response_content = response.content[0].text.value
            return response_content

        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"


def main():
    """
    Main entry point for the PlannerAgent.
    """
    planner_agent = PlannerAgent( agent_id="planner_agent", server_port=PORT )

    try:
        planner_agent.logger.info("PlannerAgent is starting in port " + str( PORT ) + "...")
        planner_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        planner_agent.logger.info("Shutting down...")


if __name__ == "__main__":
    main()
```

Please rewrite this collaborator agent to work just like the Planner agent.  I don't want it to start any subprocesses.  I just want it to start and listen on its own port.  It will take up its own terminal session, that's ok.

Here is the Python code to rewrite:
```python
import os
import socket
import subprocess
import sys
from abc import ABC, abstractmethod

# Ensure the BaseAgent is in the path
home_directory = os.path.expanduser("~")
sys.path.append(os.path.join(home_directory, "the_function_caller/agents"))
from base_agent.base_agent import BaseAgent

class AgentManager:
    """Manages starting agents based on their running status."""

    def __init__(self):
        self.agents = {
            "CollaboratorAgent": AgentConfig(8001, "message_collaborator_agent/collaborator.py"),
            "PlannerAgent": AgentConfig(8002, "planner_agent/planner_agent_exe.py"),
            "CoderAgent": AgentConfig(8003, "coder_agent/coder_agent_exe.py"),
            "PromptAgent": AgentConfig(8004, "prompt_agent/prompt_agent_exe.py"),
        }
        self.collaboration_script = os.path.join(
            home_directory, "the_function_caller/agents/start_collaborating.py"
        )

    def is_port_in_use(self, port):
        """Check if a specific port is in use on localhost."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    def start_agent(self, agent_name):
        """Start an agent based on its configuration."""
        config = self.agents[agent_name]
        script_path = os.path.join(home_directory, "the_function_caller/agents", config.script_path)
        
        if not self.is_port_in_use(config.port):
            subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setpgrp,
            )
            print(f"{agent_name} started on port {config.port}.")
        else:
            print(f"{agent_name} is already running on port {config.port}.")

    def start_collaboration(self):
        """Start the collaboration process."""
        subprocess.call([sys.executable, self.collaboration_script])

    def run(self):
        """Main function to orchestrate agent startup."""
        startup_sequence = ["CollaboratorAgent", "PlannerAgent", "CoderAgent", "PromptAgent"]
        
        for agent_name in startup_sequence:
            self.start_agent(agent_name)

        if all(self.is_port_in_use(config.port) for config in self.agents.values()):
            print("All agents are running. Starting collaboration.")
            self.start_collaboration()


class AgentConfig:
    """Stores configuration for an agent."""
    def __init__(self, port, script_path):
        self.port = port
        self.script_path = script_path

if __name__ == "__main__":
    manager = AgentManager()
    manager.run()
```

Just get rid of the AgentManager, we don't need it yet.
