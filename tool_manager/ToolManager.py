#
# ToolManager
#
from read_file_tool.read_file_tool import ReadFileTool
from write_file_tool.write_file_tool import WriteFileTool


class ToolManager:
    def get_tool_schemas( self ):
        #
        # we start with giving the model the ability to read and write files
        #
        tools = [ 
                    ReadFileTool.schema(), 
                    WriteFileTool.schema()
                ]
        
        return tools
