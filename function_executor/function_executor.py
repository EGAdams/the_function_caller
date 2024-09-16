#
# FunctionExecutor class
#
# since the function executor needs to create a function from a string,
# it needs to be instantiated with it's main partner.  I'm not sure how 
# this code would work without creating a function from a string.
#
class FunctionExecutor:
    def __init__(self, string_to_function_arg):
        self.string_to_function = string_to_function_arg

    def execute_function(self, function_name, arguments):
        '''
        Execute a function referenced by its name with provided arguments.
        
        Args:
            function_name (str): The name of the function to execute.
            arguments (dict): The arguments to pass to the function as keyword arguments.
        
        Returns:
            str: The result of the function execution or a message if the function is not recognized.
        '''
        
        function_to_run = self.string_to_function.create_function_from_string(function_name)
        if function_to_run is not None:
            if isinstance(function_to_run, type):
                # If it's a class, instantiate it and call the method
                instance = function_to_run()
                method_name = function_name.split('.')[-1]
                method = getattr(instance, method_name)
                return method(**arguments)
            elif callable(function_to_run):
                # If it's a function or static method, call it directly
                return function_to_run(**arguments)
            else:
                # If it's an instance method already bound to an instance
                return function_to_run(**arguments)
        else:
            return 'Function not recognized.'
