#
# spring hill pf.  lecture about html, php and mysterious tools
#
class ReadFileTool:
    """
    Provides a tool for reading the contents of a file.
    
    The `ReadFileTool` class exposes a `read_file` function that can be used to read the contents of a file. The function takes a `filename` parameter that specifies the name of the file to read.
    
    The `schema` method returns a JSON schema that describes the `read_file` function, including its parameters and return value.
    """
    def __init__( self ):
        print ( "initialaizing" )

    def schema(): 
        return '''
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "The name of the file to read.",
                            }
                        },
                        "required": ["filename"],
                    },
                }
            }
            '''
    
    def read_file(filename):
        """Reads content from a specified file.
        
        Args:
            filename (str): The name of the file to read from.
        
        Returns:
            str: The content of the file.
        """
        with open(filename, 'r') as file:
            return file.read()
