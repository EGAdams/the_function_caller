#
# 09-28-2024
#
from python_menu_interface.show_todo_list_command.show_todo_list_command import ShowTodoListCommand
from todo_list_tools.add_todo_tool.add_todo_tool import AddTodoTool

class ToolFactory:
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
    
    def create_tool(self, tool_name):
        if tool_name == "add_todo":
            return AddTodoTool(self.storage_handler)
        elif tool_name == "show_todo_list":
            return ShowTodoListCommand(self.storage_handler)
        else:
            raise ValueError(f"Tool {tool_name} not found")
