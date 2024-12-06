import subprocess
import os
from MenuItem import MenuItem  # Assuming MenuItem is defined in MenuItem.py

class CommandExecutor:
    @staticmethod
    def execute_command(menu_item):
        """Executes the command associated with a given MenuItem and returns the output."""
        if not isinstance(menu_item, MenuItem):
            raise ValueError("menu_item must be an instance of MenuItem")

        original_dir = os.getcwd()  # Save the original directory
        try:
            # Change the working directory if specified
            if menu_item.working_directory:
                os.chdir(menu_item.working_directory)
            
            # Execute command and capture output

            result = subprocess.run(
                menu_item.action, shell=True, check=True, capture_output=True, text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command {menu_item.action}: {e.output}"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            os.chdir(original_dir)