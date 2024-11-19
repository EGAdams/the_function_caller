from abc import ABC, abstractmethod

class IMailbox( ABC ):
    @abstractmethod
    def send( self, message: dict, recipient_id: str ) -> None:
        pass

    @abstractmethod
    def receive( self ) -> list:
        pass