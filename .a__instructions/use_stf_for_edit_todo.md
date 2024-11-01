# Persona
World-Class Python Developer and avid user of the GoF design patterns.

# Scenario
Please analyze this edit todo tool.  Instead of an if-then or case statement, I want to use a "string to function" method inside this edit todo tool so that it will not need editing no matter how many types of tasks are given to the tool.  Here is the Python code for the edit todo tool:
```python
import json

class EditTodoTool:
    def __init__(self, storage_handler, task_finder, task_editor, subtask_manager):
        self.storage_handler = storage_handler
        self.task_finder = task_finder
        self.task_editor = task_editor
        self.subtask_manager = subtask_manager
        self.todo_list = self.storage_handler.load()

    @staticmethod
    def schema():
        return {
            "name": "edit_todo",
            "description": "Edit a todo item or add a subtask",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "new_task": {"type": "string"},
                    "action": {"type": "string", "enum": ["edit", "add_subtask"]}
                },
                "additionalProperties": False,
                "required": ["task_id", "new_task", "action"]
            }
        }

    def process_request(self, task_id, new_task, action):
        task = self.task_finder.find_task(self.todo_list, task_id)
        if task is None:
            return f"Task with ID {task_id} not found."
        if action == "edit":
            self.task_editor.edit_task(task, new_task)
        elif action == "add_subtask":
            self.subtask_manager.add_subtask(task, task_id, new_task)
        else:
            return f"Invalid action: {action}"
        self.storage_handler.save(self.todo_list)
        return f"Task updated: {task}"
```

Here is the Python code for the string to function method:
```python
#
#  creates a live function from a string
#
class StringToFunction:
    def __init__( self, function_map_arg ):
        '''
        Initialize the StringToFunction object with a dictionary of available functions.
        
        Args:
            function_map_arg (dict): A dictionary mapping function names to their implementations.
        '''
        self.function_map = function_map_arg

    def create_function_from_string( self, function_name ):
        '''
        Create a function from a string.

        Args:
            function_string (str): The string representation of the function.

        Returns:
            function: The function object.
        '''
        if ( self.function_map.get_length() == 0 ):
            print( "*** Error: No functions initialized in the StringToFunction Object. ***" )
            return None
        
        function_maps = self.function_map.get_all_entries()
        if function_name in function_maps:
            return self.function_map.get_function( function_name )
        else:
            return None
```

The function map to use for the string to function method:
```python
# 
# Function Map
#
# manages the function map that is used for the
# string to function operations
#
class FunctionMap:
    """
    Manages a mapping of function names to function pointers. This allows for
    dynamic lookup and execution of functions by name.
    
    Attributes:
        function_map (dict): A dictionary that maps function names to function pointers.
    
    Methods:
        add_function(function_name_string, function_pointer):
            Adds a new function to the function map.
        get_function(function_name_string):
            Retrieves the function pointer for the given function name.
        get_all_entries():
            Returns a dictionary of all the function name to function pointer mappings.
        get_length():
            Returns the number of functions in the function map.
    """
    
    def __init__( self ) -> None:
        print( "initializing function map..." )
        self.function_map = {} 

    def add_function( self, function_name_string, function_pointer ):
        self.function_map[ function_name_string ] = function_pointer

    def get_function(self, function_name_string ):
        return self.function_map.get( function_name_string )

    def get_all_entries( self ):
        return self.function_map
    
    def get_length( self ):
        return len( self.function_map )
```

# Your Task
Rewrite the edit todo tool using the string to function method so that we can follow the Open/Closed Principle and not ever have to modify the edit todo tool code.
