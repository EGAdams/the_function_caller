import os
import sys

sys.path.append( '/home/adamsl/the_function_caller/todo_list_tools' )

from task import Task
from task_finder import TaskFinder
import json
from datetime import datetime

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

