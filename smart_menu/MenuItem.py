import os
import subprocess
class MenuItem:
    """
    Represents a menu item that can be executed, with options to change the working directory, open in a subprocess, and use the expect library.

    The `MenuItem` class provides a way to encapsulate a command or action that can be executed, with various options to control how the command is run. The class has the following attributes:

    - `title`: The title or label of the menu item.
    - `action`: The command or action to be executed.
    - `working_directory`: The working directory to change to before executing the action.
    - `open_in_subprocess`: A boolean indicating whether to open the command in a new subprocess.
    - `use_expect_library`: A boolean indicating whether to use the expect library to handle the command.

    The `execute()` method is responsible for running the command or action, with the specified options. It changes the working directory if necessary, and then either runs the command in a new subprocess or in the current process, depending on the `open_in_subprocess` option. If an error occurs during execution, it is caught and printed.

    The `to_dict()` method serializes the `MenuItem` instance into a dictionary, which can be useful for storing or transmitting the menu item data.
    """
    def __init__(self, title, action, working_directory, open_in_subprocess, use_expect_library):
        self.title = title
        self.action = action
        self.working_directory = working_directory
        self.open_in_subprocess = open_in_subprocess
        self.use_expect_library = use_expect_library

    def execute(self):
        try:
            final_command = self.action
            # Change directory if specified and necessary
            if self.working_directory:
                os.chdir(self.working_directory)
            
            if self.open_in_subprocess:
                # Open the command in a new subprocess
                process = subprocess.Popen(final_command, shell=True)
                process.communicate()  # Wait for the command to complete if needed
            else:
                # Execute the command in the current process
                subprocess.run(final_command, shell=True, check=True)
            
            print(f"Command executed: {self.action}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        finally:
            # If we changed directories, change back to the original
            if self.working_directory:
                os.chdir(os.path.dirname(__file__))
        
    def to_dict(self):
        """Serializes the MenuItem into a dictionary."""
        return {
            "title": self.title,
            "action": self.action,
            "working_directory": self.working_directory,
            "open_in_subprocess": self.open_in_subprocess,
            "use_expect_library": self.use_expect_library
        }