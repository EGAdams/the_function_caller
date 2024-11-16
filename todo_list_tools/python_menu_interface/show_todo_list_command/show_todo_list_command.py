#
# ShowTodoListCommand implements IMenuCommand
#
import sys
sys.path.append('/home/adamsl/the_function_caller/')
from todo_list_tools.python_menu_interface.menu_command.i_menu_command import IMenuCommand
from todo_list_tools.task.task import Task

class ShowTodoListCommand(IMenuCommand):
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler

    def convert_tree_to_markdown( self, tree_input ):
        markdown_lines = []
        for line in tree_input.strip().split('\n'):
            # Find the index of '├' or '└'
            idx = line.find('├')
            if idx == -1:
                idx = line.find('└')
            if idx == -1:
                continue  # Skip lines that don't have '├' or '└'
            # Compute the level
            level = idx // 4
            # Extract the content after '├───' or '└───'
            content = line[idx + 4:].strip()
            # Append to markdown lines with proper indentation
            markdown_lines.append('  ' * level + '* ' + content)
        return '\n'.join(markdown_lines)
    
    def execute( self ):
        todo_list = self.storage_handler.load()
        if todo_list:
            for todo_dict in todo_list:
                task = Task(todo_dict)
                print(task.display_tree())
                markdown_output = self.convert_tree_to_markdown( task.display_tree())
                # put the markdown output in a file
                with open( "/home/adamsl/the_function_caller/todo_list_tools/todo_list.md", "w" ) as f:
                    f.write( markdown_output )
        else:
            print("No tasks in the TODO list.")
        import time
        time.sleep(1)
