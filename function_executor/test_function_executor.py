import unittest
from function_executor.FunctionExecutor import FunctionExecutor

class TestFunctionExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = FunctionExecutor()

    def test_empty_executor(self):
        self.assertEqual(len(self.executor.functions), 0)

    def test_add_function(self):
        def test_func():
            return "Test"
        self.executor.add_function("test", test_func)
        self.assertEqual(len(self.executor.functions), 1)
        self.assertIn("test", self.executor.functions)

    def test_execute_function(self):
        def greet(name):
            return f"Hello, {name}!"
        self.executor.add_function("greet", greet)
        result = self.executor.execute("greet", "Alice")
        self.assertEqual(result, "Hello, Alice!")

    def test_execute_nonexistent_function(self):
        with self.assertRaises(KeyError):
            self.executor.execute("nonexistent", "arg")

    def test_remove_function(self):
        def dummy():
            pass
        self.executor.add_function("dummy", dummy)
        self.executor.remove_function("dummy")
        self.assertEqual(len(self.executor.functions), 0)

    def test_list_functions(self):
        def func1():
            pass
        def func2():
            pass
        self.executor.add_function("func1", func1)
        self.executor.add_function("func2", func2)
        function_list = self.executor.list_functions()
        self.assertEqual(set(function_list), {"func1", "func2"})

if __name__ == '__main__':
    unittest.main()
