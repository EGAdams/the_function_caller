import os

class MakeDirectoryTool:
    """
    Provides a tool for creating a new directory.
    
    The `MakeDirectoryTool` class exposes a `make_directory` function that can be used to create a new directory. 
    The function takes a `directory_path` parameter that specifies the path of the directory to create.
    
    The `schema` method returns a JSON schema that describes the `make_directory` function, including its parameters and return value.
    """
    
    def __init__(self):
        print("initializing")

    def schema():
        return {
            "name": "make_directory",
            "description": "Create a new directory at the specified path",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "The full path of the directory to create."
                    }
                },
                "additionalProperties": False,
                "required": ["directory_path"]
            }
        }

    def make_directory(directory_path):
        """Creates a new directory at the specified path.
        
        Args:
            directory_path (str): The path of the directory to create.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return f"Directory '{directory_path}' created successfully."
        except Exception as e:
            return f"Error creating directory '{directory_path}': {str(e)}"