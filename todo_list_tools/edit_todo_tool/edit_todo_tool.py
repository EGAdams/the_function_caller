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

    def get_all_task_ids(self):
        """Collect all task IDs from the todo list."""
        ids = []
        for task in self.todo_list:
            ids.extend(task.get_all_ids())
        return ids

    def edit_todo(self, task_id: str, new_description: str):
        # Validate input types
        if not isinstance(task_id, str) or not isinstance(new_description, str):
            print("task_id is a " + str(type(task_id)))
            print("new_description is a " + str(type(new_description)))
            print("*** ERROR: edit_todo_subtask only accepts string objects for task_id and new_description ***")
            exit()

        # Find the task
        task_to_edit = TaskFinder.find_task(self.todo_list, task_id)

        if not task_to_edit:
            print(f"*** ERROR: Task with ID {task_id} not found ***")
            exit()

        # Update the task's description
        task_to_edit.update_task(new_description)

        # Save the updated todo list
        todo_list_data = [task.to_dict() for task in self.todo_list]
        self.storage_handler.save(todo_list_data)
        
        return f"Task updated successfully: [ID: {task_id}] {new_description}"
