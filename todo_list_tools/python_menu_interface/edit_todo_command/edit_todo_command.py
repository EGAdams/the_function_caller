# EditTodoCommand implements IMenuCommand
from python_menu_interface.menu_command.i_menu_command import IMenuCommand

class EditTodoCommand( IMenuCommand ):  # The command uses the tool
    def __init__(self, edit_todo_tool):
        self.edit_todo_tool = edit_todo_tool

    def execute(self):
        task_id = input("Enter the ID of the task you want to edit:\n")
        new_description = input("Enter the new description for the task:\n")
        result = self.edit_todo_tool.edit_todo_subtask(task_id, new_description)
        print(result)
        # Simulate a pause after the task is edited
        import time
        time.sleep( 1 )
