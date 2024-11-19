import time
import json
import os
import logging
import multiprocessing
from abc import ABC, abstractmethod

# Mailbox Interface
class MailboxInterface(ABC):
    @abstractmethod
    def send(self, message: dict, recipient_id: str) -> None:
        pass

    @abstractmethod
    def receive(self) -> list:
        pass

# File-Based Mailbox Implementation
class FileMailbox(MailboxInterface):
    def __init__(self, agent_id: str, mailbox_dir: str = "./mailboxes"):
        self.agent_id = agent_id
        self.mailbox_path = os.path.join(mailbox_dir, f"{agent_id}.mbox")
        os.makedirs(mailbox_dir, exist_ok=True)

    def send(self, message: dict, recipient_id: str) -> None:
        recipient_mailbox = os.path.join("./mailboxes", f"{recipient_id}.mbox")
        with open(recipient_mailbox, 'a') as mbox:
            mbox.write(json.dumps(message) + '\n')

    def receive(self) -> list:
        messages = []
        if os.path.exists(self.mailbox_path):
            with open(self.mailbox_path, 'r') as mbox:
                for line in mbox:
                    messages.append(json.loads(line))
            # Clear mailbox after reading
            open(self.mailbox_path, 'w').close()
        return messages

# Base Agent
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
            time.sleep(1)  # Add a delay to avoid CPU hogging

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
        logger = logging.getLogger(self.agent_id)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
        logger.addHandler(handler)
        return logger

# Test Agent
class TestAgent(BaseAgent):
    def process_message(self, message: dict):
        self.logger.info(f"Processing message: {message}")
        # Respond with an acknowledgment
        if message["message_type"] == "test_message":
            response = {
                "message_type": "response",
                "sender": self.agent_id,
                "receiver": message["sender"],
                "timestamp": time.time(),
                "payload": {"content": f"ok, from agent {self.agent_id}"}
            }
            self.send_message(response, message["sender"])

# Test Scenario
if __name__ == "__main__":
    def start_agent_process(agent_id):
        agent = TestAgent(agent_id)
        agent.run()

    # Start Agent1 and Agent2 processes
    agent1_process = multiprocessing.Process(target=start_agent_process, args=("Agent1",))
    agent2_process = multiprocessing.Process(target=start_agent_process, args=("Agent2",))
    agent1_process.start()
    agent2_process.start()

    time.sleep(2)  # Allow processes to start

    # Simulate communication between agents
    mailbox = FileMailbox("Agent1")
    test_message = {
        "message_type": "test_message",
        "sender": "Agent1",
        "receiver": "Agent2",
        "timestamp": time.time(),
        "payload": {"content": "Hello from Agent1"}
    }
    mailbox.send(test_message, "Agent2")  # Agent1 sends a message to Agent2

    time.sleep(5)  # Allow time for processing and responses

    # Terminate processes
    agent1_process.terminate()
    agent2_process.terminate()
