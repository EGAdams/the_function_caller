import os
import sys
import time
from xmlrpc.server import SimpleXMLRPCServer
from mailboxes.rpc_mailbox.rpc_mailbox import IRPCCommunication
from mailboxes.rpc_mailbox.threaded_rpc import ThreadingXMLRPCServer
from chromadb import Client
from chromadb.config import Settings
from teachability import MemoStore
from agents.base_agent.base_agent import BaseAgent

class MemoryAgent(BaseAgent):
    def __init__(self, agent_id: str, server_port: int):
        super().__init__(agent_id, server_port)
        self.memo_store = MemoStore(
            verbosity=1,
            reset_db=False,
            path_to_db_dir="./memory_agent_db"
        )
        self.logger.info(f"MemoryAgent {self.agent_id} initialized.")

    def process_message(self, message: dict):
        command = message.get("command")
        content = message.get("content")

        if command == "store":
            return self.store_memory(content)
        elif command == "retrieve":
            return self.retrieve_memory(content)
        else:
            self.logger.info(f"Unknown command received: {command}")
            return {"status": "error", "message": "Unknown command."}

    def store_memory(self, content: dict):
        input_text = content.get("input_text")
        output_text = content.get("output_text")

        if input_text and output_text:
            self.memo_store.add_input_output_pair(input_text, output_text)
            self.memo_store._save_memos()
            self.logger.info(f"Stored memory: {input_text} -> {output_text}")
            return {"status": "success", "message": "Memory stored."}
        else:
            return {"status": "error", "message": "Invalid memory format."}

    def retrieve_memory(self, input_text: str):
        memos = self.memo_store.get_related_memos(
            query_text=input_text, 
            n_results=5, 
            threshold=1.5
        )

        if memos:
            formatted_memos = [
                {"input_text": memo[0], "output_text": memo[1], "distance": memo[2]} for memo in memos
            ]
            self.logger.info(f"Retrieved memories for '{input_text}': {formatted_memos}")
            return {"status": "success", "memos": formatted_memos}
        else:
            self.logger.info(f"No relevant memories found for '{input_text}'.")
            return {"status": "error", "message": "No relevant memories found."}


def main():
    print("\n=== Starting MemoryAgent ===")
    memory_agent = MemoryAgent(agent_id="memory_agent", server_port=8005)

    try:
        memory_agent.logger.info("MemoryAgent is starting...")
        print("Starting XML-RPC server on port 8005")
        memory_agent.run()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
        memory_agent.logger.info("Shutting down...")
        print("=== MemoryAgent shutdown complete ===")


if __name__ == "__main__":
    main()
