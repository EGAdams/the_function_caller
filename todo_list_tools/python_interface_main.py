#
# 09-29-2024
#
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from python_menu_interface.edit_todo_command.edit_todo_command import EditTodoCommand
from python_menu_interface.show_todo_list_command.show_todo_list_command import ShowTodoListCommand
from python_menu_interface.add_todo_comand.add_todo_command import AddTodoCommand
from python_menu_interface.add_todo_subtask_command import AddTodoSubtaskCommand
from python_menu_interface.show_storage_handler_path_command import ShowStorageHandlerPathCommand

from python_menu_interface.menu_invoker.menu_invoker import MenuInvoker

from python_menu_interface.tool_factory.tool_factory import ToolFactory

from storage_handler.storage_handler import StorageHandler


if __name__ == "__main__":
    storage_handler = StorageHandler() # defaults to todo_list.json
    tool_factory = ToolFactory(storage_handler) # Initialize the factory
    menu = MenuInvoker()    # Create the menu

                            # Register commands
    menu.register( "1", AddTodoCommand(tool_factory.create_tool("add_todo")))
    menu.register( "2", AddTodoSubtaskCommand(tool_factory.create_tool("add_todo_subtask")))
    menu.register( "3", EditTodoCommand(tool_factory.create_tool("edit_todo_subtask")))
    menu.register( "4", ShowTodoListCommand(storage_handler))
    menu.register( "5", ShowStorageHandlerPathCommand( storage_handler ))
    menu.display_menu() # Display the menu
