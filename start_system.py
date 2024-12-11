import os
import socket
import subprocess
import sys

def is_port_in_use(port):
    """Check if a specific port is in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_agent_in_foreground(agent_name, script_path):
    """Start an agent script in the foreground."""
    print(f"Starting {agent_name} in the foreground.")
    subprocess.call([sys.executable, script_path])

def start_agent(agent_name, script_path, pipe_path):
    """Start an agent script and redirect its stdout to a named pipe."""
    # Create the named pipe if it doesn't exist
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    
    # Start the agent process
    subprocess.Popen(
        [sys.executable, script_path],
        stdout=open(pipe_path, 'w'),
        stderr=subprocess.STDOUT,
        preexec_fn=os.setpgrp  # Detach from parent process
    )
    print(f"{agent_name} started with output redirected to {pipe_path}")

def main():
    """Main function to orchestrate the starting of agents and collaboration."""
    # Define the ports each agent listens on
    collaborator_port   = 8001
    planner_port        = 8002
    coder_port          = 8003
    prompt_port         = 8004

    # Define paths to agent scripts
    planner_script       = os.path.join( 'agents/planner_agent/'            , 'planner_agent_exe.py'   )
    coder_script         = os.path.join( 'agents/coder_agent'               , 'coder_agent_exe.py'     )
    collaborator_script  = os.path.join( 'agents/message_collaborator_agent', 'collaborator.py'        )
    prompt_script        = os.path.join( 'agents/prompt_agent'              , 'prompt_agent_exe.py'    )
    collaboration_script = os.path.join( 'agents'                           , 'start_collaborating.py' )

    # Define named pipe paths
    planner_pipe        = 'planner_agent.pipe'
    coder_pipe          = 'coder_agent.pipe'
    collaborator_pipe   = 'collaborator.pipe'
    prompt_pipe         = 'prompt_agent.pipe'

    # Check if agents are currently running
    planner_running = is_port_in_use( planner_port  )
    coder_running   = is_port_in_use( coder_port    )
    prompt_running  = is_port_in_use( prompt_port   )

    # Logic to start agents based on their running status
    collaborator_running = is_port_in_use(collaborator_port)
    if not collaborator_running:
        print("Starting CollaboratorAgent first.")
        start_agent_in_foreground("CollaboratorAgent", collaborator_script)
    elif not planner_running and not coder_running and not prompt_running:
        print("Neither PlannerAgent, CoderAgent, nor PromptAgent are running. Starting PlannerAgent.")
        start_agent_in_foreground("PlannerAgent", planner_script)
    elif planner_running and not coder_running and not prompt_running:
        print("PlannerAgent is running. Starting CoderAgent.")
        start_agent_in_foreground("CoderAgent", coder_script)
    elif planner_running and coder_running and not prompt_running:
        print("PlannerAgent and CoderAgent are running. Starting PromptAgent.")
        start_agent_in_foreground("PromptAgent", prompt_script)
    elif not planner_running and coder_running:
        print("CoderAgent is running. Starting PlannerAgent.")
        start_agent_in_foreground("PlannerAgent", planner_script)
    elif not planner_running and prompt_running:
        print("PromptAgent is running. Starting PlannerAgent.")
        start_agent_in_foreground("PlannerAgent", planner_script)
    else:
        print("All agents are running.")
        print("Starting Collaboration.")
        # Run the collaboration script in the foreground
        subprocess.call([ sys.executable, collaboration_script ])
if __name__ == '__main__':
    main()
