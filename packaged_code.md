# Persona
- World-class Python developer and avid user of the GoF design patterns.

# Your Goal
Rewrite the add_todo_subtask method in the AddTodoSubtaskTool class.  It is not adding the subtask correctly.  Maybe you can use the task iterator to help us put the subtask into the correct place in the task hierarchy.  Please let me know what I need to change to get this to work.

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

    def add_subtask( self, subtask ):
        """Add a new subtask to this task."""
        if not isinstance( subtask, dict ):
            raise TypeError( "subtask must be a JSON object" )
        # set the subtask parent id to self.id
        subtask['parent_id'] = self.id
        self.subtasks.append( subtask )
        return self

    def update_task( self, new_task_description ):
        """Update the task description."""
        self.description = new_task_description
        return self

    def to_dict( self ):
        """Convert Task object to dictionary representation."""
        return {
            "id"          : self.id,
            "parent_id"   : self.parent_id,
            "priority"    : self.priority,
            "born_on"     : self.born_on,
            "description" : self.description,
            "subtasks"    : [ Task(subtask).to_dict() for subtask in self.subtasks ]}
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
    
    def display_tree(self, indent="", is_last=True):
        """Display task and subtasks in a tree format with proper alignment."""
        branch = " └───" if is_last else "├───" # ──
        tree_output = f"{indent}{branch}[{self.id}] {self.description}\n"
        
        for i, subtask in enumerate(self.subtasks):
            sub_is_last = (i == len(self.subtasks) - 1)
            next_indent = indent + ("    " if is_last else "│   ")
            tree_output += subtask.display_tree(next_indent, sub_is_last)
            
        return tree_output
```

```python
class TaskIterator:
    """Iterates through the tasks based on task ID parts."""
    
    def __init__( self, task_list, task_id ):
        self.task_list = task_list
        self.task_id = task_id
    
    def iterate( self ):
        current_tasks = self.task_list.tasks
        for task in current_tasks:
            result = task.find_task_by_id( self.task_id )
            if result:
                return result
        return None
```

```python
class TaskFinder:
    """
    Finds a task within a todo list by its ID.
    
    Args:
        todo_list (TaskList): The todo list to search.
        task_id (str): The ID of the task to find.
    
    Returns:
        Task: The task with the specified ID, or None if not found.
    """

    @staticmethod
    def find_task( todo_list, task_id ):
        task_list = TaskFactory.create_task_list( todo_list )
        task_iterator = TaskIterator( task_list, task_id )
        return task_iterator.iterate()
```

```python
class AddTodoSubtaskTool:
    """
    Provides a tool for adding a new todo item to a list and saving it.
    """
    
    def __init__(self, storage_handler):              # load self.todo_list
        self.storage_handler = storage_handler        # from a file.
        self.todo_list = self.storage_handler.load()

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
                        "description": "The task to add to the todo list.  may contain subtasks which are also objects with the same properties",
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

    def add_todo_subtask(self, description: str, parent_id: str ):
        # check if this is a task object, if not, fail and exit
        if not isinstance( description, str ) or not isinstance( parent_id, str ):
          print( "task is a " + str(type(task)))
          print( "parent_id is a " + str(type(parent_id)))
          print( "*** ERROR: add todo subtask only accepts String objects in the constructor ***" )
          exit()

        # Generate a new ID
        new_id = str( len( self.todo_list ) + 1 )
        todo_item = {
            "id": new_id,
            "parent_id": parent_id or None,
            "priority": 1,  # Default priority
            "born_on": datetime.now().isoformat(),
            "description": description,
            "subtasks": []  # Initialize empty subtasks list
        }

        # Find the parent task inside the Task object
        parent_task = TaskFinder.find_task( self.todo_list, parent_id )

        # add the new task to the parent task
        parent_task.add_subtask( todo_item )

        # Put the edited parent task back into the todo list
        # transform the parent id to it's integer equivalent
        parent_id = int( parent_id ) - 1
        self.todo_list[ parent_id ] = parent_task.to_dict()

        self.storage_handler.save( self.todo_list )
        
        return f"Task added successfully: [ID: { new_id }] { description }"
```
