#
# 09-29-2024
#
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from python_menu_interface.show_todo_list_command.show_todo_list_command import ShowTodoListCommand
from python_menu_interface.add_todo_comand.add_todo_command import AddTodoCommand
from python_menu_interface.menu_invoker.menu_invoker import MenuInvoker
from python_menu_interface.tool_factory.tool_factory import ToolFactory
from storage_handler.storage_handler import StorageHandler


if __name__ == "__main__":
    storage_handler = StorageHandler()
    tool_factory = ToolFactory(storage_handler) # Initialize the factory
    menu = MenuInvoker()    # Create the menu

                            # Register commands
    menu.register("1", AddTodoCommand(tool_factory.create_tool("add_todo")))
    menu.register("2", ShowTodoListCommand(storage_handler))
    menu.display_menu()     # Display the menu
