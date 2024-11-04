import sys
import os
# sys.path.append( '/home/adamsl/the_function_caller/todo_list_tools' )
# Add the parent directory of the current file (task_list) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage_handler.storage_handler import StorageHandler
from add_todo_tool.add_todo_tool import AddTodoTool

def main():
    # Get task from user
    print("\nEnter your new task:")
    task_description = input("> ")

    # snake case the task description to snake_case so it can be used as a filename
    filename = task_description.replace(" ", "_")
    
    # Initialize storage handler with a new file name with .json at the end
    storage = StorageHandler( filename + ".json" )
    
    # Create the add todo tool
    todo_tool = AddTodoTool(storage)
    
    # Add the task and show result
    result = todo_tool.add_todo(task_description)
    print(result)

if __name__ == "__main__":
    main()
