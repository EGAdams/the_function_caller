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
        branch = " └───" if is_last else "├───" # ──
        tree_output = f"{indent}{branch}[{self.id}] {self.description}\n"
        
        for i, subtask in enumerate(self.subtasks):
            sub_is_last = (i == len(self.subtasks) - 1)
            next_indent = indent + ("    " if is_last else "│   ")
            tree_output += subtask.display_tree(next_indent, sub_is_last)
            
        return tree_output
