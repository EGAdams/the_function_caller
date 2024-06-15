#
#  creates a live function from a string
#
class StringToFunction:
    def __init__( self, function_map_arg ):
        '''
        Initialize the StringToFunction object with a dictionary of available functions.
        
        Args:
            function_map_arg (dict): A dictionary mapping function names to their implementations.
        '''
        self.function_map = function_map_arg

    def create_function_from_string( self, function_name ):
        '''
        Create a function from a string.

        Args:
            function_string (str): The string representation of the function.

        Returns:
            function: The function object.
        '''
        if function_name in self.function_map:
            return self.function_map[ function_name ]
        else:
            return None