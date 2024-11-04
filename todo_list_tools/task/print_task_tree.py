import json
import sys
# import task
from task import Task

def display_tree_with_ids(task, indent=""):
    """Display task and subtasks in a tree format with IDs."""
    tree_output = f"{indent}├── [{ task.id }] {task.task}\n"
    for i, subtask in enumerate(task.subtasks):
        is_last = i == len(task.subtasks) - 1
        next_indent = indent + ("    " if is_last else "│   ")
        tree_output += display_tree_with_ids(subtask, next_indent)
    return tree_output

def main():
    # get the full path to the JSON file from argument.  If there is no argument, use the "task.json" file in the current directory
    if len(sys.argv) > 1:
        json_file_path = sys.argv[ 1 ]
    else:
        json_file_path = "/home/adamsl/the_function_caller/todo_list_tools/task/task_config.json"
        
    # Read the JSON file
    with open( json_file_path, 'r') as file:
        task_data = json.load(file)
    
    # Create Task object
    root_task = Task( task_data [ 0 ])
    
    # Print the tree
    print("\nTask Tree with IDs:")
    print(display_tree_with_ids(root_task))

if __name__ == "__main__":
    main()