#
# EditTodoDescriptionCommand implements IMenuCommand
#
import time
import sys
sys.path.append( '/home/adamsl/the_function_caller/todo_list_tools' )
from python_menu_interface.menu_command.i_menu_command import IMenuCommand

class EditTodoDescriptionCommand( IMenuCommand ):  # The command uses the tool
    def __init__( self, edit_todo_description_tool_arg ):
        self.edit_todo_description_tool = edit_todo_description_tool_arg

    def execute( self ):
        task_id = input( "Enter the ID of the task you want to edit:\n" )
        new_description = input( "Enter the new description for the task:\n" )
        result = self.edit_todo_description_tool.edit_todo_description( task_id, new_description )
        print( result )
        time.sleep( 1 ) # Simulate a pause after the task is edited
