import os
import sys
from xmlrpc.server import SimpleXMLRPCServer
from mailboxes.rpc_mailbox.rpc_mailbox import IRPCCommunication
from mailboxes.rpc_mailbox.threaded_rpc import ThreadingXMLRPCServer
from agents.base_agent.base_agent import BaseAgent
from chromadb import Client
from chromadb.config import Settings
import pickle

class MemoryAgent(BaseAgent):
    def __init__(self, agent_id: str, server_port: int, db_path: str = "./tmp/memory_agent_db"):
        super().__init__(agent_id, server_port)
        self.db_path = db_path
        self.db_client = Client(Settings(
            anonymized_telemetry=False, allow_reset=True, is_persistent=True, persist_directory=db_path
        ))
        self.memo_store = self.db_client.create_collection("memos", get_or_create=True)
        self.memo_dict = {}
        self.load_memos()

    def process_message(self, message: dict):
        command = message.get("command")
        if command == "store":
            input_text = message.get("input_text", "")
            output_text = message.get("output_text", "")
            self.store_memo(input_text, output_text)
            return f"Stored: {input_text} -> {output_text}"
        elif command == "retrieve":
            query_text = message.get("query_text", "")
            results = self.retrieve_memo(query_text)
            return results
        else:
            return "Unknown command."

    def store_memo(self, input_text: str, output_text: str):
        memo_id = str(len(self.memo_dict) + 1)
        self.memo_store.add(documents=[input_text], ids=[memo_id])
        self.memo_dict[memo_id] = (input_text, output_text)
        self.save_memos()

    def retrieve_memo(self, query_text: str):
        results = self.memo_store.query(query_texts=[query_text], n_results=5)
        retrieved_memos = []
        for idx, memo_id in enumerate(results['ids'][0]):
            input_text, output_text = self.memo_dict[memo_id]
            distance = results['distances'][0][idx]
            retrieved_memos.append({
                "input_text": input_text,
                "output_text": output_text,
                "distance": distance
            })
        return retrieved_memos

    def save_memos(self):
        path = os.path.join(self.db_path, "memo_dict.pkl")
        with open(path, "wb") as file:
            pickle.dump(self.memo_dict, file)

    def load_memos(self):
        path = os.path.join(self.db_path, "memo_dict.pkl")
        if os.path.exists(path):
            with open(path, "rb") as file:
                self.memo_dict = pickle.load(file)

if __name__ == "__main__":
    PORT = 8005
    memory_agent = MemoryAgent(agent_id="memory_agent", server_port=PORT)
    try:
        memory_agent.logger.info(f"MemoryAgent starting on port {PORT}...")
        print(f"Starting XML-RPC server on port {PORT}")
        memory_agent.run()  # Start the XML-RPC server
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
        memory_agent.logger.info("Shutting down...")
        print("=== MemoryAgent shutdown complete ===")
