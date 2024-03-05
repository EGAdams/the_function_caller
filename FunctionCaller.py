# this is the interface between the llm and 
# functions being called on this machine by the
# llm.
#!pip install scipy --quiet
#!pip install tenacity --quiet
#!pip install tiktoken --quiet
#!pip install termcolor --quiet
#!pip install openai --quiet

import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read.",
                    }
                },
                "required": ["filename"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to write to.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file.",
                    },
                },
                "required": ["filename", "content"],
            },
        }
    },
]

def write_file(filename, content):
    """Writes content to a specified file.
    
    Args:
        filename (str): The name of the file to write to.
        content (str): The content to write to the file.
    """
    with open(filename, 'w') as file:
        file.write(content)
    return "File written successfully."

def read_file(filename):
    """Reads content from a specified file.
    
    Args:
        filename (str): The name of the file to read from.
    
    Returns:
        str: The content of the file.
    """
    with open(filename, 'r') as file:
        return file.read()

def execute_function( function_json ):
    """Parses a JSON object to execute a function based on the name and parameters.
    
    Args:
        function_json (str): A JSON string containing the function name and parameters.
        
    Returns:
        str: The result of the function execution.
    """
    
    # Parse the JSON string into a Python dictionary
    function_data = json.loads(function_json)
    
    # Extract the function name and parameters
    function_name = function_data.get("function")
    parameters = function_data.get("parameters", {})
    
    # Match the function name to the actual function and execute it
    if function_name == "write_file":
        return write_file(parameters.get("filename"), parameters.get("content"))
    elif function_name == "read_file":
        return read_file(parameters.get("filename"))
    else:
        return "Function not recognized."

# Example JSON object for writing to a file
function_json_write = json.dumps({
    "function": "write_file",
    "parameters": {
        "filename": "example.txt",
        "content": "This is an example content."
    }
})

# Execute the write function
result = execute_function(function_json_write)
print(result)

# Example JSON object for reading from a file
function_json_read = json.dumps({
    "function": "read_file",
    "parameters": {
        "filename": "example.txt"
    }
})

# Execute the read function and print the file content
file_content = execute_function(function_json_read)
print(file_content)


# Example usage
if __name__ == "__main__":
    # Example of writing to a file
    write_result = write_file( "example.txt", "This is some new content.")
    print("Write result:", write_result)

    # Example of reading from a file
    read_content = read_file( "example.txt" )
    print("Read from file:", read_content)
    