import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from abc import ABC

class IRPCCommunication(ABC):
    def send(self, message: dict, recipient_url: str) -> None:
        with xmlrpc.client.ServerProxy(recipient_url) as proxy:
            proxy.receive_message(message)

    def receive(self, message: dict) -> None:
        raise NotImplementedError("Subclasses must implement the receive method.")