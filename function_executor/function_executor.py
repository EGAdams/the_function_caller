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
        """
        Execute a function referenced by its name with provided arguments.

        Args:
            function_name (str): The name of the function to execute.
            arguments (dict): The arguments to pass to the function as keyword arguments.

        Returns:
            str: The result of the function execution or a message if the function is not recognized.
        """
        print(f"Debug: function_name = {function_name}")
        print(f"Debug: arguments before execution = {arguments}")

        try:
            # Retrieve the function or class to execute
            function_to_run = self.string_to_function.create_function_from_string(function_name)
            print(f"Debug: Retrieved function_to_run = {function_to_run}")

            if function_to_run is None:
                return 'Function not recognized.'

            if callable(function_to_run):
                print(f"Debug: {function_name} is callable. Executing it with arguments {arguments}")

                # Ensure arguments are passed as **kwargs
                if not isinstance(arguments, dict):
                    raise ValueError(f"Expected a dictionary for arguments, got: {type(arguments)}")

                return function_to_run(**arguments)

            return 'Invalid function type.'

        except Exception as e:
            print(f"Error during execution: {e}")
            return f"Error: {e}"

        