#
# /** @class BaseAgent */
#
import os
import sys
import json
import socket
import subprocess
import psutil

home_directory = os.path.expanduser("~")
sys.path.append( home_directory + '/the_function_caller' )

from abc import ABC, abstractmethod
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

class BaseAgent( ABC ):
    def __init__(self, agent_id: str, server_port: int, communication_mode="rpc", mcp_server_command=None):
        self.agent_id = agent_id
        self.server_port = server_port
        self.communication_mode = communication_mode  # "rpc" or "stdio"
        self.rpc_communication = IRPCCommunication()
        self.logger = BaseAgentLogger()

        print ( "communication mode: " + communication_mode )
        print ( "initializing base agent... " )

        # MCP Server for stdio mode
        self.mcp_process = None
        if communication_mode == "stdio" and mcp_server_command:
            self.mcp_process = subprocess.Popen(
                mcp_server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

    def run(self):
        self.logger.info(f"Agent {self.agent_id} started in {self.communication_mode} mode.")

        if is_port_in_use(self.server_port):
            self.logger.info(f"Port {self.server_port} is in use. Killing the process...")
            kill_process_on_port(self.server_port)

        if is_port_in_use(self.server_port):
            self.logger.error(f"Port {self.server_port} is still in use after attempting to kill the process.")
            return

        if self.communication_mode == "rpc":
            # Start the Threading XML-RPC server
            with ThreadingXMLRPCServer(("localhost", self.server_port), allow_none=True) as server:
                server.register_instance(self)
                self.logger.info(f"Agent {self.agent_id} listening on port {self.server_port}.")
                server.serve_forever()
        elif self.communication_mode == "stdio":
            self.logger.info(f"Agent {self.agent_id} ready to process stdio requests.")
            self.process_stdio_requests()

    def process_stdio_requests(self):
        """Continuously read from the MCP server process and process messages."""
        if not self.mcp_process:
            self.logger.error("MCP process not initialized for stdio communication.")
            return

        try:
            print( "starting while loop in process_stdio_requests()..." )
            while True:
                line = self.mcp_process.stdout.readline().strip()
                if line:
                    message = json.loads(line)
                    response = self.process_message(message)
                    self.mcp_process.stdin.write(json.dumps(response) + "\n")
                    self.mcp_process.stdin.flush()
        except Exception as e:
            self.logger.error(f"Error during stdio processing: {e}")

    def send_message(self, message: dict, recipient_url: str):
        self.rpc_communication.send(message, recipient_url)
        self.logger.info(f"Sent message to {recipient_url}: {message}")

    def receive_message(self, message: dict):
        # self.logger.info(f"{self.agent_id} received message: {message}")
        return self.process_message(message)

    @abstractmethod
    def process_message(self, message: dict):
        pass

    def initialize_logger(self):
        self.logger = Logger()
