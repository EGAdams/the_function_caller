import os
import ast

def extract_classes_and_functions(content):
    """
    Extracts all classes and functions from the given Python content.
    Returns a list of code snippets as strings.
    """
    extracted_code = []
    tree = ast.parse(content)

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            # Get the full source code for the class or function
            class_or_func = ast.get_source_segment(content, node)
            if class_or_func:
                extracted_code.append(class_or_func)
    
    return extracted_code

def process_python_file(input_path, output_file_path, append_mode=False):
    """
    Processes a single Python file to extract classes and functions
    and writes them to the output file in Markdown format.
    """
    with open(input_path, 'r', encoding='utf-8') as python_file:
        content = python_file.read()
        code_snippets = extract_classes_and_functions(content)
        if code_snippets:
            with open(output_file_path, 'a' if append_mode else 'w', encoding='utf-8') as output_file:
                for snippet in code_snippets:
                    output_file.write(f"```python\n{snippet}\n```\n\n")

def process_python_files_in_directory(input_dir, output_file_path):
    """
    Processes all Python files in the given directory (and subdirectories)
    to extract classes and functions and append them to the output file.
    """
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith(".py"):
                full_path = os.path.join(root, file_name)
                append = os.path.exists(output_file_path)
                process_python_file(full_path, output_file_path, append_mode=True)

# Path setup
base_dir = "/home/adamsl/the_function_caller"
project_dir = os.path.join(base_dir, "todo_list_tools")
view_controllers_dir = os.path.join(project_dir, "view_controllers")
custom_views_dir = os.path.join(project_dir, "custom_views")
table_view_cell_dir = os.path.join(project_dir, "custom_views/table_view_cell")
factories_dir = os.path.join(project_dir, "factories")
keyboard_scroll_dir = os.path.join(project_dir, "keyboard_scroll")


# /home/adamsl/the_function_caller/  # todo_list_tools/task_finder/task_iterator/task_iterator.py
output_file_path       = os.path.join( base_dir, "packaged_code.md"                          )
todo_list_tools_task   = os.path.join( base_dir, "todo_list_tools/task"                      )
task_iterator_path     = os.path.join( base_dir, "todo_list_tools/task_finder/task_iterator" )
task_finder_path       = os.path.join( base_dir, "todo_list_tools/task_finder/"              )
add_todo_subtask_path  = os.path.join( base_dir, "todo_list_tools/add_todo_subtask_tool"     )
edit_todo_subtask_path = os.path.join( base_dir, "todo_list_tools/edit_todo_subtask_tool"    )

# /home/adamsl/the_function_caller/todo_list_tools/add_todo_subtask_tool/add_todo_subtask_tool.py
path = os.path.join( todo_list_tools_task, "task.py"                        )
process_python_file( path, output_file_path, append_mode=False              )

# path = os.path.join( task_iterator_path, "task_iterator.py"               )
# process_python_file( path, output_file_path, append_mode=True             )   

# path = os.path.join( task_finder_path, "task_finder.py"                     )
# process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( add_todo_subtask_path, "add_todo_subtask_tool.py"      )
process_python_file( path, output_file_path, append_mode=True               )

# path = os.path.join( add_todo_subtask_path, "add_todo_subtask_tool.py"      )
# process_python_file( path, output_file_path, append_mode=True               )

# path = os.path.join( add_todo_subtask_path, "test_add_todo_subtask_tool.py" )
# process_python_file( path, output_file_path, append_mode=True               )

# path = os.path.join( edit_todo_subtask_path, "edit_todo_subtask_tool.py" )
# process_python_file( path, output_file_path, append_mode=True            )

