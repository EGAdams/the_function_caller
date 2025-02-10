import os

class CreateDirectoryTool:
    """
    Provides a tool for creating directories.

    The `CreateDirectoryTool` class exposes a `create_directory` function that can be used to create a new directory at a specified path.

    The `schema` method returns a JSON schema that describes the `create_directory` function, including its parameters and return value.
    """

    def __init__(self):
        print("Initializing CreateDirectoryTool")

    @staticmethod
    def schema():
        return {
            "name": "create_directory",
            "description": "Creates a directory at the specified path.",
            "strict": False,
            "parameters": {
                "properties": {
                    "directory_path": {
                        "description": "The complete path of the directory to be created.",
                        "title": "Directory Path",
                        "type": "string"
                    }
                },
                "required": ["directory_path"],
                "type": "object"
            }
        }

    def create_directory(self, directory_path: str):
        """
        Creates a directory at the specified path.

        Args:
            directory_path (str): The full path of the directory to create.

        Returns:
            str: A message indicating success or failure.
        """
        sanitized_path = os.path.abspath(directory_path)
        print(f"Debug: Sanitized directory_path = {sanitized_path}")

        try:
            os.makedirs(sanitized_path, exist_ok=True)
            return f"Directory created successfully at {sanitized_path}."
        except Exception as e:
            print(f"Error creating directory: {e}")
            return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    tool = CreateDirectoryTool()
    print(tool.schema())
    response = tool.create_directory("./test_directory")
    print(response)
