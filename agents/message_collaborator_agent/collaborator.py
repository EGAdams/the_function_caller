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
