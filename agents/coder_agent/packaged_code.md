# Persana 
You are an expert Python programmer.

# Instructions
Analyze the following code and pay particular attention to how tools are used.

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
def chat_with_agents():
    """
    Chat with the remote CoderAgent or TestAgent via XML-RPC.
    """
    try:
        # Connect to the remote agents
        remote_coder_agent = xmlrpc.client.ServerProxy(CODER_AGENT_URL, allow_none=True)
        remote_test_agent = xmlrpc.client.ServerProxy(TEST_AGENT_URL, allow_none=True)

        print(f"Connected to CoderAgent at: {CODER_AGENT_URL}")
        print(f"Connected to TestAgent at: {TEST_AGENT_URL}")

        while True:
            # Get user input for agent selection
            target_agent = input("Select agent (coder/test): ").strip().lower()
            if target_agent not in {"coder", "test"}:
                print("Invalid agent selection. Choose 'coder' or 'test'.")
                continue

            # Get user input for the message
            user_message = input("You: ").strip()
            if user_message.lower() in {"exit", "quit"}:
                print("Exiting chat.")
                break

            # Construct the message
            message = {
                "command": "process_message",
                "author_url": TEST_AGENT_URL if target_agent == "coder" else CODER_AGENT_URL,
                "message": user_message,
            }

            # Send the message to the selected agent
            try:
                target_agent_proxy = remote_coder_agent if target_agent == "coder" else remote_test_agent
                response = target_agent_proxy.receive_message(message)

                if response is None:
                    print("No response from agent.")
                    continue

                agent_response = response.get("response", "No response")
                print(f"{target_agent.capitalize()}Agent: {agent_response}")
            except xmlrpc.client.Fault as fault:
                print(f"{target_agent.capitalize()}Agent returned an XML-RPC Fault: {fault}")
            except Exception as e:
                print(f"Error while sending message to {target_agent.capitalize()}Agent: {e}")

    except Exception as e:
        print(f"Error during chat setup: {e}")
```

```python
class ICommand( ABC ):
    @abstractmethod
    def execute( self, message: dict ) -> dict:
        pass
```

```python
class ProcessMessageCommand( ICommand ):
    def __init__( self, coder_agent ):
        self.coder_agent = coder_agent

    def execute( self, message: dict ) -> dict:
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        print( "Processing message for the CoderAgent..." )
        try:
            author_url = message.get( "author_url", "" )
            print( f"Author URL: {author_url}" )

            content = message.get( "message", "" )
            print( f"Received message: {content}" )
            # Add the incoming message to the thread
            message = self.coder_agent.client.beta.threads.messages.create(
                thread_id=self.coder_agent.thread.id,
                role="user",
                content=content
            )
            
            print( f"Added message to thread: {message.id}" )
            # Start a run with the assistant
            run = self.coder_agent.client.beta.threads.runs.create(
                thread_id=self.coder_agent.thread.id,
                assistant_id=self.coder_agent.assistant.id )

            print( f"Started run: {run.id}" )
            # Wait for the run to complete
            self.coder_agent.run_spinner.spin( run, self.coder_agent.thread )

            print( f"Run completed: {run.status}" )
            # Fetch messages from the thread
            messages = self.coder_agent.client.beta.threads.messages.list( thread_id=self.coder_agent.thread.id )
            messages_list = list( messages )    # Get the last message as the response 
            response = messages_list[ 0 ]       # now the last message is in the [ 0 ] position for some reason

            # Extract the content from the response ## add "command": "process_message" back so that it is routed to the correct command!
            response_content = response.content[ 0 ].text.value
            return { "status": "success", "response": response_content, "author_url": author_url, "command": "process_message" }

        except Exception as e:
            self.coder_agent.logger.error( f"CoderAgent error processing message: {e}" )
            return { "status": "error", "message": str( e )}
```

```python
class ReadFileTool:
    """
    Provides a tool for reading the contents of a file.
    
    The `ReadFileTool` class exposes a `read_file` function that can be used to read the contents of a file. The function takes a `file_path` parameter that specifies the path and the name of the file to read.
    
    The `schema` method returns a JSON schema that describes the `read_file` function, including its parameters and return value.
    """
    
    def __init__( self ):
        print ( "initialaizing" )

    def schema(): 
        return {
            "name": "read_file",
            "description": "This tool reads a file and returns the contents.",
            "strict": False,
            "parameters": {
                "properties": {
                "file_path": {
                    "description": "Path to the file to read with extension.",
                    "title": "File Path",
                    "type": "string"
                }
                },
                "required": [
                "file_path"
                ],
                "type": "object"
            }
        }

    def read_file(self, file_path):
        """
        Reads content from a specified file.
        
        Args:
            file_path (str): The path of the file to read.
        
        Returns:
            str: The content of the file.
        """
        # Sanitize file path for sandbox environment
        file_path = file_path.replace('/mnt/data/', '')
        print(f"Debug: Sanitized file_path = {file_path}")
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return f"Error: {e}"
```

```python
class WriteFileTool:
    """
    Provides a tool for writing the contents of a file.
    The `WriteFileTool` class exposes a `write_file` function that can be used to write a string to a file with the specified filename.
    The `schema` method returns a JSON schema that describes the parameters expected by the `write_file` function.
    """
    
    def __init__( self ):
        print ( "initialaizing" )

    @staticmethod
    def schema():
        return {
            "name": "write_file",
            "description": "Allows you to write new files.",
            "strict": False,
            "parameters": {
                "properties": {
                "chain_of_thought": {
                    "description": "Please think step-by-step about what needs to be written to the file in order for the program to match the requirements.",
                    "title": "Chain Of Thought",
                    "type": "string"
                },
                "file_path": {
                    "description": "The full path of the file to write.",
                    "type": "string"
                },
                "content": {
                    "description": "The full content of the file to write. Content must not be truncated and must represent a correct functioning program with all the imports defined.",
                    "type": "string"
                }
                },
                "required": [
                "file_path",
                "content"
                ],
                "type": "object"
            }
        }
    
    def write_file( self, file_path, content ):
        """Writes content to a specified file.
        
        Args:
            file_path (str): The full path of the file to write to.
            content (str): The content to write to the file.
        """
        
        print ( "opening file with arguments: " + file_path + " and " + content )
        with open( file_path, 'w' ) as file:
            file.write( content )

        return "File written successfully."
```

# Your Task
We need a tool that will create directoriies.  Please create this tool for our Agents to use.
