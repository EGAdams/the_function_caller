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
        if ( self.function_map.get_length() == 0 ):
            print( "*** Error: No functions initialized in the StringToFunction Object. ***" )
            return None
        
        function_maps = self.function_map.get_all_entries()
        if function_name in function_maps:
            return self.function_map.get_function( function_name )
        else:
            return None