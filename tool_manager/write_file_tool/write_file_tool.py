#
# spring hill pf  got led matrix almost straightened out.  just kept compiling and swapping
# out until it worked.
#
class WriteFileTool:
    def __init__( self ):
        print ( "initialaizing" )

    def schema():
        return '''
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "The name of the file to write.",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content to write to the file.",
                            }
                        },
                        "required": ["filename", "content"],
                    },
                }
            }
            '''
    
    def write_file( filename, content ):
        """Writes content to a specified file.
        
        Args:
            filename (str): The name of the file to write to.
            content (str): The content to write to the file.
        """
        
        with open( filename, 'w' ) as file:
            file.write( content )

        return "File written successfully."