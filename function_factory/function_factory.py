
from read_file_handler.read_file_handler import ReadFileHandler
from read_file_tool.read_file_tool import ReadFileTool
from write_file_handler.write_file_handler import WriteFileHandler
from write_file_tool.write_file_tool import WriteFileTool


class FunctionFactory:
    def __init__(self):
        # Initialize instances of tools that handlers may need
        self.read_file_tool = ReadFileTool()
        self.write_file_tool = WriteFileTool()
        # Initialize other tools if necessary

    def create_function_handler(self, function_name):
        """
        Creates and returns an instance of a FunctionHandler subclass based on the function_name.

        Args:
            function_name (str): The name of the function to create a handler for.

        Returns:
            FunctionHandler: An instance of a subclass of FunctionHandler.
        """
        if function_name == "read_file":
            return ReadFileHandler(self.read_file_tool)
        elif function_name == "write_file":
            return WriteFileHandler(self.write_file_tool)
        # Add additional handlers for other functions as needed
        else:
            return None  # or raise an exception if preferred
