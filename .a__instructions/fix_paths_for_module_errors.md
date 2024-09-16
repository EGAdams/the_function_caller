I am running the following Python script from the todo_list_tools directory as you have suggested.

Here is the source file.
```python
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
```

```bash
adamsl@DESKTOP-2OBSQMC:~/the_function_caller$ cd todo_list_tools/
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$ python3 run_all_tests.py 
test_remove_todo_tool (unittest.loader._FailedTest.test_remove_todo_tool) ... ERROR
test_add_todo_tool (unittest.loader._FailedTest.test_add_todo_tool) ... ERROR
test_find_non_existent_subtask (task_finder.test_task_finder.TestTaskFinder.test_find_non_existent_subtask)
Test finding a non-existent subtask. ... ok
test_find_non_existent_task (task_finder.test_task_finder.TestTaskFinder.test_find_non_existent_task)
Test finding a non-existent task. ... ok
test_find_root_task (task_finder.test_task_finder.TestTaskFinder.test_find_root_task)
Test finding a root-level task. ... ok
test_find_subtask (task_finder.test_task_finder.TestTaskFinder.test_find_subtask)
Test finding a subtask. ... ok
test_find_subtask_with_multiple_levels_missing (task_finder.test_task_finder.TestTaskFinder.test_find_subtask_with_multiple_levels_missing)
Test finding a subtask with multiple levels that does not exist. ... ok
test_find_task_with_multiple_levels (task_finder.test_task_finder.TestTaskFinder.test_find_task_with_multiple_levels)
Test finding a task with more than one subtask level. ... ok
test_iterate_finds_task (task_finder.task_iterator.test_task_iterator.TaskIteratorTest.test_iterate_finds_task)
Test that TaskIterator correctly finds a task based on task_id. ... ok
test_iterate_finds_task_with_no_subtasks (task_finder.task_iterator.test_task_iterator.TaskIteratorTest.test_iterate_finds_task_with_no_subtasks)
Test that TaskIterator correctly finds a task with no subtasks. ... ok
test_iterate_finds_top_level_task (task_finder.task_iterator.test_task_iterator.TaskIteratorTest.test_iterate_finds_top_level_task)
Test that TaskIterator finds a top-level task. ... ok
test_iterate_returns_none_for_invalid_task_id (task_finder.task_iterator.test_task_iterator.TaskIteratorTest.test_iterate_returns_none_for_invalid_task_id)
Test that TaskIterator returns None for an invalid task_id. ... ok
test_find_task_by_id_does_not_exist (task_finder.task_list.test_task_list.TestTaskList.test_find_task_by_id_does_not_exist)
Test finding a task by ID when the task does not exist. ... ok
test_find_task_by_id_exists (task_finder.task_list.test_task_list.TestTaskList.test_find_task_by_id_exists)
Test finding a task by ID when the task exists. ... ok
test_find_task_no_subtasks (task_finder.task_list.test_task_list.TestTaskList.test_find_task_no_subtasks)
Test finding a task that has no subtasks. ... ok
test_find_task_with_subtasks (task_finder.task_list.test_task_list.TestTaskList.test_find_task_with_subtasks)
Test finding a task and its subtasks. ... ok
test_add_subtask_to_existing_task (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_add_subtask_to_existing_task) ... ok
test_edit_existing_task (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_edit_existing_task) ... ok
test_invalid_action (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_invalid_action) ... ok
test_save_todo_list_after_add_subtask (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_save_todo_list_after_add_subtask) ... ok
test_save_todo_list_after_edit (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_save_todo_list_after_edit) ... ok
test_schema (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_schema) ... ok
test_task_not_found (edit_todo_tool.test_edit_todo_tool.TestEditTodoTool.test_task_not_found) ... ok
test_task_initialization (task.test_task.TestTask.test_task_initialization)
Test that a Task object is initialized correctly. ... ok
test_task_no_subtasks (task.test_task.TestTask.test_task_no_subtasks)
Test a Task object with no subtasks. ... ok
test_task_with_subtasks (task.test_task.TestTask.test_task_with_subtasks)
Test a Task object with subtasks. ... ok
test_load_file_not_found (storage_handler.test_storage_handler.TestStorageHandler.test_load_file_not_found)
Test loading when the file is not found (FileNotFoundError). ... ok
test_load_json_decode_error (storage_handler.test_storage_handler.TestStorageHandler.test_load_json_decode_error)
Test loading when the file contains invalid JSON. ... ok
test_load_valid_file (storage_handler.test_storage_handler.TestStorageHandler.test_load_valid_file)
Test loading from a valid file with valid JSON. ... ok
test_save_todo_list (storage_handler.test_storage_handler.TestStorageHandler.test_save_todo_list)
Test saving a todo list to the file. ... ok

======================================================================
ERROR: test_remove_todo_tool (unittest.loader._FailedTest.test_remove_todo_tool)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_remove_todo_tool
Traceback (most recent call last):
  File "/usr/lib/python3.12/unittest/loader.py", line 137, in loadTestsFromName
    module = __import__(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/adamsl/the_function_caller/todo_list_tools/remove_todo_tool/test_remove_todo_tool.py", line 6, in <module>
    from todo_list_tools.remove_todo_tool.remove_todo_tool import RemoveTodoTool
ModuleNotFoundError: No module named 'todo_list_tools'


======================================================================
ERROR: test_add_todo_tool (unittest.loader._FailedTest.test_add_todo_tool)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_add_todo_tool
Traceback (most recent call last):
  File "/usr/lib/python3.12/unittest/loader.py", line 137, in loadTestsFromName
    module = __import__(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/adamsl/the_function_caller/todo_list_tools/add_todo_tool/test_add_todo_tool.py", line 7, in <module>
    from add_todo_tool import AddTodoTool
ImportError: cannot import name 'AddTodoTool' from 'add_todo_tool' (unknown location)


----------------------------------------------------------------------
Ran 30 tests in 0.019s

FAILED (errors=2)

Some tests failed.
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$
```

Is this correct?