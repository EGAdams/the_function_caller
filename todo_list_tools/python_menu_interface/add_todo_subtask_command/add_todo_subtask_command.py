#
# AddTodoSubtaskCommand implements IMenuCommand 110424
#
from python_menu_interface.menu_command.i_menu_command import IMenuCommand

class AddTodoSubtaskCommand( IMenuCommand ):
    def __init__(self, add_todo_subtask_tool ):
        self.add_todo_subtask_tool = add_todo_subtask_tool

    def execute(self):
        parent_id = input( "What is the id of the Task that you want to add a subtask for?\n" )
        description = input( "What is the subtask that you want to add to this task?\n")
        result = self.add_todo_subtask_tool.add_todo_subtask( description, parent_id ) 
        print(result)
        # Simulate a pause after the task is added
        import time
        time.sleep(1)
