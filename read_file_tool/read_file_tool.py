#
# spring hill pf.  lecture about html, php and mysterious tools
#
class ReadFileTool:
    """
    Provides a tool for reading the contents of a file.
    
    The `ReadFileTool` class exposes a `read_file` function that can be used to read the contents of a file. The function takes a `file_path` parameter that specifies the path and the name of the file to read.
    
    The `schema` method returns a JSON schema that describes the `read_file` function, including its parameters and return value.
    """
    
    def __init__( self ):
        print ( "initialaizing" )

    def schema(): 
        return {
            "name": "read_file_tool",
            "description": "This tool reads a file and returns the contents.",
            "strict": False,
            "parameters": {
                "properties": {
                "file_path": {
                    "description": "Path to the file to read with extension.",
                    "examples": [
                    "/home/adamsl/the_function_caller/info.txt",
                    "./file.txt",
                    "./file.json",
                    "../../file.py"
                    ],
                    "title": "File Path",
                    "type": "string"
                }
                },
                "required": [
                "file_path"
                ],
                "type": "object"
            }
        }

    def read_file( self, filename ):
        """Reads content from a specified file.
        
        Args:
            filename (str): The name of the file to read from.
        
        Returns:
            str: The content of the file.
        """
        # morph the file name since the assistant seems to be looking at it's sandbox
        filename = filename.replace( '/mnt/data/', '' )
        with open( filename, 'r' ) as file:
            return file.read()
