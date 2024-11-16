from task.task import Task
from task_finder.task_finder import TaskFinder


class EditTodoTool:
    """
    Provides a tool for editing an existing todo item in the list and saving it.
    """
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        todo_list_data = self.storage_handler.load()
        # Convert the list of dicts into a list of Task objects
        self.todo_list = [Task(task_dict) for task_dict in todo_list_data]

    @staticmethod
    def schema():
        return {
            "name": "edit_todo_subtask",
            "description": "Edit an existing todo item in the list",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to edit",
                    },
                    "new_description": {
                        "type": "string",
                        "description": "The new description of the task",
                    }
                },
                "additionalProperties": False,
                "required": ["task_id", "new_description"]
            }
        }
