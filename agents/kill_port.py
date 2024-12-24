import os
import sys
import socket
import subprocess

def find_process_using_port(port):
    """
    Finds the process ID (PID) of the process using the specified port.
    """
    try:
        # Use lsof to find the process using the port
        result = subprocess.run(
            ["lsof", "-i", f":{port}"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        output = result.stdout.strip()

        # Parse the output to find the PID
        lines = output.splitlines()
        if len(lines) <= 1:
            print(f"No process is using port {port}.")
            return None

        # Extract the PID from the output
        pid = lines[1].split()[1]
        print(f"Port {port} is in use by process ID: {pid}")
        return pid
    except Exception as e:
        print(f"Error finding process using port {port}: {e}")
        return None

def kill_process(pid):
    """
    Kills the process with the specified PID.
    """
    try:
        os.kill(int(pid), 9)  # 9 means SIGKILL
        print(f"Process {pid} has been killed.")
    except Exception as e:
        print(f"Error killing process {pid}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python kill_port.py <port_number>")
        sys.exit(1)

    port = sys.argv[1]
    if not port.isdigit():
        print("Port number must be an integer.")
        sys.exit(1)

    pid = find_process_using_port(port)
    if pid:
        kill_process(pid)

if __name__ == "__main__":
    main()
