#
# ToolManager
#
class ToolManager:
    def get_tools( self ):
        #
        # we start with giving the model the ability to read and write files
        #
        tools = [
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
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "The name of the file to write to.",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content to write to the file.",
                            },
                        },
                        "required": ["filename", "content"],
                    },
                }
            },
        ]
        
        return tools
