#
# Base Agent
#
import time
from mailboxes.file_mailbox import FileMailbox

class BaseAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.mailbox = FileMailbox(agent_id)
        self.logger = self.initialize_logger()

    def run(self):
        self.logger.info(f"Agent {self.agent_id} started.")
        while True:
            messages = self.receive_messages()
            for message in messages:
                self.process_message(message)
            # Sleep or wait for a specific interval
            time.sleep(1)

    def send_message(self, message: dict, recipient_id: str):
        self.mailbox.send(message, recipient_id)
        self.logger.info(f"Sent message to {recipient_id}: {message}")

    def receive_messages(self):
        messages = self.mailbox.receive()
        if messages:
            self.logger.info(f"Received messages: {messages}")
        return messages

    def process_message(self, message: dict):
        raise NotImplementedError("Subclasses should implement this method.")

    def initialize_logger(self):
        print( "not implemented yet but set up logging configuration here... " )
        pass
