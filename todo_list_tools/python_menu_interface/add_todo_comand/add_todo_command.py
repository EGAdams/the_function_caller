#
# AddTodoCommand implements IMenuCommand
#
from python_menu_interface.menu_command.i_menu_command import IMenuCommand

class AddTodoCommand( IMenuCommand ):
    def __init__(self, add_todo_tool):
        self.add_todo_tool = add_todo_tool

    def execute(self):
        task = input(
            "What is the task that you want to add to the TODO list?\n")
        result = self.add_todo_tool.add_todo(task)
        print(result)
        # Simulate a pause after the task is added
        import time
        time.sleep(1)
