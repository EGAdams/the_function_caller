import os
from MenuItem import MenuItem  # Assuming MenuItem is defined in MenuItem.py

class CommandExecutor:
    @staticmethod
    def execute_command(menu_item):
        """Executes the command associated with a given MenuItem and returns the output."""
        if not isinstance(menu_item, MenuItem):
            raise ValueError("menu_item must be an instance of MenuItem")

        original_dir = os.getcwd()  # Save the original directory
        fifo_path = "/tmp/output_fifo"  # Define the FIFO path
        
        try:
            # Change the working directory if specified
            if menu_item.working_directory:
                print(f"Changing directory to: {menu_item.working_directory}")
                os.chdir(menu_item.working_directory)

            print(f"Executing command: {menu_item.action}")
            
            # Create a named pipe (FIFO)
            os.system(f"mkfifo {fifo_path}")
            
            # Redirect the command output to the named pipe and execute
            command = f"{menu_item.action} > {fifo_path} 2>&1 &"
            os.system(command)
            
            # Read the output from the named pipe
            with open(fifo_path, "r") as fifo:
                output = fifo.read()
            
            return output

        except Exception as e:
            return f"Error: {str(e)}"
        
        finally:
            # Cleanup: Restore original directory and remove the FIFO
            os.chdir(original_dir)
            os.system(f"rm -f {fifo_path}")
