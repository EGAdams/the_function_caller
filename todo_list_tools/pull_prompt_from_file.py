# Load the template from the file
with open('/home/eg1972/the_function_caller/todo_list_tools/store_template.md', 'r') as file:
    prompt_template = file.read()

# Format the template with dynamic values
tool_name = 'edit_todo_tool'
tool_file_text = 'def edit_todo_tool(...): pass'  # Example tool code
test_file_text = 'def test_edit_todo_tool(...): pass'  # Example test code
test_output = 'Ran 1 test in 0.01s\nOK'  # Example test output
test_file = 'test_edit_todo_tool.py'

# Format the template
prompt = prompt_template.format(
    tool_name=tool_name,
    tool_file_text=tool_file_text,
    test_file_text=test_file_text,
    test_output=test_output,
    test_file=test_file
)

print(prompt)

