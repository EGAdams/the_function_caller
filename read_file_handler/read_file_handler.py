from function_handler.ifunction_handler import IFunctionHandler # import IFunctionHandler Interface
from read_file_tool.read_file_tool import ReadFileTool

# ReadFileHandler implementation
class ReadFileHandler( IFunctionHandler ):
    def __init__(self):
        self.read_file_tool = ReadFileTool()

    def execute(self, parameters: dict) -> str:
        """
        Executes the read file operation using the ReadFileTool.

        Args:
            parameters (dict): A dictionary containing the 'filename' key.

        Returns:
            str: The content of the file.

        Raises:
            ValueError: If 'filename' is not provided in parameters.
        """
        filename = parameters.get('filename')
        if not filename:
            raise ValueError("The 'filename' parameter is required.")

        return self.read_file_tool.read_file(filename)
