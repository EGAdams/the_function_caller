import json


class EditTodoTool:
    """
    Coordinates the editing of todo items and adding subtasks.
    """

    def __init__(self, storage_handler, task_finder, task_editor, subtask_manager):
        self.storage_handler = storage_handler
        self.task_finder = task_finder
        self.task_editor = task_editor
        self.subtask_manager = subtask_manager
        self.todo_list = self.storage_handler.load()

    @staticmethod
    def schema():
        return {
            "name": "edit_todo",
            "description": "Edit a todo item or add a subtask",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to edit (e.g., '19' or '19.b')"
                    },
                    "new_task": {
                        "type": "string",
                        "description": "The new task description or subtask to add"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["edit", "add_subtask"],
                        "description": "Whether to edit the existing task or add a subtask"
                    }
                },
                "additionalProperties": False,
                "required": ["task_id", "new_task", "action"]
            }
        }

    def process_request(self, task_id, new_task, action):
        """Edits a todo item or adds a subtask."""
        task = self.task_finder.find_task(self.todo_list, task_id)
        if task is None:
            return f"Task with ID {task_id} not found."

        if action == "edit":
            self.task_editor.edit_task(task, new_task)
        elif action == "add_subtask":
            self.subtask_manager.add_subtask(task, task_id, new_task)
        else:
            return f"Invalid action: {action}"
        
        self.storage_handler.save(self.todo_list)
        return f"Task updated: {json.dumps(task)}"
