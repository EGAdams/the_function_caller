import os
import time
import json
from base_agent import BaseAgent 

class MessageCollaboratorAgent( BaseAgent ):
    def __init__(self, agent_id, mailboxes):
        super().__init__(agent_id)
        self.mailboxes = mailboxes

    def send_message(self, recipient_id, message):
        """
        Send a message to the specified recipient's mailbox.
        """
        mailbox_path = self.mailboxes.get(recipient_id)
        if mailbox_path:
            with open(mailbox_path, "a") as f:
                f.write(json.dumps(message) + "\n")
            self.logger.info(f"Message sent to {recipient_id}: {message}")
        else:
            self.logger.error(f"Unknown agent: {recipient_id}")

    def process_message(self, message):
        """
        Process incoming messages from the mailbox.
        For this agent, we'll handle routing commands from the user.
        """
        try:
            command = message.get("command")
            if not command:
                self.logger.error("Invalid message format. Missing 'command'.")
                return
            
            if command.startswith("coder:"):
                self.send_message("coder", {"message": command[len("coder:"):].strip()})
            elif command.startswith("planner:"):
                self.send_message("planner", {"message": command[len("planner:"):].strip()})
            else:
                self.logger.info(f"Unknown command: {command}")
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")

def main():
    """
    Main entry point for the MessageCollaboratorAgent.
    """
    mailboxes = {
        "coder": "coder_mailbox.txt",
        "planner": "planner_mailbox.txt",
        "collaborator": "collaborator_mailbox.txt",
    }

    # Create the collaborator agent
    collaborator = MessageCollaboratorAgent(agent_id="collaborator", mailboxes=mailboxes)

    # Ensure mailboxes exist
    for mailbox in mailboxes.values():
        if not os.path.exists(mailbox):
            open(mailbox, "w").close()

    # Start the agent's main loop
    try:
        collaborator.logger.info("MessageCollaboratorAgent is starting...")
        collaborator.run()
    except KeyboardInterrupt:
        collaborator.logger.info("Shutting down...")

if __name__ == "__main__":
    main()
