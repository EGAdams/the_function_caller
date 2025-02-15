# https://chatgpt.com/share/6778c573-77d0-8006-abe3-e0a7b0512b79
from abc import ABC, abstractmethod
import json
import socket
import subprocess
import psutil
import xmlrpc

from commands.command.i_command import ICommand
from xmlrpc.server import SimpleXMLRPCServer
from send_message_tool.send_message_tool import SendMessageTool

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

class ICommunicationStrategy(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def receive_message(self, message: str ) -> str:
        pass

    @abstractmethod
    def send_message( self, recipient_id, message: str ):
        pass

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

class RPCCommunicationStrategy(ICommunicationStrategy):
    def __init__(self, agent, port: int, logger: ILogger):
        self.agent = agent
        self.port = port
        self.logger = logger

    def start(self):
        self.logger.info(f"Starting RPC communication on port {self.port}.")
        server = SimpleXMLRPCServer(("localhost", self.port), allow_none=True)

        # Register the agent as the handler
        server.register_instance(self.agent)
        self.logger.info("XML-RPC server is now running.")
        server.serve_forever()

    def receive_message(self, message: dict) -> dict:
        # Delegate to the agent's receive_message method
        self.logger.info("RPCCommunicationStrategy received a message.")
        return self.agent.receive_message(message)

    def send_message(self, recipient_id: str, message: str):
        recipient_url = self.agent.agent_urls.get( recipient_id )
        # Logic to send RPC message
        # Connect to the CoderAgent's XML-RPC server
        print(f"Inside class: {self.__class__.__name__} send_message method" )
        print(f"creating xmlrpc.client.ServerProxy for {recipient_url}")
        recipient_agent = xmlrpc.client.ServerProxy( recipient_url, allow_none=True )
        print(f"calling receive_message on Agent with url: {recipient_url}")
        recipient_agent.receive_message( message ) #TODO catch response!
        self.logger.info(f"done sending RPC message to {recipient_url}: {message}")

class StdioCommunicationStrategy(ICommunicationStrategy):
    def __init__(self, process_manager: IMCPProcessManager, logger: ILogger):
        self.process_manager = process_manager
        self.logger = logger

    def start(self):
        self.logger.info("Starting Stdio communication...")
        while True:
            try:
                line = self.process_manager.read_output()
                if line:
                    message = json.loads(line)
                    response = self.receive_message(message)
                    self.process_manager.write_input(response)
            except Exception as e:
                self.logger.error(f"Error during Stdio communication: {e}")

    def receive_message(self, message: dict) -> dict:
        # Logic to process stdio message
        return {"status": "received"}

    def send_message(self, recipient_id: str, message: str ):
        # Not applicable for stdio mode
        self.logger.info("Send message not supported in stdio mode.")

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

class ICommunicationStrategyFactory(ABC):
    @abstractmethod
    def create(self) -> ICommunicationStrategy:
        pass

class RPCCommunicationStrategyFactory(ICommunicationStrategyFactory):
    def __init__(self, port: int, logger: ILogger):
        self.port = port
        self.logger = logger

    def create(self, agent) -> ICommunicationStrategy:
        return RPCCommunicationStrategy(agent=agent, port=self.port, logger=self.logger)

class DefaultCommand( ICommand ):
    def execute(self, message: dict) -> dict:
        # Default processing logic
        print ( "Default processing logic" )
        return {"status": "processed"}

class CustomCommand( ICommand ):
    def execute(self, message: dict) -> dict:
        # Custom processing logic
        return {"status": "custom_processed"}

class BaseAgent(ABC):
    def __init__(self, agent_id: str, strategy_factory: ICommunicationStrategyFactory, logger: ILogger = ConsoleLogger()):
        self.agent_id = agent_id
        self.communication_strategy = strategy_factory.create( self )
        self.commands = {}
        self.logger = logger
        self.logger.info(f"Initializing BaseAgent with strategy from factory: {type(strategy_factory).__name__}")
        agents_urls = {
            "collaborator"  : "http://localhost:8001",
            "planner"       : "http://localhost:8002",
            "coder"         : "http://localhost:8003",
            "prompt"        : "http://localhost:8004" }
        
        self.send_message_tool = SendMessageTool( agents_urls ) # Create an instance of the send message tool just like we do
                                                                # when we initialize the file system mapped functions.
    def run(self):
        self.logger.info(f"Agent {self.agent_id} is starting...")
        self.communication_strategy.start()

    def register_command(self, key: str, command: ICommand):
        self.commands[key] = command
        self.logger.info(f"Registered command: {key} with {type(command).__name__}")

    def process_message( self, message: str ):
        """
        Process a received message by finding and executing the appropriate command.
        If the command is not found, use DefaultCommand().
        """
        print(f"Processing message: {message}")
        command = self.commands.get( "process_message", DefaultCommand()) # gets the child's process_message command
        print( f"command: {command}" )
        print( f"Base Agent's child: {self.__class__.__name__}" )
        self.logger.info(f"Processing message with command: process_message for now...")
        print( f"returning command.execute(message)...")
        return command.execute( message ) # executing child's process_message() for now..

    def send_message(self, recipient_id: str, message: str):
        """
        Send a message using the communication strategy.
        """
        print(f"Base Agent's child: {self.__class__.__name__}")
        self.send_message_tool.send_message( recipient_id, message )

    def receive_message( self, message: str ):
        """
        Receive a message and process it, then send a response.
        """
        print(f"Received message: {message}")
        print(f"Base Agent's child: {self.__class__.__name__}")   # print the name of the class 
        self.logger.info(f"Received message: {message}")        # that is inheriting from BaseAgent
        response = self.process_message( message )
        print ( "returning from receive_message. " )  # used to hang here because we where not returning a 
        return response                               # value.  now it is ok. 021425
