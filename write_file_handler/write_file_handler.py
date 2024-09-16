# Assuming that FunctionHandler is an interface or abstract base class you've defined
# with an execute method that accepts a parameters dictionary.
from function_handler.ifunction_handler import IFunctionHandler

class WriteFileHandler( IFunctionHandler ):
    def __init__(self, write_file_tool):
        """
        Initializes the WriteFileHandler with a WriteFileTool instance.

        Args:
            write_file_tool (WriteFileTool): An instance of WriteFileTool.
        """
        self.write_file_tool = write_file_tool

    def execute( self, parameters ):
        """
        Executes the write file operation.

        Args:
            parameters (dict): A dictionary containing 'filename' and 'content'.

        Returns:
            str: A confirmation message or error message.
        """
        # Extract parameters
        filename = parameters.get('filename')
        content = parameters.get('content')

        # Validate parameters
        if not filename or content is None:
            return "Error: 'filename' and 'content' parameters are required."

        # Call the write_file method of WriteFileTool
        try:
            self.write_file_tool.write_file(filename, content)
            return f"File '{filename}' has been written successfully."
        except Exception as e:
            return f"Error writing file: {str(e)}"
