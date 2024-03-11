#
#  FunctionExecutor class
#
class FunctionExecutor:
    def __init__( self, available_functions ):
        self.available_functions = available_functions

    def execute_function( self, function_name, arguments ):
        if function_name in self.available_functions:
            return self.available_functions[ function_name ]( **arguments )
        
        return "Function not recognized."
