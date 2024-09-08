import os
import re

def find_python_files(directory):
    """Recursively find all Python files in the specified directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            # skip the __init__.py files
            if ( file == '__init__.py' or 
                 file == 'fix_unit_tests.py' or
                 file == 'run_all_tests.py' or
                 file == 'all_classes.py'
                 ):
                continue
            # skip files that begin with test_
            if ( file.startswith('test_') ):
                continue
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_classes_from_file(filepath):
    """Extract class definitions from a Python file."""
    class_pattern = re.compile(r'^\s*class\s+\w+.*:')
    classes = []
    
    with open(filepath, 'r') as file:
        inside_class = False
        class_lines = []
        indent_level = None
        
        for line in file:
            # Check if the line contains a class definition
            if class_pattern.match(line):
                # If we're inside a class, store the current class and reset
                if inside_class:
                    classes.append("".join(class_lines))
                # Start capturing a new class
                inside_class = True
                class_lines = [line]
                indent_level = len(line) - len(line.lstrip())
            elif inside_class:
                current_indent = len(line) - len(line.lstrip())
                
                # End the class when the indentation level changes or the line is empty
                if current_indent > indent_level or line.strip() == "":
                    class_lines.append(line)
                else:
                    inside_class = False
                    classes.append("".join(class_lines))
                    class_lines = []
                    indent_level = None
        
        # If we reached the end of the file and were inside a class
        if inside_class:
            classes.append("".join(class_lines))

    return classes



def append_classes_to_file(classes, output_file):
    """Append the extracted class definitions to the output file."""
    with open(output_file, 'a') as file:
        for class_def in classes:
            file.write(class_def)
            file.write("\n\n")

def main():
    current_directory = os.getcwd()
    print( "current directory: " + current_directory )
    output_file = 'all_classes.py'

    # Clear the content of the output file if it already exists
    with open(output_file, 'w') as file:
        file.write("# All classes from Python files in the directory\n\n")

    # Find all Python files in the current directory
    python_files = find_python_files(current_directory)
    # print the python files separated by "\n"
    for python_file in python_files:
        print(python_file)

    # Extract classes from each Python file and append to the output file
    for python_file in python_files:
        classes = extract_classes_from_file(python_file)
        append_classes_to_file(classes, output_file)

if __name__ == "__main__":
    main()
