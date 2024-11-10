# Novemer 10, 2024
# Shows the path to the storage handler which was 1st built to show the location of the todo list JSON file.
# ShowStorageHandlerPath implements IMenuCommand
from python_menu_interface.menu_command.i_menu_command import IMenuCommand

class ShowStorageHandlerPathCommand( IMenuCommand ):  # The command uses the tool
    def __init__( self, storage_handler ):
        self.storage_handler = storage_handler

    def execute(self):
        self.storage_handler.show_path()
        import time # Simulate a pause after the task is edited
        time.sleep( 1 )
