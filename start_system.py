import os 
import socket
import sys

def is_port_in_use(port):
    """Check if a specific port is in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_agent_in_foreground(agent_name, script_path):
    """Start an agent script in the foreground."""
    print(f"Starting {agent_name} in the foreground.")
    os.execlp(sys.executable, sys.executable, script_path)

def main():
    """Main function to orchestrate the starting of agents and collaboration."""
    # Define the ports each agent listens on
<<<<<<< HEAD
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
=======
    ports = {
        'CollaboratorAgent': 8001,
        'PlannerAgent': 8002,
        'CoderAgent': 8003,
        'PromptAgent': 8004
    }

    # Define paths to agent scripts
    home_directory = os.path.expanduser("~")
    scripts = {
        'CollaboratorAgent': os.path.join(home_directory, 'the_function_caller/agents/message_collaborator_agent/collaborator.py'),
        'PlannerAgent': os.path.join(home_directory, 'the_function_caller/agents/planner_agent/planner_agent_exe.py'),
        'CoderAgent': os.path.join(home_directory, 'the_function_caller/agents/coder_agent/coder_agent_exe.py'),
        'PromptAgent': os.path.join(home_directory, 'the_function_caller/agents/prompt_agent/prompt_agent_exe.py'),
        'Collaboration': os.path.join(home_directory, 'the_function_caller/start_collaborating.py')
    }
>>>>>>> 69061f4 (start system wip)

    # Check if agents are currently running
    running_status = {agent: is_port_in_use(port) for agent, port in ports.items()}

    if not running_status['CollaboratorAgent']:
        print("Starting CollaboratorAgent first.")
<<<<<<< HEAD
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
    elif planner_running and coder_running and prompt_running:
        print("Planner Agent, CoderAgent and PromptAgent is running. Starting PlannerAgent.")
        start_agent_in_foreground("PlannerAgent", planner_script)
=======
        start_agent_in_foreground("CollaboratorAgent", scripts['CollaboratorAgent'])

    elif not running_status['PlannerAgent']:
        print("Planner agent is not running, Starting PlannerAgent...")
        start_agent_in_foreground("PlannerAgent", scripts['PlannerAgent'])

    elif not running_status['CoderAgent']:
        print("PlannerAgent is running. Starting CoderAgent.")
        start_agent_in_foreground("CoderAgent", scripts['CoderAgent'])

    elif not running_status['PromptAgent']:
        print("PlannerAgent and CoderAgent are running. Starting PromptAgent.")
        start_agent_in_foreground("PromptAgent", scripts['PromptAgent'])

>>>>>>> 69061f4 (start system wip)
    else:
        print("All agents are running.")
        print("Starting Collaboration.")
        os.execlp(sys.executable, sys.executable, scripts['Collaboration'])

if __name__ == '__main__':
    main()
