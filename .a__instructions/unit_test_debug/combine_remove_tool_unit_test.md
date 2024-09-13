I am trying to run the unit tests for all of the files below that begin with `test_`.
# `tree` output:
```bash
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$ tree
.
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-312.pyc
│   ├── test_edit_todo_tool.cpython-312.pyc
│   └── test_remove_todo_tool.cpython-312.pyc
├── add_todo_tool
│   ├── add_todo_tool.py
│   └── test_add_todo_tool.py
├── all_classes.md
├── edit_todo_tool
│   ├── __pycache__
│   │   └── edit_todo_tool.cpython-312.pyc
│   ├── edit_todo_tool.py
│   ├── fix_unit_tests.py
│   ├── test_edit_todo_tool.py
│   └── unit_test_prompt.md
├── find_python_classes.py
├── fix_unit_tests.py
├── prompts
│   ├── break_edit_tool_into_smaller_objects.md
│   ├── complete_todo_instructions.md
│   ├── corrected_prompt_template.md
│   ├── fix_unit_tests.md
│   ├── new_prompt.md
│   └── unit_test_prompt.md
├── pull_prompt_break_object.py
├── pull_prompt_from_file.py
├── read_todo_tool.py
├── remove_todo_tool
│   ├── __pycache__
│   │   └── remove_todo_tool.cpython-312.pyc
│   ├── remove_todo_tool.py
│   └── test_remove_todo_tool.py
├── run_all_tests.py
├── storage_handler
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── storage_handler.cpython-312.pyc
│   │   └── test_storage_handler.cpython-312.pyc
│   ├── storage_handler.py
│   └── test_storage_handler.py
├── task
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── task.cpython-312.pyc
│   │   └── test_task.cpython-312.pyc
│   ├── fix_unit_tests.py
│   ├── task.py
│   ├── test_task.py
│   └── unit_test_prompt.md
├── task_editor
│   ├── __pycache__
│   │   └── task_editor.cpython-312.pyc
│   └── task_editor.py
├── task_factory
│   ├── __pycache__
│   │   └── task_factory.cpython-312.pyc
│   └── task_factory.py
├── task_finder
│   ├── __pycache__
│   │   ├── task_finder.cpython-312.pyc
│   │   └── test_task_finder.cpython-312.pyc
│   ├── class.md
│   ├── fix_unit_tests.py
│   ├── run_all_tests.py
│   ├── sequence.md
│   ├── simplify_moduraly.md
│   ├── task_finder.py
│   ├── task_iterator
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── task_iterator.cpython-312.pyc
│   │   │   └── test_task_iterator.cpython-312.pyc
│   │   ├── fix_unit_tests.py
│   │   ├── task_iterator.py
│   │   ├── test_task_iterator.py
│   │   └── unit_test_prompt.md
│   ├── task_list
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── task_list.cpython-312.pyc
│   │   │   └── test_task_list.cpython-312.pyc
│   │   ├── task_list.py
│   │   └── test_task_list.py
│   ├── test_task_finder.py
│   └── unit_test_prompt.md
└── todo_list_tool.py

22 directories, 70 files
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$
```
Here is the Python code that I am running:
# Source code for running the tests:
```python
import unittest
import os

def discover_and_run_tests():
    # Set the base directory for the tests
    base_dir = '/home/adamsl/the_function_caller/todo_list_tools/'  # os.path.dirname(os.path.abspath(__file__))

    # Discover all test files that start with 'test_' in the directory and subdirectories
    loader = unittest.TestLoader()
    suite = loader.discover(base_dir, pattern='test_*.py')

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == '__main__':
    discover_and_run_tests()
```

# Output:
```bash
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$ python3 run_all_tests.py
test_load_file_not_found (storage_handler.test_storage_handler.TestStorageHandler.test_load_file_not_found)
Test loading when the file is not found (FileNotFoundError). ... ok
test_load_json_decode_error (storage_handler.test_storage_handler.TestStorageHandler.test_load_json_decode_error)
Test loading when the file contains invalid JSON. ... ok
test_load_valid_file (storage_handler.test_storage_handler.TestStorageHandler.test_load_valid_file)
Test loading from a valid file with valid JSON. ... ok
test_save_todo_list (storage_handler.test_storage_handler.TestStorageHandler.test_save_todo_list)
Test saving a todo list to the file. ... ok
test_task_initialization (task.test_task.TestTask.test_task_initialization)
Test that a Task object is initialized correctly. ... ok
test_task_no_subtasks (task.test_task.TestTask.test_task_no_subtasks)
Test a Task object with no subtasks. ... ok
test_task_with_subtasks (task.test_task.TestTask.test_task_with_subtasks)
Test a Task object with subtasks. ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.023s

OK

All tests passed!
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$
```

There are alot more tests than what are shown in this output.  It doesn't look like the python file is searching recursively for the tests.
