import os
import subprocess
import signal

def get_active_ports(start=8000, end=8010):
    active_ports = {}
    for port in range(start, end + 1):
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            capture_output=True,
            text=True
        )
        if result.stdout:
            lines = result.stdout.splitlines()
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) > 1:
                    pid = parts[1]
                    active_ports[port] = pid
    return active_ports

def display_menu(active_ports):
    print("\nActive Ports:")
    for i, (port, pid) in enumerate(active_ports.items(), 1):
        print(f"{i}. Port {port} (PID: {pid})")
    print("0. Exit")

def kill_process(pid):
    try:
        os.kill(int(pid), signal.SIGKILL)
        print(f"Process {pid} on port successfully terminated.")
    except ProcessLookupError:
        print(f"Process {pid} not found.")
    except Exception as e:
        print(f"Error killing process {pid}: {e}")

def main():
    active_ports = get_active_ports()
    if not active_ports:
        print("No active ports found in the range 8000-8010.")
        return
    
    while True:
        display_menu(active_ports)
        choice = input("Select a port number to kill its process (or 0 to exit): ")
        
        if choice == "0":
            print("Exiting...")
            break
        
        try:
            choice = int(choice)
            ports_list = list(active_ports.keys())
            if 1 <= choice <= len(ports_list):
                selected_port = ports_list[choice - 1]
                kill_process(active_ports[selected_port])
                active_ports.pop(selected_port)
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
