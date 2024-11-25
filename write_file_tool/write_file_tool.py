#
# spring hill pf  got led matrix almost straightened out.  just kept compiling and swapping out until it worked.
#
class WriteFileTool:
    """
    Provides a tool for writing the contents of a file.
    The `WriteFileTool` class exposes a `write_file` function that can be used to write a string to a file with the specified filename.
    The `schema` method returns a JSON schema that describes the parameters expected by the `write_file` function.
    """
    
    def __init__( self ):
        print ( "initialaizing" )

    @staticmethod
    def schema():
        return {
            "name": "write_file",
            "description": "Allows you to write new files.",
            "strict": False,
            "parameters": {
                "properties": {
                "chain_of_thought": {
                    "description": "Please think step-by-step about what needs to be written to the file in order for the program to match the requirements.",
                    "title": "Chain Of Thought",
                    "type": "string"
                },
                "file_path": {
                    "description": "The full path of the file to write.",
                    "type": "string"
                },
                "content": {
                    "description": "The full content of the file to write. Content must not be truncated and must represent a correct functioning program with all the imports defined.",
                    "type": "string"
                }
                },
                "required": [
                "file_path",
                "content"
                ],
                "type": "object"
            }
        }
    
    def write_file( self, file_path, content ):
        """Writes content to a specified file.
        
        Args:
            file_path (str): The full path of the file to write to.
            content (str): The content to write to the file.
        """
        
        print ( "opening file with arguments: " + file_path + " and " + content )
        with open( file_path, 'w' ) as file:
            file.write( content )

        return "File written successfully."