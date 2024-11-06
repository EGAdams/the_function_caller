#
# ShowTodoListCommand implements IMenuCommand
#
from python_menu_interface.menu_command.i_menu_command import IMenuCommand
from task.task import Task

class ShowTodoListCommand(IMenuCommand):
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler

    def execute(self):
        todo_list = self.storage_handler.load()
        if todo_list:
            for todo_dict in todo_list:
                task = Task(todo_dict)
                print(task.display_tree())
        else:
            print("No tasks in the TODO list.")
        import time
        time.sleep(1)
