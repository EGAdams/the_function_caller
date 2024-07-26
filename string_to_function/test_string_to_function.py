# Let's write the testing code and run it in the Python environment.
import unittest

# Assuming the following is the implementation of string_to_function.py for testing purposes.
def hello():
    return "Hello, world!"

def goodbye():
    return "Goodbye, world!"

# Simulate the call_function that maps strings to functions
def call_function(func_name):
    functions = {
        'hello': hello,
        'goodbye': goodbye,
    }
    return functions[func_name]()

# Now let's define the unit tests
class TestStringToFunction(unittest.TestCase):

    def test_valid_function_call(self):
        self.assertEqual(call_function('hello'), 'Hello, world!')

    def test_invalid_function_call(self):
        with self.assertRaises(KeyError):
            call_function('non_existent_function')

    def test_another_function_call(self):
        self.assertEqual(call_function('goodbye'), 'Goodbye, world!')

# Running the tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestStringToFunction)
runner = unittest.TextTestRunner()
result = runner.run(suite)

print( result )


