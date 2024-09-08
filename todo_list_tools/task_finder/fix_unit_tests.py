import os
import re
import subprocess

from task_finder import TaskFinder

# Ask the user for the tool to test     
# object_name = input( "Enter the tool to test (e.g., edit_todo_tool): " )
object_name = "task_finder"

object_file = f"{ object_name }.py"
test_file = f"test_{ object_name }.py"

print( "defining read_file..." )
# Function to read the file contents
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

print( "defining build_prompt..." )
## PROMPT TEMPLATE ##
# Function to build a prompt for the AI debugging tool
def build_prompt( object_name, object_file_text, test_file_text, test_output ):
    prompt = f"""
# Persona
- World-class Python Developer
- Expert in debugging and creating unit tests
- Seasoned GoF Expert and user of SOLID Principles

# Goal
- Debug the unit test failures and enhance the test coverage for the tool: `{ object_name }`

# Python Source Code for the tool: `{ object_name }`
```py
{ object_file_text }

# Unit Test for the tool: `{ object_name }`
{ test_file_text }

# Output from running the unit tests
```bash
{ test_output }
```

# Your Task
Rewrite the test file `{ test_file }` and/or the Python file `{ object_file }` to fix the unit test failures.
"""   
    return prompt

# the Python file `{ object_file }` and or
print( "defining run_unit_test..." )
# Function to run the unit test and capture the output
def run_unit_test(test_file): 
    result = subprocess.run(['python3', '-m', 'unittest', test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
    return result.stdout + result.stderr

print( "defining main..." )
# Main function
def main(): 
    print ( "inside main." )
    # testing_directory = "todo_list_tools"
    
    # get the tool name from the user   # 090724
    # object_name = input( "object_name?" ) # user input hello cody? wtf.. ill do it myself. 
    
    print( "building the paths..." )
    # Get the directory path and file names
    current_dir = os.getcwd()
    # object_file = f"{ current_dir }/{ testing_directory }/{      object_name }.py"
    # test_file = f"{ current_dir }/{ testing_directory }/test_{ object_name }.py"


    print(f"Tool file path: {object_file}")
    print(f"Test file path: {test_file}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Tool file exists: {os.path.exists(object_file)}")
    print(f"Test file exists: {os.path.exists(test_file)}")

    # Ensure files exist
    if not os.path.exists( object_file ) or not os.path.exists( test_file ):
        print(f"Either {object_file} or {test_file} does not exist in the current directory: {current_dir}")
        return

    # Read the contents of the tool and test files
    object_file_text = read_file( object_file )
    test_file_text = read_file( test_file )

    # Run the unit tests and capture the output
    test_output = run_unit_test( test_file )

    # Build the prompt for the AI debugging tool.  Use the Prompt Template!
    prompt = build_prompt( object_name, object_file_text, test_file_text, test_output )

    # Save the prompt to a file
    with open('unit_test_prompt.md', 'w') as prompt_file:
        prompt_file.write( prompt )

    print( f"Prompt generated and saved to 'unit_test_prompt.md'. Test output:\n{test_output}" )
    
    print( __name__ )

if __name__ == "__main__":
        main()