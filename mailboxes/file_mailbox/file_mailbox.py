
#
# File Mail Box
#
import json
import os
from imailbox import IMailbox

class FileMailbox( IMailbox ):
    def __init__(self, agent_id: str, mailbox_dir: str = "./mailboxes"):
        self.agent_id = agent_id
        self.mailbox_path = os.path.join(mailbox_dir, f"{agent_id}.mbox")
        os.makedirs(mailbox_dir, exist_ok=True)

    def send(self, message: dict, recipient_id: str) -> None:
        recipient_mailbox = os.path.join("./mailboxes", f"{recipient_id}.mbox")
        with open(recipient_mailbox, 'a') as mbox:
            mbox.write(json.dumps(message) + '')

    def receive(self) -> list:
        messages = []
        if os.path.exists(self.mailbox_path):
            with open(self.mailbox_path, 'r') as mbox:
                for line in mbox:
                    messages.append(json.loads(line))
            # Clear mailbox after reading
            open(self.mailbox_path, 'w').close()
        return messages