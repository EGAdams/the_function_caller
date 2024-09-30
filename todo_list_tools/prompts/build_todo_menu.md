# Persona
World-class Python Developer and seasoned user of the GoF Design Patterns

# Our Goal
Create a command-line menu system in Python to help us use the tools that manipulate the TODO List.

# Your Task For now
Create the Python menu with only one item, the "Add Todo" action.  Be creative with the design patterns.  I am trying to learn how to use them myself.

# Menu operation
When the program starts up, we show the menud:
```bash
Todo Commnad Menu
1. Add Todo
```

When the user presses "1", the system responds with:
```bash
What is the task that you want to add to the TODO list?
```

Then the user enters the task for example; "Clean my room"

The system uses the AddTodoTool to add a task to the TODO list
After the task has been added, the system responds with: 
```bash
TODO ID: {task_id} "Clean my room" added successfully.
```

Then the system sleeps for 1 second, after that, the menu is shown again.

# Python Source Code for the AddTodoTool that we are using
```python
import json
from datetime import datetime

class AddTodoTool:
    """
    Provides a tool for adding a new todo item to a list and saving it.
    """
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        self.todo_list = self.storage_handler.load()

    @staticmethod
    def schema():
        return {
            "name": "add_todo",
            "description": "Add a new todo item to the list",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to add to the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["task"]
            }
        }

    def add_todo(self, task):
        timestamp = datetime.now().isoformat()
        new_id = str(len(self.todo_list) + 1)
        todo_item = {"id": new_id, "timestamp": timestamp, "task": task}
        self.todo_list.append(todo_item)
        self.storage_handler.save(self.todo_list)
        return f"Todo item added and saved: {json.dumps(todo_item)}"
```

# Python Source Code for the Task Object that the AddTodoTool is going to use
```python
import json
from datetime import datetime

# Now, let's rerun the unit tests with the corrected Task class implementation.

# Redefine the Task class
# Define the Task class
class Task:
    """Represents a task with optional subtasks."""
    
    def __init__(self, task_dict):
        # Ensure task_dict is a dictionary
        if isinstance(task_dict, dict):
            self.id = task_dict.get('id')
            self.task = task_dict.get('task')
            self.subtasks = [Task(subtask) for subtask in task_dict.get('subtasks', [])]
        else:
            raise ValueError("task_dict must be a dictionary")

    def find_task_by_id(self, task_id):
        if self.id == task_id:
            return self
        for subtask in self.subtasks:
            result = subtask.find_task_by_id(task_id)
            if result:
                return result
        return None

    def has_subtasks(self):
        """Return True if the task has subtasks."""
        return len(self.subtasks) > 0
    
    def get_id(self):
        """Return the task's ID."""
        return self.id

    def get_task(self):
        """Return the task description."""
        return self.task
```