import unittest
from unittest.mock import mock_open, patch
import json
from storage_handler import StorageHandler

class TestStorageHandler(unittest.TestCase):
    
    def setUp(self):
        """Setup StorageHandler with a test file."""
        self.storage_handler = StorageHandler(filename="test_todo_list.json")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "1", "task": "Test Task"}]')
    def test_load_valid_file(self, mock_file):
        """Test loading from a valid file with valid JSON."""
        todo_list = self.storage_handler.load()
        mock_file.assert_called_once_with("test_todo_list.json", "r")
        self.assertEqual(len(todo_list), 1)
        self.assertEqual(todo_list[0]["id"], "1")
        self.assertEqual(todo_list[0]["task"], "Test Task")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_file_not_found(self, mock_file):
        """Test loading when the file is not found (FileNotFoundError)."""
        mock_file.side_effect = FileNotFoundError
        todo_list = self.storage_handler.load()
        mock_file.assert_called_once_with("test_todo_list.json", "r")
        self.assertEqual(todo_list, [])

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_json_decode_error(self, mock_file):
        """Test loading when the file contains invalid JSON."""
        mock_file.side_effect = json.JSONDecodeError("Expecting value", "invalid json", 0)
        todo_list = self.storage_handler.load()
        mock_file.assert_called_once_with("test_todo_list.json", "r")
        self.assertEqual(todo_list, [])

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_todo_list(self, mock_json_dump, mock_file):
        """Test saving a todo list to the file."""
        todo_list = [{"id": "1", "task": "Test Task"}]
        self.storage_handler.save(todo_list)
        mock_file.assert_called_once_with("test_todo_list.json", "w")
        mock_json_dump.assert_called_once_with(todo_list, mock_file(), indent=2)


if __name__ == "__main__":
    unittest.main()
