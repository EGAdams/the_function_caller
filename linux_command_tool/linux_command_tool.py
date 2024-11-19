import pexpect

class LinuxCommandTool:
    """
    Provides a tool for executing Linux commands and capturing their output using pexpect.
    
    The `LinuxCommandTool` class exposes an `execute_command` function that can be used to run a Linux command
    and capture its output. The function takes a `command` parameter that specifies the command to execute.
    
    The `schema` method returns a JSON schema that describes the `execute_command` function, including its
    parameters and return value.
    """
    
    def __init__(self):
        print("Initializing LinuxCommandTool")

    def schema():
        return {
            "type": "function",
            "function": {
                "name": "execute_command",
                "description": "Execute a Linux command and capture its output",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The Linux command to execute."
                        }
                    },
                    "required": ["command"]
                }
            }
        }

    def execute_command(command):
        """Executes a Linux command and captures its output using pexpect.
        
        Args:
            command (str): The Linux command to execute.
        
        Returns:
            str: The output of the command.
        """
        try:
            print(f"Executing( pexpect.spawn ) command: {command}")
            child = pexpect.spawn(command, encoding='utf-8')
            output = child.read().strip()
            child.close()
            return f"Command output:\n{output}"
        except pexpect.ExceptionPexpect as e:
            return f"An error occurred while executing the command: {str(e)}"