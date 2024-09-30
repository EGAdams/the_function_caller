#
# AddTodoCommand implements IMenuCommand
#
from python_menu_interface.menu_command.i_menu_command import IMenuCommand

class ShowTodoListCommand( IMenuCommand ):
    def __init__( self, storage_handler ):
        self.storage_handler = storage_handler

    def execute( self ):
        todo_list = self.storage_handler.load()
        if todo_list:
            for todo in todo_list:
                print( f"TODO ID: {todo['id']} - {todo['task']}" )
        else:
            print( "No tasks in the TODO list." )
        import time
        time.sleep( 1 )