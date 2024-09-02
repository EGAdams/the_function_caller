from read_file_tool.read_file_tool      import ReadFileTool
from todo_list_tools.add_todo_tool import AddTodoTool
from todo_list_tools.remove_todo_tool import RemoveTodoTool
from write_file_tool.write_file_tool    import WriteFileTool
from function_map.function_map          import FunctionMap
from make_directory_tool.make_directory_tool import MakeDirectoryTool
from change_directory_tool.change_directory_tool import ChangeDirectoryTool
from linux_command_tool.linux_command_tool import LinuxCommandTool
from get_current_directory_tool.get_current_directory_tool import GetCurrentDirectoryTool

class FileSystemMappedFunctions:
    def __init__( self ):
        self.function_map = FunctionMap()
        print( "initializing file system mapped functions..." )
        self.function_map.add_function( "write_file", WriteFileTool.write_file )
        self.function_map.add_function( "read_file" , ReadFileTool.read_file   )
        self.function_map.add_function( "make_directory", MakeDirectoryTool.make_directory )
        self.function_map.add_function( "change_directory", ChangeDirectoryTool.change_directory )
        self.function_map.add_function( "get_current_directory", GetCurrentDirectoryTool.get_current_directory )
        self.function_map.add_function( "execute_command", LinuxCommandTool.execute_command )
        self.function_map.add_function( "add_todo", AddTodoTool.add_todo )
        self.function_map.add_function( "remove_todo", RemoveTodoTool.remove_todo )

    def get_function_map( self ):
        return self.function_map