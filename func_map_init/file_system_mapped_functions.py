#
# FileSystemMappedFunctions
#
# These tools operate on the file system in different ways.
#
from read_file_tool.read_file_tool import ReadFileTool
from write_file_tool.write_file_tool import WriteFileTool
from function_map.function_map import FunctionMap

class FileSystemMappedFunctions:
    def __init__( self ):
        self.function_map = FunctionMap()
        print( "initializing file system mapped functions..." )
        self.function_map.add_function( "write_file", WriteFileTool.write_file )
        self.function_map.add_function( "read_file" , ReadFileTool.read_file   )

    def get_function_map( self ):
        return self.function_map