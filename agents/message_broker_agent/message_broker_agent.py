#
# class File Mailbox -- File-Based Mailbox Implementation
#
import json
import os
from agents.test_two_agents import MailboxInterface

class FileMailbox( MailboxInterface ):
    def __init__( self, agent_id: str, mailbox_dir: str = "./mailboxes" ):
        self.agent_id = agent_id
        self.mailbox_path = os.path.join( mailbox_dir, f"{agent_id}.mbox" )
        os.makedirs( mailbox_dir, exist_ok=True )

    def send( self, message: dict, recipient_id: str) -> None:
        recipient_mailbox = os.path.join( "./mailboxes", f"{recipient_id}.mbox" )
        with open(recipient_mailbox, 'a') as mbox: 
            mbox. write( json.dumps(message, indent=4) + '\n')  # Pretty print the JSON

    def receive( self ) -> list:
        messages = []
        if os.path.exists( self.mailbox_path):
            with open( self.mailbox_path, 'r' ) as mbox: 
                for line in mbox: 
                    messages.append( json.loads( line ))
            # Clear mailbox after reading
            open( self.mailbox_path, 'w' ).close()
        return messages


# Base Agent
class BaseAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.mailbox = FileMailbox(agent_id)
        self.logger = self.initialize_logger()

    def send_message(self, message: dict, recipient_id: str):
        self.mailbox.send(message, recipient_id)
        self.logger.info(f"Sent message to {recipient_id}:\n{json.dumps(message, indent=4)}")  # Pretty print the JSON

    def receive_messages(self):
        messages = self.mailbox.receive()
        if messages:
            self.logger.info(f"Received messages:\n{json.dumps(messages, indent=4)}")  # Pretty print the JSON list
        return messages


# Message Broker Agent
class MessageBrokerAgent(BaseAgent):
    def process_message(self, message: dict):
        self.logger.info(f"Processing message:\n{json.dumps(message, indent=4)}")  # Pretty print the JSON
        recipient = message.get("receiver")
        if recipient:
            self.route_message(message, recipient)
        else:
            self.logger.error("Message has no recipient specified!")
