from abc import ABC, abstractmethod

class IMailbox( ABC ):
    @abstractmethod
    def send( self, message: dict, recipient_id: str ) -> None:
        print( "*** Warning: the send method for the IMailbox interface has not been implemented yet. ***" )
        pass

    @abstractmethod
    def receive( self ) -> list:
        print( "*** Warning: the receive method for the IMailbox interface has not been implemented yet. ***" )
        pass