#
# EditTodoDescriptionTool
#
import sys
sys.path.append( '/home/adamsl/the_function_caller/todo_list_tools' )
from todo_list_tools.task.task import Task

class EditTodoDescriptionTool:
    """
    Provides a tool for editing the description of a subtask in the todo list.
    """
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        todo_list_data = self.storage_handler.load()
        # Convert the list of dicts into a list of Task objects
        self.todo_list = [Task(task_dict) for task_dict in todo_list_data]

    @staticmethod
    def schema():
        return {
            "name": "edit_todo_subtask_description",
            "description": "Edit the description of an existing subtask",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task whose description needs to be updated",
                    },
                    "new_description": {
                        "type": "string",
                        "description": "The new description for the task",
                    }
                },
                "additionalProperties": False,
                "required": ["task_id", "new_description"]
            }
        }

    def edit_todo_description(self, task_id: str, new_description: str):
        # Validate input types
        if not isinstance(task_id, str) or not isinstance(new_description, str):
            print("task_id is a " + str(type(task_id)))
            print("new_description is a " + str(type(new_description)))
            print("*** ERROR: edit_subtask_description only accepts string objects for task_id and new_description ***")
            exit()

        # Find the task using the main todo list
        parent_task = None
        target_task = None

        for task in self.todo_list:
            target_task = task.find_task_by_id(task_id)
            if target_task:
                parent_task = task
                break

        if not target_task:
            print(f"*** ERROR: Task with ID {task_id} not found ***")
            exit()

        # Update the description of the target task
        target_task.update_task_description(new_description)

        # Save the updated todo list
        todo_list_data = [task.to_dict() for task in self.todo_list]
        self.storage_handler.save(todo_list_data)

        return f"Task description updated successfully: [ID: {task_id}] {new_description}"
