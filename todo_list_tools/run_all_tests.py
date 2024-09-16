import unittest
import os

def discover_and_run_tests():
    # Set the base directory for the tests
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Initialize a test suite
    suite = unittest.TestSuite()

    # Walk through the directory structure to find all test_*.py files
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                # Get the relative path of the file
                rel_dir = os.path.relpath(root, base_dir)
                # Form the module name by replacing path separators with dots and stripping the '.py' extension
                module_name = os.path.join(rel_dir, file).replace(os.sep, '.').rstrip('.py')
                # Load the module and add it to the test suite
                try:
                    loaded_tests = unittest.defaultTestLoader.loadTestsFromName(module_name)
                    suite.addTests(loaded_tests)
                except ModuleNotFoundError as e:
                    print(f"Could not load tests from {module_name}: {e}")
                except Exception as e:
                    print(f"Error loading tests from {module_name}: {e}")

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == '__main__':
    discover_and_run_tests()
