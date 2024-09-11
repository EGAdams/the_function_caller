import unittest
import os

def discover_and_run_tests():
    # Set the base directory for the tests
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Discover all test files that start with 'test_' in the directory and subdirectories
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=base_dir, pattern='test_*.py', top_level_dir=None)

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == '__main__':
    discover_and_run_tests()

