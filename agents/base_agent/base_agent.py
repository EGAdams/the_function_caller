# https://chatgpt.com/share/6778c573-77d0-8006-abe3-e0a7b0512b79
from abc import ABC, abstractmethod
import json
import socket
import subprocess
import psutil
import xmlrpc

from commands.command.i_command import ICommand
from xmlrpc.server import SimpleXMLRPCServer

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
    def receive_message(self, message: dict) -> dict:
        pass

    @abstractmethod
    def send_message(self, message: dict, recipient_url: str = None):
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

    def send_message(self, message: dict, recipient_url: str):
        # Logic to send RPC message
        # Connect to the CoderAgent's XML-RPC server
        print(f"Inside class: {self.__class__.__name__} send_message method" )
        print(f"creating xmlrpc.client.ServerProxy for {recipient_url}")
        recipient_agent = xmlrpc.client.ServerProxy( recipient_url, allow_none=True )
        print(f"calling receive_message on Agent with url: {recipient_url}")
        recipient_agent.receive_message( message )
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

    def send_message(self, message: dict, recipient_url: str = None):
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

    def run(self):
        self.logger.info(f"Agent {self.agent_id} is starting...")
        self.communication_strategy.start()

    def register_command(self, key: str, command: ICommand):
        """
        Register a command with a specific key.
        """
        self.commands[key] = command
        self.logger.info(f"Registered command: {key} with {type(command).__name__}")

    def process_message(self, message: dict) -> dict:
        """
        Process a received message by finding and executing the appropriate command.
        If the command is not found, use DefaultCommand().
        """
        print(f"Processing message: {message}")
        command = self.commands.get(message.get("command"), DefaultCommand())
        print( f"Inheriting class: {self.__class__.__name__}" )
        self.logger.info(f"Processing message with command: {message.get('command', 'default')}")
        print( f"returning command.execute(message)...")
        return_message = command.execute( message )
        return return_message

    def send_message(self, message: dict, recipient_url: str = None):
        """
        Send a message using the communication strategy.
        """
        print(f"Inheriting class: {self.__class__.__name__}")
        self.logger.info(f"Sending message to {recipient_url if recipient_url else 'default recipient'}: {message}")
        if ( recipient_url ):
            print(f"calling send_message on Agent with url: {recipient_url}")
        else:
            print(f"*** Warning: calling send_message on Agent without url ***")
        self.communication_strategy.send_message( message, recipient_url )

    def receive_message(self, message: dict):
        """
        Receive a message and process it, then send a response.
        """
        print(f"Received message: {message}")
        # print the name of the class that is inheriting from BaseAgent
        print(f"Inheriting class: {self.__class__.__name__}")
        # self.logger.info(f"Received message: {message}")
        response = self.process_message(message)
        print(f"Inheriting class: {self.__class__.__name__}")
        author_url = message.get("author", {}).get("url")
        next_command = message.get( "command" )
        print( f"sending message from {self.agent_id} to {author_url} with command: {next_command}" )
        self.send_message( response, author_url )
        # we don't come back here.  we will be tunning in though.
