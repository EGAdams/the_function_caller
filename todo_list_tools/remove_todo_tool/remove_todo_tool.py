from storage_handler.storage_handler import StorageHandler

class RemoveTodoTool:
    """
    Provides a tool for removing a todo item from a list and updating the storage.
    """
    def __init__(self, file_name: str = None, storage_handler = None):
        if storage_handler:
            self.storage_handler = storage_handler
        elif file_name:
            self.storage_handler = StorageHandler(file_name)
        else:
            raise ValueError("Either file_name or storage_handler must be provided")
        
        self.todo_list = self.storage_handler.load()
    @staticmethod
    def schema():
        return {
            "name": "remove_todo",
            "description": "Remove a todo item from the list and update the storage",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to remove from the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["task_id"]
            }
        }

    def remove_todo(self, task_id):
        """Removes a todo item from the list and updates the storage."""
        def remove_recursive(task_list, target_id):
            for index, item in enumerate(task_list):
                if item["id"] == target_id:
                    removed_item = task_list.pop(index)
                    return removed_item
                if "subtasks" in item:
                    result = remove_recursive(item["subtasks"], target_id)
                    if result:
                        return result
            return None

        removed_item = remove_recursive(self.todo_list, task_id)
        if removed_item:
            self.storage_handler.save(self.todo_list)
            return f"Todo item removed and file updated: {json.dumps(removed_item)}"
        return f"Todo item not found: {task_id}"
