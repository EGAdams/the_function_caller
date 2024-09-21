# Import main classes and functions from the package modules using relative imports
# task_iterator/__init__.py
from .task_iterator import TaskIterator
from .task_list     import TaskList

# You can define __all__ to specify what gets imported when using "from todo_list_tools import *"
__all__ = [ 'TaskList', 'TaskIterator' ]

# Package metadata
__version__ = '0.1.0'
__author__ = 'EG Adams'
__email__ = 'eg@americansjewelry.com'

# You can also include a brief description of the package
__doc__ = """
A package for managing todo lists and items.

This package provides classes and functions to create, manage, and manipulate todo lists and individual todo items.
"""
