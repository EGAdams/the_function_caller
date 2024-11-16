Please analyze the following Python code and think about how we could make a tool to edit the Task object:
```python
class Task:
    """Represents a task with optional subtasks.
    
    The `Task` class is used to model a task, which can have subtasks. Each task has an ID, priority, born_on, description and an array of subtask which could possibly be an empty array. Subtasks are also represented as `Task` objects.

    The class provides methods to manage the task and its subtasks, such as adding, removing, and updating tasks, as well as traversing the task hierarchy.
    """
    
    def __init__( self, task_dict ):
        if isinstance( task_dict, dict ):                  # 1st make sure task_dict is a dict
            self.id          = task_dict.get( 'id'          )
            self.parent_id   = task_dict.get( 'parent_id'   )   
            self.priority    = task_dict.get( 'priority'    )
            self.born_on     = task_dict.get( 'born_on'     )        
            self.description = task_dict.get( 'description' )
            self.status      = task_dict.get( 'status'      )
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

    def get_description( self ):
        """Return the task description."""
        return self.description
    
    def set_parent_id( self, parent_id ):
        """Set the parent ID for the task."""
        self.parent_id = parent_id

    def add_subtask( self, subtask ):
        """Add a new subtask to this task."""
        if not isinstance( subtask, Task ):
            raise TypeError( "subtask must be a Task object" )
        # set the subtask parent id to self.id
        subtask.set_parent_id ( self.id )
        self.subtasks.append( subtask )
        return self

    def update_task( self, new_task_description ):
        """Update the task description."""
        self.description = new_task_description
        return self

    def to_dict( self ):
        """Convert Task object to dictionary representation."""
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "priority": self.priority,
            "born_on": self.born_on,
            "description": self.description,
            "status": self.status,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks]
        }

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

    def get_all_ids(self):
        """Recursively collect all task IDs."""
        ids = [self.id]
        for subtask in self.subtasks:
            ids.extend(subtask.get_all_ids())
        return ids

    def display_tree(self, indent="", is_last=True):
        """Display task and subtasks in a tree format with proper alignment."""
        branch = " └───" if is_last else " ├───" # ──
        tree_output = f"{indent}{branch}[{self.id}] {self.description}\n"
        
        for i, subtask in enumerate(self.subtasks):
            sub_is_last = (i == len(self.subtasks) - 1)
            next_indent = indent + ("    " if is_last else " │   ")
            tree_output += subtask.display_tree(next_indent, sub_is_last)
            
        return tree_output
```

```python
class AddTodoSubtaskTool:
    """
    Provides a tool for adding a new todo item to a list and saving it.
    """
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        todo_list_data = self.storage_handler.load()
        # Convert the list of dicts into a list of Task objects
        self.todo_list = [Task(task_dict) for task_dict in todo_list_data]

    @staticmethod
    def schema():
        return {
            "name": "add_todo_subtask",
            "description": "Add a new todo item to the list",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "object",
                        "description": "The task to add to the todo list. May contain subtasks which are also objects with the same properties",
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "The ID of the parent task",
                    }
                },
                "additionalProperties": False,
                "required": ["task", "parent_id"]
            }
        }

    def get_all_task_ids(self):
        """Collect all task IDs from the todo list."""
        ids = []
        for task in self.todo_list:
            ids.extend(task.get_all_ids())
        return ids

    def add_todo_subtask(self, description: str, parent_id: str):
        # Validate input types
        if not isinstance(description, str) or not isinstance(parent_id, str):
            print("description is a " + str(type(description)))
            print("parent_id is a " + str(type(parent_id)))
            print("*** ERROR: add_todo_subtask only accepts string objects for description and parent_id ***")
            exit()

        # Generate a unique new ID
        existing_ids = self.get_all_task_ids()
        max_id = max([int(id) for id in existing_ids if id.isdigit()] + [0])
        new_id = str(max_id + 1)

        # Create a new Task object
        new_task = Task({
            "id": new_id,
            "parent_id": parent_id,
            "priority": 1,  # Default priority
            "born_on": datetime.now().isoformat(),
            "description": description,
            "status": "born_status",
            "subtasks": []
        })

        # Find the parent task
        parent_task = TaskFinder.find_task(self.todo_list, parent_id)

        if not parent_task:
            print(f"*** ERROR: Parent task with ID {parent_id} not found ***")
            exit()

        # Add the new task to the parent task's subtasks
        parent_task.add_subtask(new_task)

        # Save the updated todo list
        todo_list_data = [task.to_dict() for task in self.todo_list]
        self.storage_handler.save(todo_list_data)
        
        return f"Task added successfully: [ID: {new_id}] {description}"
```

Create the EditTodoSubtaskTool class.  Use the AdddTodoSubtaskTool class as a guide.
