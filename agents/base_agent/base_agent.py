from abc import ABC, abstractmethod
import os
import sys
import json
import socket
import subprocess
import psutil

# Define Interfaces
class ILogger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass


class IPortHandler(ABC):
    @abstractmethod
    def is_port_in_use(self, port: int) -> bool:
        pass

    @abstractmethod
    def kill_process_on_port(self, port: int):
        pass


class IRPCServer(ABC):
    @abstractmethod
    def start_server(self, instance, port: int):
        pass


class IMCPProcessManager(ABC):
    @abstractmethod
    def start_process(self, command: list):
        pass

    @abstractmethod
    def read_output(self):
        pass

    @abstractmethod
    def write_input(self, response: dict):
        pass


# Implementations
class ConsoleLogger(ILogger):
    def info(self, message: str):
        print(f"INFO: {message}")

    def error(self, message: str):
        print(f"*** ERROR: {message} ***")


class DefaultPortHandler(IPortHandler):
    def is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def kill_process_on_port(self, port: int):
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


class XMLRPCServer(IRPCServer):
    def start_server(self, instance, port: int):
        from xmlrpc.server import SimpleXMLRPCServer
        server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
        server.register_instance(instance)
        print(f"RPC Server started on port {port}")
        server.serve_forever()


class MCPProcessManager(IMCPProcessManager):
    def __init__(self):
        self.process = None

    def start_process(self, command: list):
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def read_output(self):
        return self.process.stdout.readline().strip()

    def write_input(self, response: dict):
        self.process.stdin.write(json.dumps(response) + "\n")
        self.process.stdin.flush()


# Refactored BaseAgent
class BaseAgent(ABC):
    def __init__(self, agent_id: str, server_port: int, communication_mode="rpc",
                 mcp_server_command=None, logger: ILogger = ConsoleLogger(),
                 port_handler: IPortHandler = DefaultPortHandler(),
                 rpc_server: IRPCServer = XMLRPCServer(),
                 mcp_manager: IMCPProcessManager = MCPProcessManager()):
        self.agent_id = agent_id
        self.server_port = server_port
        self.communication_mode = communication_mode
        self.logger = logger
        self.port_handler = port_handler
        self.rpc_server = rpc_server
        self.mcp_manager = mcp_manager

        self.logger.info(f"Initializing BaseAgent with mode: {communication_mode}")
        if communication_mode == "stdio" and mcp_server_command:
            self.mcp_manager.start_process(mcp_server_command)

    def run(self):
        self.logger.info(f"Agent {self.agent_id} started in {self.communication_mode} mode.")
        if self.port_handler.is_port_in_use(self.server_port):
            self.logger.info(f"Port {self.server_port} is in use. Killing the process...")
            self.port_handler.kill_process_on_port(self.server_port)

        if self.port_handler.is_port_in_use(self.server_port):
            self.logger.error(f"Port {self.server_port} is still in use after attempting to kill the process.")
            return

        if self.communication_mode == "rpc":
            self.rpc_server.start_server(self, self.server_port)
        elif self.communication_mode == "stdio":
            self.process_stdio_requests()

    def process_stdio_requests(self):
        if not self.mcp_manager:
            self.logger.error("MCP process manager not initialized for stdio communication.")
            return

        try:
            while True:
                line = self.mcp_manager.read_output()
                if line:
                    message = json.loads(line)
                    response = self.process_message(message)
                    self.mcp_manager.write_input(response)
        except Exception as e:
            self.logger.error(f"Error during stdio processing: {e}")

    @abstractmethod
    def process_message(self, message: dict):
        pass
