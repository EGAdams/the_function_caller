#
# Base Agent
#
import time
from mailboxes.imailbox import IMailbox

class BaseAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.mailbox = IMailbox()
        self.logger = self.initialize_logger()
        self.SLEEP_TIME = 1

    def run(self):
        self.logger.info(f"Agent {self.agent_id} started.")
        while True:
            messages = self.receive_messages()
            for message in messages:
                self.process_message(message)
            print ( "sleeping for " + self.SLEEP_TIME + " seconds..." )
            time.sleep( self.SLEEP_TIME )

    def set_sleeptime( self, new_sleep_time: int ):
        self.SLEEP_TIME = new_sleep_time

    def send_message(self, message: dict, recipient_id: str):
        self.mailbox.send(message, recipient_id)
        self.logger.info(f"Sent message to {recipient_id}: {message}")

    def receive_messages(self):
        messages = self.mailbox.receive()
        if messages:
            self.logger.info(f"Received messages: {messages}")
        return messages

    def process_message(self, message: dict):
        raise NotImplementedError( "*** Error: Subclasses should implement this method. ***" )

    def initialize_logger(self):
        print( "*** Warning: not implemented yet but set up logging configuration here... ***" )
        pass
