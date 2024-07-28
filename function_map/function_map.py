# 
# Function Map
#
# manages the function map that is used for the
# string to function operations
#
class FunctionMap:
    """
    Manages a mapping of function names to function pointers. This allows for
    dynamic lookup and execution of functions by name.
    
    Attributes:
        function_map (dict): A dictionary that maps function names to function pointers.
    
    Methods:
        add_function(function_name_string, function_pointer):
            Adds a new function to the function map.
        get_function(function_name_string):
            Retrieves the function pointer for the given function name.
        get_all_entries():
            Returns a dictionary of all the function name to function pointer mappings.
        get_length():
            Returns the number of functions in the function map.
    """
    
    def __init__( self ) -> None:
        print( "initializing function map..." )
        self.function_map = {} 

    def add_function( self, function_name_string, function_pointer ):
        self.function_map[ function_name_string ] = function_pointer

    def get_function(self, function_name_string ):
        return self.function_map.get( function_name_string )

    def get_all_entries( self ):
        return self.function_map
    
    def get_length( self ):
        return len( self.function_map )

