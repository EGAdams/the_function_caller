# Persona
World-class Python Developer and seasoned user of the GoF Design Patterns

# Our Goal
Create a command-line menu system in Python to help us use the tools that manipulate the TODO List.

# Your Task For now
Create the Python menu with only one item, the "Add Todo" action.  Be creative with the design patterns.  I am trying to learn how to use them myself.  We will need some sample Python Task objects and make a sample config file to get us started.

# Menu operation
When the program starts up, we show the menu:
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
        born_on = datetime.now().isoformat()
        new_id = str(len(self.todo_list) + 1)
        todo_item = {"id": new_id, "born_on": born_on, "task": task}
        self.todo_list.append(todo_item)
        self.storage_handler.save(self.todo_list)
        return f"Todo item added and saved: {json.dumps(todo_item)}"
```

# Python Source Code for the Task Object that the AddTodoTool is going to use
```python
import json
from datetime import datetime

class Task:
    """Represents a task with optional subtasks.
    
    The `Task` class is used to model a task, which can have subtasks. Each task has an ID, priority, born_on, description and an array of subtask which could possibly be an empty array. Subtasks are also represented as `Task` objects.

    The class provides methods to manage the task and its subtasks, such as adding, removing, and updating tasks, as well as traversing the task hierarchy.
    """
    
    def __init__( self, task_dict ):
        if isinstance( task_dict, dict ):                  # 1st make sure task_dict is a dict
            self.id          = task_dict.get( 'id'          )
            self.priority    = task_dict.get( 'priority'    )
            self.born_on     = task_dict.get( 'born_on'   )        
            self.description = task_dict.get( 'description' )
            self.subtasks    = [ Task( subtask ) for subtask in task_dict.get( 'subtasks', [])]
        else:
            raise ValueError( "task_dict must be a dictionary" )

    def find_task_by_id( self, task_id ):
        if self.id == task_id:
            return self
        for subtask in self.subtasks:
            result = subtask.find_task_by_id( task_id )
            if result:
                return result
        return None

    def has_subtasks( self ):
        """Return True if the task has subtasks."""
        return len(self.subtasks) > 0
    
    def get_id( self ):
        """Return the task's ID."""
        return self.id

    def get_task( self ):
        """Return the task description."""
        return self.task

    def add_subtask( self, subtask ):
        """Add a new subtask to this task."""
        if not isinstance( subtask, Task ):
            raise TypeError( "subtask must be a Task object" )
        self.subtasks.append( subtask )
        return self

    def update_task( self, new_task_description ):
        """Update the task description."""
        self.task = new_task_description
        return self

    def to_dict( self ):
        """Convert Task object to dictionary representation."""
        return {
            "id"        : self.id,
            "priority"  : self.priority,
            "task"      : self.task,
            "subtasks"  : [ subtask.to_dict() for subtask in self.subtasks ]}

    def remove_subtask(self, task_id):
        """Remove a subtask by its ID."""
        for i, subtask in enumerate( self.subtasks ):
            if subtask.get_id() == task_id:
                return self.subtasks.pop( i )
            
        return None

    def get_subtasks( self ):
        """Return the list of subtasks."""
        return self.subtasks

    def set_id( self, new_id ):
        """Set a new ID for the task."""
        self.id = new_id
        return self
    
    def display_tree(self, indent=""):
        """Display task and subtasks in a tree format."""
        tree_output = f"{indent}├── {self.task}\n"
        for i, subtask in enumerate(self.subtasks):
            is_last = i == len(self.subtasks) - 1
            next_indent = indent + ("    " if is_last else "│   ")
            tree_output += subtask.display_tree(next_indent)
        return tree_output

```