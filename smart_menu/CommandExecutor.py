import os
import time
import signal

from MenuItem import MenuItem  # Assuming MenuItem is defined in MenuItem.py

class CommandExecutor:
    @staticmethod
    def execute_command(menu_item):
        """Executes the command associated with a given MenuItem and returns the output."""

        print("DEBUG: Entering execute_command method.")

        if not isinstance(menu_item, MenuItem):
            raise ValueError("menu_item must be an instance of MenuItem")

        print(f"DEBUG: Menu item is a valid MenuItem instance.")
        print(f"DEBUG: Action: {menu_item.action}")
        print(f"DEBUG: Working Dir: {menu_item.working_directory}")

        original_dir = os.getcwd()   # Save the original directory
        fifo_path = "/tmp/output_fifo"
        pid_file = "/tmp/output_fifo_pid"

        print(f"DEBUG: Original directory: {original_dir}")
        print(f"DEBUG: FIFO path: {fifo_path}")
        print(f"DEBUG: PID file: {pid_file}")

        try:
            # Change to the target directory if specified
            if menu_item.working_directory:
                print(f"DEBUG: Changing directory to: {menu_item.working_directory}")
                os.chdir(menu_item.working_directory)
                print(f"DEBUG: Now in {os.getcwd()}")
            else:
                print("DEBUG: No working directory specified. Staying put.")

            # Clean up any leftover FIFO or PID file
            if os.path.exists(fifo_path):
                print(f"DEBUG: Removing existing FIFO {fifo_path}")
                os.system(f"rm -f {fifo_path}")
            if os.path.exists(pid_file):
                print(f"DEBUG: Removing existing PID file {pid_file}")
                os.system(f"rm -f {pid_file}")

            # Create the FIFO
            # print("DEBUG: Creating FIFO.")
            # mkfifo_rc = os.system(f"mkfifo {fifo_path}")
            # print(f"DEBUG: mkfifo return code: {mkfifo_rc}")

            # # Construct the command line:
            # #
            # #   1) Redirect stdin from /dev/null so the script can’t block waiting for user input.
            # #   2) Redirect stdout/stderr to the FIFO.
            # #   3) Put it in the background (&).
            # #   4) Echo the PID ($!) into a pid file.
            # #
            # command = (
            #     f"{menu_item.action} < /dev/null > {fifo_path} 2>&1 & echo $! > {pid_file}"
            # )
            # print(f"DEBUG: Final shell command: {command}")

            # # Execute the command (in the background) via os.system
            # print("DEBUG: Spawning background command.")
            # rc = os.system(command)
            # print(f"DEBUG: os.system command return code: {rc}")

            # This runs in the foreground:
            os.system(menu_item.action)
            
            # Read the PID from pid_file
            # if not os.path.exists(pid_file):
            #     return "Error: PID file was not created. Command might not have started."
            # with open(pid_file, "r") as pf:
            #     pid_str = pf.read().strip()
            # if not pid_str.isdigit():
            #     return f"Error: Invalid PID read from {pid_file}: '{pid_str}'"
            # child_pid = int(pid_str)
            # print(f"DEBUG: Captured child PID: {child_pid}")

            # # Now, read from the FIFO line by line until the process finishes
            # output_lines = []
            # print("DEBUG: Opening FIFO for reading.")
            # with open(fifo_path, "r") as fifo:
            #     print("DEBUG: FIFO opened. Starting to read line by line.")
                
            #     while True:
            #         # Attempt to read one line from the FIFO
            #         line = fifo.readline()
            #         if line == "":
            #             # If we get an empty string, there are two possibilities:
            #             # 1) The command hasn't written anything else yet, or
            #             # 2) The command has exited and closed the pipe
            #             # We’ll check if the process is still alive.
            #             try:
            #                 os.kill(child_pid, 0)  # Raises OSError if process is gone
            #                 # Process is still alive, so maybe no more data *right now*.
            #                 # Sleep briefly to avoid spinning the CPU.
            #                 time.sleep(0.25)
            #                 continue
            #             except OSError:
            #                 # Process is gone, so we assume the FIFO is closed.
            #                 print("DEBUG: Child process has ended. Stopping read loop.")
            #                 break
            #         else:
            #             # We got a line of output
            #             print(f"DEBUG: READ LINE -> {line.rstrip()}")
            #             output_lines.append(line)

            # # Join lines together
            # output = "".join(output_lines)
            # print("DEBUG: Finished reading all FIFO contents.")
            # print("DEBUG: Returning output now.")
            # return output

        except Exception as e:
            print(f"DEBUG: Caught Exception: {e}")
            return f"Error: {str(e)}"

        finally:
            print("DEBUG: Entering 'finally' block. Cleaning up.")
            # Restore original directory
            try:
                os.chdir(original_dir)
                print(f"DEBUG: Changed directory back to {original_dir}")
            except Exception as exc:
                print(f"DEBUG: Could not change back to original directory: {exc}")
            
            # Remove the FIFO
            if os.path.exists(fifo_path):
                print(f"DEBUG: Removing FIFO {fifo_path}")
                os.system(f"rm -f {fifo_path}")
            
            # Remove the PID file
            if os.path.exists(pid_file):
                print(f"DEBUG: Removing PID file {pid_file}")
                os.system(f"rm -f {pid_file}")

            print("DEBUG: Done cleaning up resources. Exiting execute_command method.")
