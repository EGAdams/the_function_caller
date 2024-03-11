#
# FunctionExecutor class
#
class FunctionExecutor:
    def __init__( self, available_functions ):
        '''
        Initialize the FunctionExecutor object with a dictionary of available functions.
        
        Args:
            available_functions (dict): A dictionary mapping function names to their implementations.
        '''
        self.available_functions = available_functions

    def execute_function( self, function_name, arguments ):
        '''
        Execute a function referenced by its name with provided arguments.
        
        Args:
            function_name (str): The name of the function to execute.
            arguments (dict): The arguments to pass to the function as keyword arguments.
        
        Returns:
            str: The result of the function execution or a message if the function is not recognized.
        '''
        if function_name in self.available_functions:
            return self.available_functions[ function_name ]( **arguments )
        
        return 'Function not recognized.'
