import os

class ChangeDirectoryTool:
    """
    Provides a tool for changing the current working directory.
    
    The `ChangeDirectoryTool` class exposes a `change_directory` function that can be used to change the current working directory. The function takes a `path` parameter that specifies the new directory path.
    
    The `schema` method returns a JSON schema that describes the `change_directory` function, including its parameters and return value.
    """
    
    def __init__(self):
        print("initializing")

    def schema():
        return {
            "type": "function",
            "function": {
                "name": "change_directory",
                "description": "Change the current working directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the directory to change to."
                        }
                    },
                    "required": ["path"]
                }
            }
        }

    def change_directory(path):
        """Changes the current working directory.
        
        Args:
            path (str): The path of the directory to change to.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            os.chdir(path)
            return f"Successfully changed directory to: {os.getcwd()}"
        except FileNotFoundError:
            return f"Directory not found: {path}"
        except PermissionError:
            return f"Permission denied: {path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"