import json
import os
import sys

class StorageHandler:
    """Handles the loading and saving of the todo list to/from a file."""

    def __init__(self, filename="todo_list.json"):
        self.filename = filename

    def show_path( self ):
        # show the current path of this process:
        import os
        current_path = os.getcwd()
        if ( current_path != "/home/adamsl/the_function_caller/todo_list_tools" ):
            print ( "*** Warning: not a tested current path. *** " )
        print( "Current path:", current_path )
        print( "storage file name: " + self.filename )


    def load(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, todo_list):
        with open(self.filename, 'w') as file:
            json.dump(todo_list, file, indent=2)
        
        with open( self.filename + ".bak", 'w' ) as file:
            json.dump( todo_list, file, indent=2 )
