# Persana 
You are an expert Python programmer.

# Instructions
Please create a detailed mermaid sequence diagram for the following code.

```python
class ILogger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass
```

```python
class IPortHandler(ABC):
    @abstractmethod
    def is_port_in_use(self, port: int) -> bool:
        pass

    @abstractmethod
    def kill_process_on_port(self, port: int):
        pass
```

```python
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
```

```python
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
```

```python
class ConsoleLogger(ILogger):
    def info(self, message: str):
        print(f"INFO: {message}")

    def error(self, message: str):
        print(f"*** ERROR: {message} ***")
```

```python
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
```

```python
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
```

```python
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
```

```python
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
```

```python
class ICommunicationStrategyFactory(ABC):
    @abstractmethod
    def create(self) -> ICommunicationStrategy:
        pass
```

```python
class RPCCommunicationStrategyFactory(ICommunicationStrategyFactory):
    def __init__(self, port: int, logger: ILogger):
        self.port = port
        self.logger = logger

    def create(self, agent) -> ICommunicationStrategy:
        return RPCCommunicationStrategy(agent=agent, port=self.port, logger=self.logger)
```

```python
class DefaultCommand( ICommand ):
    def execute(self, message: dict) -> dict:
        # Default processing logic
        print ( "Default processing logic" )
        return {"status": "processed"}
```

```python
class CustomCommand( ICommand ):
    def execute(self, message: dict) -> dict:
        # Custom processing logic
        return {"status": "custom_processed"}
```

```python
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
        author_url = message.get( "author_url" )
        next_command = message.get( "command" )
        print( f"sending message from {self.agent_id} to {author_url} with command: {next_command}" )
        self.send_message( response, author_url )
```

```python
class CoderAgent( BaseAgent ):
    def __init__( self, agent_id: str, strategy_factory, agent_url: str, logger=None ):
        super().__init__( agent_id, strategy_factory, logger or ConsoleLogger())
        self.url                = agent_url
        self.client             = OpenAI()                                  # Create the OpenAI client
        self.pretty_print       = PrettyPrint()
        self.assistant_factory  = AssistantFactory()
        self.assistant          = self.assistant_factory.getExistingAssistant( assistant_id="asst_MGrsitU5ZvgY530WDBLK3ZaS" )
        self.run_spinner        = RunSpinner( self.client )
        self.thread             = self.client.beta.threads.create()         # Create a thread
        self.message            = self.client.beta.threads.messages.create( # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="Make sure to write testable, modular, reusable code for our project." )
        
        self.register_command( "process_message", ProcessMessageCommand( self )) # Register the command to process incoming messages

    def show_json( self, obj ):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads( obj.model_dump_json())
        pretty_json = json.dumps( json_obj, indent=4 )
        print( pretty_json )
```

```python
def main():
    """
    Main entry point for the CoderAgent.
    """
    agent_url           = "http://localhost:" + str( PORT )
    logger              = ConsoleLogger()
    strategy_factory    = RPCCommunicationStrategyFactory( port=PORT, logger=logger )

    coder_agent = CoderAgent(
        agent_id="coder_agent",
        strategy_factory=strategy_factory,
        agent_url=agent_url,
        logger=logger )

    try:
        coder_agent.logger.info( f"CoderAgent is starting on port {PORT}..." )
        coder_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        coder_agent.logger.info( "Shutting down..." )
```

```python
class EchoCommand(ICommand):
    def execute(self, message: dict) -> dict:
        """
        Simple command to echo the received message back for testing.
        """
        response = message.get('response', '')
        # return { "status": "success", "response": response }
        print(f"TestAgent received message: { response }")
```

```python
class TestAgent(BaseAgent):
    def __init__(self, agent_id: str, port: int, logger=None):
        strategy_factory = RPCCommunicationStrategyFactory(port=port, logger=logger)
        super().__init__(agent_id, strategy_factory, logger or ConsoleLogger())
        # Register commands
        self.register_command( "process_message", EchoCommand())

    def receive_message(self, message: dict) -> dict:
        """
        Handle incoming messages from other agents.
        """
        print(f"TestAgent received message: {message}")
        return self.process_message(message)
```

```python
def run_test_agent():
    """
    Run the TestAgent to receive messages.
    """
    agent_id = "test_agent"
    port = 8004  # Port for the TestAgent
    logger = ConsoleLogger()
    test_agent = TestAgent(agent_id=agent_id, port=port, logger=logger)
    test_agent.logger.info("TestAgent is running...")
    test_agent.run()
```

```python
def chat_with_coder_agent():
    """
    Chat with the remote CoderAgent via XML-RPC and allow receiving messages via TestAgent.
    """
    try:
        # Connect to the remote CoderAgent's XML-RPC server
        remote_coder_agent = xmlrpc.client.ServerProxy(CODER_AGENT_URL, allow_none=True)
        print(f"Connected to CoderAgent at: {CODER_AGENT_URL}")

        # Start the TestAgent in a separate thread
        test_agent_thread = Thread(target=run_test_agent, daemon=True)
        test_agent_thread.start()
        print(f"TestAgent is running at: {TEST_AGENT_URL}")

        while True:
            # Get user input
            user_message = input("You: ").strip()
            if user_message.lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break

            # Send the message to the CoderAgent
            message = {"command": "process_message", "author_url":TEST_AGENT_URL, "message": user_message}
            print(f"Sending message: {message}")
            try:
                response = remote_coder_agent.receive_message(message)    # the coder agent receives the message
                                                                          # the coder agent sends the message to the test agent
                                                                          # using its send message tool.
                # if the response is None, continue to the next iteration 
                if response is None:                   # jan_11_53 response should not be none here. ## it is supposed to be because
                                                       # we have no return address. jan_11_53

                    # print( "*** ERROR: no response from Agent. Continuing anyway... ***" )
                    continue
                agent_response = response.get("response", "No response")
                print(f"CoderAgent: {agent_response}")
            except xmlrpc.client.Fault as fault:
                print(f"CoderAgent returned an XML-RPC Fault: {fault}")
            except Exception as e:
                print(f"Error while sending message to CoderAgent: {e}")

    except Exception as e:
        print(f"Error during chat setup: {e}")
```

