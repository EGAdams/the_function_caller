from agents.agent_urls import AgentUrlProvider
from read_file_tool.read_file_tool      import ReadFileTool
from send_message_tool.send_message_tool import SendMessageTool
from todo_list_tools.add_todo_subtask_tool.add_todo_subtask_tool import AddTodoSubtaskTool
from todo_list_tools.read_todo_tool import ReadTodoTool
from write_file_tool.write_file_tool    import WriteFileTool
from function_map.function_map          import FunctionMap
from make_directory_tool.make_directory_tool import MakeDirectoryTool
from change_directory_tool.change_directory_tool import ChangeDirectoryTool
from linux_command_tool.linux_command_tool import LinuxCommandTool
from get_current_directory_tool.get_current_directory_tool import GetCurrentDirectoryTool
from todo_list_tools.storage_handler import StorageHandler

class FileSystemMappedFunctions:
    def __init__( self ):
        self.function_map = FunctionMap()
        print("initializing file system mapped functions...")
        storage_handler = StorageHandler("todo_list.json")
       
        # Create instances of the tools
        send_message_tool       = SendMessageTool( AgentUrlProvider.get_agent_urls())
        write_file_tool         = WriteFileTool()
        read_file_tool          = ReadFileTool()
        mkdir_tool              = MakeDirectoryTool()
        change_directory_tool   = ChangeDirectoryTool()
        get_cd_tool             = GetCurrentDirectoryTool()
        linux_command_tool      = LinuxCommandTool()
        add_todo_subtask_tool   = AddTodoSubtaskTool( storage_handler )
        read_todo_tool          = ReadTodoTool()

        # Add bound methods to the function map
        self.function_map.add_function( "write_file",            write_file_tool.write_file )
        self.function_map.add_function( "read_file",             read_file_tool.read_file )
        self.function_map.add_function( "make_directory",        mkdir_tool.make_directory )
        self.function_map.add_function( "change_directory",      change_directory_tool.change_directory )
        self.function_map.add_function( "get_current_directory", get_cd_tool.get_current_directory )
        self.function_map.add_function( "execute_command",       linux_command_tool.execute_command )
        self.function_map.add_function( "add_todo",              add_todo_subtask_tool.add_todo_subtask )
        self.function_map.add_function( "read_todo_list",        read_todo_tool.read_todo_list )
        self.function_map.add_function( "send_message",          send_message_tool.send_message )
        
    def get_function_map( self ):
        return self.function_map
