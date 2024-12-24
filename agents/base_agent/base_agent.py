#
# Base Agent
#
import time
import socket
import psutil
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from mailboxes.rpc_mailbox.rpc_mailbox import IRPCCommunication
from mailboxes.rpc_mailbox.threaded_rpc import ThreadingXMLRPCServer

class BaseAgentLogger:
    def __init__(self):
        pass

    def info(self, message):
        print(f"INFO: {message}")

    def error(self, message):
        print(f"*** ERROR: {message} ***")

class Logger:
    def __init__(self):
        print("initialized...")

    def info(self, message):
        print(message)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    print(f"Killing process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                    proc.kill()
        except psutil.AccessDenied:
            print(f"Access denied when attempting to kill process on port {port}")
        except psutil.NoSuchProcess:
            print(f"Process on port {port} no longer exists")

class BaseAgent:
    def __init__(self, agent_id: str, server_port: int):
        self.agent_id = agent_id
        self.server_port = server_port
        self.rpc_communication = IRPCCommunication()
        self.logger = BaseAgentLogger()

    def run(self):
        self.logger.info(f"Agent {self.agent_id} starting on port {self.server_port}.")

        if is_port_in_use(self.server_port):
            self.logger.info(f"Port {self.server_port} is in use. Killing the process...")
            kill_process_on_port(self.server_port)

        if is_port_in_use(self.server_port):
            self.logger.error(f"Port {self.server_port} is still in use after attempting to kill the process.")
            return

        with ThreadingXMLRPCServer(("localhost", self.server_port), allow_none=True) as server:
            server.register_instance(self)
            self.logger.info(f"Agent {self.agent_id} listening on port {self.server_port}.")
            print(f"Agent {self.agent_id} listening on port {self.server_port}.")
            server.serve_forever()

    def send_message(self, message: dict, recipient_url: str):
        self.rpc_communication.send(message, recipient_url)
        self.logger.info(f"Sent message to {recipient_url}: {message}")

    def receive_message(self, message: dict):
        print(f"{self.agent_id} received message: {message}")
        self.logger.info(f"Received message: {message}")
        return self.process_message( message )

    def process_message(self, message: dict):
        raise NotImplementedError("Subclasses should implement this method.")

    def initialize_logger(self):
        self.logger = Logger()
