# Import main classes and functions from the package modules using relative imports
from .task.task import Task
from .task_editor.task_editor import TaskEditor
from .task_factory.task_factory import TaskFactory
from .task_finder.task_finder import TaskFinder
from .storage_handler.storage_handler import StorageHandler

# You can define __all__ to specify what gets imported when using "from todo_list_tools import *"
__all__ = ['Task', 'TaskEditor', 'TaskFactory', 'TaskFinder', 'StorageHandler']

# Package metadata
__version__ = '0.1.0'
__author__ = 'EG Adams'
__email__ = 'eg@americansjewelry.com'

# You can also include a brief description of the package
__doc__ = """
A package for managing todo lists and items.

This package provides classes and functions to create, manage, and manipulate todo lists and individual todo items.
"""
