import os

class GetCurrentDirectoryTool:
    """
    Provides a tool for getting the current working directory.
    
    The `GetCurrentDirectoryTool` class exposes a `get_current_directory` function that can be used to retrieve the current working directory.
    
    The `schema` method returns a JSON schema that describes the `get_current_directory` function, including its parameters and return value.
    """
    
    def __init__(self):
        print("initializing")

    def schema():
        return {
            "name": "get_current_directory",
            "type": "function",
            "function": {
                "name": "get_current_directory",
                "description": "Get the current working directory",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def get_current_directory():
        """Retrieves the current working directory.
        
        Returns:
            str: The path of the current working directory.
        """
        try:
            current_dir = os.getcwd()
            return f"Current working directory: {current_dir}"
        except Exception as e:
            return f"An error occurred while getting the current directory: {str(e)}"