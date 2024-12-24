import os
import socket
import subprocess

def is_port_in_use(port):
    """Check if a TCP port is in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_agent(agent_name, script_path, port):
    """Start an agent if its port is not in use."""
    if not is_port_in_use(port):
        print(f"Starting {agent_name} on port {port}...")
        subprocess.Popen(["wt.exe", "new-tab", "--title", agent_name, "wsl", "python3", script_path])
        return True
    else:
        print(f"{agent_name} already running on port {port}.")
        return False

def start_collaboration():
    """Start the collaboration mode."""
    collab_script = os.path.expanduser("~/the_function_caller/agents/start_collaborating.py")
    print("All agents are running. Starting Collaboration Mode...")
    subprocess.Popen(["wt.exe", "new-tab", "--title", "Collaboration", "wsl", "python3", collab_script])

def main():
    agents = [
        ("CollaboratorAgent", "~/the_function_caller/agents/message_collaborator_agent/collaborator.py", 8001),
        ("PlannerAgent", "~/the_function_caller/agents/planner_agent/planner_agent_exe.py", 8002),
        ("CoderAgent", "~/the_function_caller/agents/coder_agent/coder_agent_exe.py", 8003),
        ("PromptAgent", "~/the_function_caller/agents/prompt_agent/prompt_agent_exe.py", 8004),
    ]

    all_running = True
    for name, path, port in agents:
        full_path = os.path.expanduser(path)
        if not start_agent(name, full_path, port):
            all_running = False

    if all_running:
        start_collaboration()

if __name__ == "__main__":
    main()
