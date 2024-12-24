import socket

def check_port_status(start_port, end_port, host='127.0.0.1'):
    status_list = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                status = "Open"
            except (socket.timeout, ConnectionRefusedError):
                status = "Closed"
            status_list.append((port, status))
    return status_list

if __name__ == "__main__":
    ports = check_port_status( 8000, 8005 )
    for port, status in ports:
        print(f"Port {port}: {status}")
