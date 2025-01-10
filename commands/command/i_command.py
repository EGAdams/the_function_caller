#
# ICommand interface
#
from abc import ABC, abstractmethod

class ICommand( ABC ):
    @abstractmethod
    def execute( self, message: dict ) -> dict:
        pass
     