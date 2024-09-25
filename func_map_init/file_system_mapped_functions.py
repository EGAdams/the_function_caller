from read_file_tool.read_file_tool      import ReadFileTool
from todo_list_tools.add_todo_tool.add_todo_tool import AddTodoTool
from todo_list_tools.remove_todo_tool.remove_todo_tool import RemoveTodoTool
from todo_list_tools.read_todo_tool import ReadTodoTool
from write_file_tool.write_file_tool    import WriteFileTool
from function_map.function_map          import FunctionMap
from make_directory_tool.make_directory_tool import MakeDirectoryTool
from change_directory_tool.change_directory_tool import ChangeDirectoryTool
from linux_command_tool.linux_command_tool import LinuxCommandTool
from get_current_directory_tool.get_current_directory_tool import GetCurrentDirectoryTool
from todo_list_tools.storage_handler import StorageHandler

class FileSystemMappedFunctions:
    def __init__(self):
        self.function_map = FunctionMap()
        print("initializing file system mapped functions...")
        storage_handler = StorageHandler("todo_list.json")
        
        # Create instances of the tools
        write_file_tool = WriteFileTool()
        read_file_tool = ReadFileTool()
        make_directory_tool = MakeDirectoryTool()
        change_directory_tool = ChangeDirectoryTool()
        get_current_directory_tool = GetCurrentDirectoryTool()
        linux_command_tool = LinuxCommandTool()
        add_todo_tool = AddTodoTool( storage_handler )
        remove_todo_tool = RemoveTodoTool( "todo_list.json", storage_handler )
        read_todo_tool = ReadTodoTool()

        # Add bound methods to the function map
        self.function_map.add_function( "write_file", write_file_tool.write_file )
        self.function_map.add_function( "read_file", read_file_tool.read_file )
        self.function_map.add_function( "make_directory", make_directory_tool.make_directory )
        self.function_map.add_function( "change_directory", change_directory_tool.change_directory )
        self.function_map.add_function( "get_current_directory", get_current_directory_tool.get_current_directory )
        self.function_map.add_function( "execute_command", linux_command_tool.execute_command )
        self.function_map.add_function( "add_todo", add_todo_tool.add_todo )
        self.function_map.add_function( "remove_todo", remove_todo_tool.remove_todo )

        self.function_map.add_function( "read_todo_list", read_todo_tool.read_todo_list )
    def get_function_map(self):
        return self.function_map
