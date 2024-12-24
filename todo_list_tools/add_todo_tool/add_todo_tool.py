import os
import sys
# 110424
home_directory = os.path.expanduser("~")
sys.path.append( home_directory + '/the_function_caller/todo_list_tools' )

# import Task
from task import Task
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
                        "type": "object",
                        "description": "The task to add to the todo list.  may contain subtasks which are also objects with the same properties",
                    }
                },
                "additionalProperties": False,
                "required": ["task"]
            }
        }

    # def add_todo(self, task): # typesafe task
    def add_todo(self, description: str, parent_id: str ): # typesafe task
        # check if this is a task object, if not, fail and exit
        if not isinstance( description, str ):
          # print the instance type of task
          print( "task is a " + str(type(task)) + " something is not right..." )
          print( "*** ERROR: task must be a String object ***" )
          exit()

        # Generate a new ID
        new_id = str( len( self.todo_list ) + 1 )
        todo_item = {
            "id": new_id,
            "parent_id": parent_id or None,
            "priority": 1,  # Default priority
            "born_on": datetime.now().isoformat(),
            "description": description,
            "status": "born_status",
            "subtasks": []  # Initialize empty subtasks list
        }
        
        # Create a Task object
        new_task = Task( todo_item )
        
        # Add to list and save
        self.todo_list.append( new_task.to_dict())
        self.storage_handler.save( self.todo_list )
        
        return f"Task added successfully: [ID: { new_id }] { description }"

