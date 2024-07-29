# from termcolor import colored  
   
#
    # Define the pretty print conversation
    #
    # def pretty_print_conversation( messages ):
    #     role_to_color = {
    #         "system": "red",
    #         "user": "green",
    #         "assistant": "blue",
    #         "function": "magenta" }
    
    #     for message in messages:
    #         if message == None:
    #             continue
    #         if message["role"] == "system":
    #             print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
    #         elif message["role"] == "user":
    #             print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
    #         elif message["role"] == "assistant" and message.get("function_call"):
    #             print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
    #         elif message["role"] == "assistant" and not message.get("function_call"):
    #             print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
    #         elif message["role"] == "function":
    #             print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

def execute_function( function_json ):
    """Parses a JSON object to execute a function based on the name and parameters.
    
    Args:
        function_json (str): A JSON string containing the function name and parameters.
        
    Returns:
        str: The result of the function execution.
    """
    
    # Parse the JSON string into a Python dictionary
    function_data = json.loads( function_json)
    
    # Extract the function name and parameters
    function_name = function_data.get( "function" )
    parameters = function_data.get( "parameters", {})
    
    # Match the function name to the actual function and execute it
    if function_name == "write_file":
        return write_file( parameters.get( "filename" ), parameters.get( "content" ))
    elif function_name == "read_file":
        return read_file( parameters.get( "filename" ))
    else:
        return "Function not recognized."
    
    # from termcolor import colored  

# def pretty_print( messages ):
#     print( "\n\n" )
#     print( "# Messages" )
#     for m in messages:
#         print( f"{ m.role }: { m.content[ 0 ].text.value }" )
#     print()

def wait_on_run( run, thread ):
    print ( "entering while.  run status is: " + run.status )
    while run.status == "queued" or \
          run.status == "in_progress" or \
          run.status == "requires_action":
              
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep( 0.5 )
        print( "done sleeping.  checking for any action required..." )
        if run.status == "requires_action":
            print( "found action required.  sending the run for processing..." )
            messages = client.beta.threads.messages.list( thread_id=thread.id )
            actionHandler = ActionHandler( messages, run )
            actionHandler.execute( thread.id ) # modifies run for now...
    
    print( f"Run { run.id } is { run.status }." )
    return run