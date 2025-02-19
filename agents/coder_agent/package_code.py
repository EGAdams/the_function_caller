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
output_file_path        = os.path.join( base_dir, "agents/coder_agent/packaged_code.md"       )
todo_list_tools_task    = os.path.join( base_dir, "todo_list_tools/task"                      )
task_iterator_path      = os.path.join( base_dir, "todo_list_tools/task_finder/task_iterator" )
task_finder_path        = os.path.join( base_dir, "todo_list_tools/task_finder/"              )
add_todo_subtask_path   = os.path.join( base_dir, "todo_list_tools/add_todo_subtask_tool"     )
edit_todo_subtask_path  = os.path.join( base_dir, "todo_list_tools/edit_todo_subtask_tool"    )

# Agents
agents_file_path        = os.path.join( base_dir, "agents"                                    )
base_agent_path         = os.path.join( base_dir, "agents/base_agent"                         )
coder_agent_path        = os.path.join( base_dir, "agents/coder_agent"                        )
planner_agent_path      = os.path.join( base_dir, "agents/planner_agent"                      )
message_collab_path     = os.path.join( base_dir, "agents/message_collaborator_agent"         )

commands_path           = os.path.join( base_dir, "commands"                                  )
command_path            = os.path.join( base_dir, "commands/command"                          )
process_message_path    = os.path.join( base_dir, "commands/process_message_command"          )

read_file_tool_path     = os.path.join( base_dir, "read_file_tool"                            )
write_file_tool_path    = os.path.join( base_dir, "write_file_tool"                           )



# path = os.path.join( planner_agent_path, "planner_agent_exe.py"             )
# process_python_file( path, output_file_path, append_mode=True               )

# path = os.path.join( message_collab_path, "collaborator.py"                 )
# process_python_file( path, output_file_path, append_mode=True               )

# path = os.path.join( agents_file_path, "start_collaborating.py"             )
# process_python_file( path, output_file_path, append_mode=False              )

# Construct the full path
path = os.path.join(agents_file_path, "coder_agent/package_code_begin.md")

# Open the output file in write mode
with open(output_file_path, 'w') as output_file:
    # Read the contents of package_code_begin.md and write them to the output file
    with open(path, 'r') as file:
        output_file.write(file.read())
        
# process_python_file( path, output_file_path, append_mode=False              )

path = os.path.join( base_agent_path, "base_agent.py"                       )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( coder_agent_path, "coder_agent_exe.py"                 )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( coder_agent_path, "test_agent.py"                      )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( coder_agent_path, "chat_w_agents.py"                   )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( command_path, "i_command.py"                           )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( process_message_path, "process_message_command.py"     )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( read_file_tool_path, "read_file_tool.py"               )
process_python_file( path, output_file_path, append_mode=True               )

path = os.path.join( write_file_tool_path, "write_file_tool.py"             )
process_python_file( path, output_file_path, append_mode=True               )
