#
# Base Agent
#
import time
from mailboxes.imailbox import IMailbox
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from mailboxes.rpc_mailbox.rpc_mailbox import IRPCCommunication
 
class BaseAgentLogger:          # create a generic logger out
    def __init__( self ):       # of thin air here.. time is burning...
        pass
        
    def info( self, message ):
        print( f"INFO: {message}" )

    def error(self, message):
        print( f"*** ERROR: {message} ***" )


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
            server.serve_forever()

    def send_message(self, message: dict, recipient_url: str):
        self.rpc_communication.send(message, recipient_url)
        self.logger.info(f"Sent message to {recipient_url}: {message}")

    def receive_message(self, message: dict):
        self.logger.info(f"Received message: {message}")
        self.process_message(message)

    def process_message(self, message: dict):
        raise NotImplementedError("Subclasses should implement this method.")
