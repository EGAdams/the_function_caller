#
# FunctionExecutor class
#
class FunctionExecutor:
    def __init__( self, string_to_function_arg ):
        self.string_to_function = string_to_function_arg

    def execute_function( self, function_name, arguments ):
        '''
        Execute a function referenced by its name with provided arguments.
        
        Args:
            function_name (str): The name of the function to execute.
            arguments (dict): The arguments to pass to the function as keyword arguments.
        
        Returns:
            str: The result of the function execution or a message if the function is not recognized.
        '''
        function_to_run = self.string_to_function.create_function_from_string( function_name )
        if ( function_to_run != None ):
            return function_to_run( **arguments )
        else:
            return 'Function not recognized.'
