
# Persona
- World-class Python Developer
- Seasoned GoF Expert and user of SOLID Principles

# Goal
Break up the following object into smaller objects.  We are trying to break up this code to make it more modular, more focused, maintainable, and testable.

# Python Source Code for the Object: `TaskFinder`
```py
import json
from datetime import datetime

class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""

    @staticmethod
    def find_task(todo_list, task_id):
        parts = task_id.split('.')
        current_list = todo_list
        
        for part in parts:
            for item in current_list:
                if item.get("id") == part:
                    if part == parts[-1]:  # If it's the last part, return the item
                        return item
                    current_list = item.get("subtasks", [])
                    break
            else:
                return None  # Return None if part not found
        return None
```

# Your Task
- Break the original object `TaskFinder` into smaller objects.
- When you break the object up into smaller objects, create each smaller object so that even a very beginner Python developer can understand it.
- Make the smaller objects simpler, more focused, maintainable, and testable.  
- Use your skills at using GoF and SOLID principles to rewrite the file `task_finder.py` to conform to this more modular approach.
- If you see a place where we could use a design pattern, use it because we are also using this code base to teach beginner Python developers how to use design patterns.