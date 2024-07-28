import unittest
from function_map import FunctionMap

class TestFunctionMap( unittest.TestCase ):
    def setUp( self ):
        self.function_map = FunctionMap()

    def test_empty_function_map( self ):
        self.assertEqual( self.function_map.get_length(), 0)

    def test_add_function(self):
        def test_func():
            return "Test"
        self.function_map.add_function( "test", test_func )
        self.assertEqual( self.function_map.get_length(), 1)

    def test_get_existing_function( self ):
        def test_func():
            return "Test"
        self.function_map.add_function( "test", test_func )
        retrieved_func = self.function_map.get_function("test")
        self.assertEqual( retrieved_func(), "Test")

if __name__ == '__main__':
    unittest.main()
