This code is used to help  autonomous agents communicate with each other.  To use this code, we start every agent process separately, and then we can use this code to communicate with each other.  But there is a problem.  We input messages in the start_collaborator.py file.  When the user inputs for example "coder: what tools do you have?" The message gets sent to the coder, the coder responds with a valid message.  The problem is that the process just hangs when trying to send a message back to the collaborator.  Plesase help me explore solutions to this problem.  I may be passing the messages around incorrectly.  I am not sure.
# Python Source Code for the Agent System
```python
def main():
    # URL of the collaborator's RPC server
    collaborator_url = "http://localhost:8001"

    try:
        # Create a proxy for the collaborator's server
        with xmlrpc.client.ServerProxy(collaborator_url) as proxy:
            print("Chat client for MessageCollaboratorAgent")
            print("Type your message and press Enter. Type 'exit' to quit.")
            
            while True:
                # Get input from the user
                message = input( "input command for collaborator: " )
                
                if message.lower() == "exit":
                    print("Exiting chat client. Goodbye!")
                    break
                
                # Send the message as a command to the collaborator
                command_packaged_message = {"command": message}
                try:
                    # invoke the recieving agent's receive_message method `agent.receive_message(message)`  
                    print ( proxy.receive_message( command_packaged_message )) 
                    print(f"Message sent to collaborator: {message}")
                except Exception as e:
                    print(f"Failed to send message: {e}")
    except Exception as e:
        print(f"Error connecting to collaborator: {e}")
```

```python
class BaseAgentLogger:          # create a generic logger out
    def __init__( self ):       # of thin air here.. time is burning...
        pass
        
    def info( self, message ):
        print( f"INFO: {message}" )

    def error(self, message):
        print( f"*** ERROR: {message} ***" )
```

```python
class BaseAgent:
    def __init__(self, agent_id: str, server_port: int):
        self.agent_id = agent_id
        self.server_port = server_port
        self.rpc_communication = IRPCCommunication()
        self.logger = BaseAgentLogger()

    def run(self):
        self.logger.info(f"Agent {self.agent_id} started.")
        
        # Start the XML-RPC server
        with SimpleXMLRPCServer(("localhost", self.server_port), allow_none=True) as server:
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
```

```python
class CoderAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int):
        super().__init__(agent_id, server_port)
        self.client = OpenAI()  # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()
        self.assistant = self.assistant_factory.getExistingAssistant(assistant_id="asst_MGrsitU5ZvgY530WDBLK3ZaS")
        self.run_spinner = RunSpinner(self.client)
        self.thread = self.client.beta.threads.create()  # Create a thread
        self.message = self.client.beta.threads.messages.create(  # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="Make sure to write good code for our project."
        )

    def show_json(self, obj):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

    def process_message(self, new_message: dict):
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        try:
            # Add the incoming message to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=new_message["message"]
            )

            # Start a run with the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for the run to complete
            self.run_spinner.spin(run, self.thread)

            # Fetch messages from the thread
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            messages_list = list(messages)
            reversed_messages = messages_list[::-1]

            # Return the content of the last message
            # Get the last message from reversed messages
            response = reversed_messages[len(reversed_messages) - 1]
            with xmlrpc.client.ServerProxy(collaborator_url) as proxy:
            
                # Send the message as a command to the collaborator
                command_packaged_message = { "command": response.content[0].text.value }
                try:
                    # invoke the recieving agent's receive_message method `agent.receive_message(message)`  
                    print ( proxy.receive_message( command_packaged_message )) 
                    print(f"Message sent to collaborator: {message}")
                except Exception as e:
                    print(f"Failed to send message: {e}")
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"
```

```python
def main():
    """
    Main entry point for the CoderAgent.
    """
    coder_agent = CoderAgent( agent_id="coder_agent", server_port=PORT )

    try:
        coder_agent.logger.info("CoderAgent is starting in port " + str( PORT ) + "...")
        coder_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        coder_agent.logger.info("Shutting down...")
```

```python
class PlannerAgent( BaseAgent ):
    def __init__(self, agent_id: str, server_port: int):
        super().__init__(agent_id, server_port)
        self.client = OpenAI()  # Create the OpenAI client
        self.pretty_print = PrettyPrint()
        self.assistant_factory = AssistantFactory()
        self.assistant = self.assistant_factory.getExistingAssistant(assistant_id="asst_OqWn6Ek5CyYlWUrYJYyhpNQh")
        self.run_spinner = RunSpinner(self.client)
        self.thread = self.client.beta.threads.create()  # Create a thread
        self.message = self.client.beta.threads.messages.create(  # Add a message to the thread
            thread_id=self.thread.id,
            role="user",
            content="What is on the agenda for today?"
        )

    def show_json(self, obj):
        """
        Pretty print a JSON object for debugging purposes.
        """
        json_obj = json.loads(obj.model_dump_json())
        pretty_json = json.dumps(json_obj, indent=4)
        print(pretty_json)

    def process_message(self, new_message: dict):
        """
        Process incoming messages, interact with OpenAI assistant, and respond.
        """
        try:
            # Add the incoming message to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=new_message["message"]
            )

            # Start a run with the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for the run to complete
            self.run_spinner.spin(run, self.thread)

            # Fetch messages from the thread
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            messages_list = list(messages)
            reversed_messages = messages_list[::-1]

            # Return the content of the last message
            # Get the last message from reversed messages
            response = reversed_messages[len(reversed_messages) - 1]
            # print(response.role)
            return response
            # self.send_message("collaborator", {"message": command[len("coder:"):].strip()})
            # return response
        
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"
```

```python
def main():
    """
    Main entry point for the PlannerAgent.
    """
    planner_agent = PlannerAgent( agent_id="planner_agent", server_port=PORT )

    try:
        planner_agent.logger.info("PlannerAgent is starting in port " + PORT + "...")
        planner_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        planner_agent.logger.info("Shutting down...")
```

```python
class MessageCollaboratorAgent(BaseAgent):
    def __init__(self, agent_id: str, server_port: int, agents_urls: dict):
        """
        Initializes the MessageCollaboratorAgent with a unique ID, server port, and agent URLs.
        :param agent_id: Unique identifier for this agent.
        :param server_port: Port on which this agent's XML-RPC server will run.
        :param agents_urls: Dictionary mapping agent IDs to their XML-RPC URLs.
        """
        super().__init__(agent_id, server_port)
        self.agents_urls = agents_urls  # Dictionary of other agents' RPC endpoints
        self.message_logs = []  # Maintain a log of all messages for auditing

    def send_message(self, recipient_id: str, message: dict):
        """
        Sends a message to the specified recipient via their RPC URL.
        :param recipient_id: ID of the recipient agent.
        :param message: The message content to be sent.
        """
        recipient_url = self.agents_urls.get(recipient_id)
        if recipient_url:
            try:
                with xmlrpc.client.ServerProxy(recipient_url) as proxy:
                    proxy.receive_message(message)
                    self.logger.info(f"Message sent to {recipient_id}: {message}")
                    self.message_logs.append({"to": recipient_id, "message": message})
            except Exception as e:
                self.logger.error(f"Failed to send message to {recipient_id}: {e}")
        else:
            self.logger.error(f"Unknown recipient: {recipient_id}")

    def process_message(self, message: dict):
        """
        Processes incoming messages and routes commands to other agents.
        :param message: Incoming message dictionary containing the "command" key.
        """
        try:
            command = message.get("command")
            if not command:
                self.logger.error("Invalid message format. Missing 'command'.")
                return
            
            # Example command parsing for routing
            if command.startswith("coder:"):
                self.send_message("coder", {"message": command[len("coder:"):].strip()})
            elif command.startswith("planner:"):
                self.send_message("planner", {"message": command[len("planner:"):].strip()})
            else:
                # Handle other commands or respond directly
                # self.logger.info(f"Unknown command: {command}")
                print( command )
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")

    def log_message_activity(self):
        """
        Logs all incoming and outgoing messages for debugging and auditing.
        Stub: Expand to store logs persistently (e.g., in a database or file).
        """
        self.logger.info(f"Message log: {self.message_logs}")

    def interact_with_user(self, user_input: str):
        """
        Allows direct interaction with the agent to handle user questions.
        :param user_input: A command or query from the user.
        """
        try:
            # Process the input as a message
            self.process_message({"command": user_input})
        except Exception as e:
            self.logger.error(f"Error interacting with user: {e}")

    def monitor_agent_health(self):
        """
        Monitors the health of connected agents.
        Stub: Implement periodic checks of agent availability via their RPC endpoints.
        """
        pass
```

```python
def main():
    """
    Main entry point for the MessageCollaboratorAgent.
    """
    # Define RPC URLs for other agents
    agents_urls = {
        "planner":      "http://localhost:8002",
        "coder":        "http://localhost:8003",
        "collaborator": "http://localhost:8001",
    }

    # Create the MessageCollaboratorAgent
    collaborator = MessageCollaboratorAgent(agent_id="collaborator_agent", server_port=PORT, agents_urls=agents_urls)

    # Start the RPC server for the collaborator
    try:
        collaborator.logger.info("MessageCollaboratorAgent is starting in port " + str( PORT ) + "...")
        collaborator.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        collaborator.logger.info("Shutting down...")
```

