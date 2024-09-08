Please analyze  all of the classes below and use as many of them as possible to create a new EditTodoTool class that is more modular.
# Python Source Code:
```python
class TodoListTool:
    """
    Provides a tool for managing a todo list.
    
    The `TodoListTool` class exposes methods to add and remove todo items.
    Each todo item is a JSON object with a timestamp and a task.
    """
    
    def __init__(self):
        self.todo_list = []

    def schema():
        return {
            "name": "todo_list",
            "description": "Manage a todo list with add and remove operations",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["add", "remove"],
                        "description": "The action to perform on the todo list."
                    },
                    "task": {
                        "type": "string",
                        "description": "The task to add or remove from the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["action", "task"]
            }
        }

    def add_todo(self, task):
        """Adds a new todo item to the list.
        
        Args:
            task (str): The task to add to the todo list.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        timestamp = datetime.now().isoformat()
        todo_item = {"timestamp": timestamp, "task": task}
        self.todo_list.append(todo_item)
        return f"Todo item added: {json.dumps(todo_item)}"

    def remove_todo(self, task):
        """Removes a todo item from the list.
        
        Args:
            task (str): The task to remove from the todo list.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        for item in self.todo_list:
            if item["task"] == task:
                self.todo_list.remove(item)
                return f"Todo item removed: {json.dumps(item)}"
        return f"Todo item not found: {task}"

    def manage_todo(self, action, task):
        """Manages the todo list based on the given action.
        
        Args:
            action (str): The action to perform (add or remove).
            task (str): The task to add or remove.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        if action == "add":
            return self.add_todo(task)
        elif action == "remove":
            return self.remove_todo(task)
        else:
            return "Invalid action. Use 'add' or 'remove'."


class AddTodoTool:
    """
    Provides a tool for adding a new todo item to a list and saving it to a file.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todo_list = self.load_todo_list()

    def schema():
        return {
            "name": "add_todo",
            "description": "Add a new todo item to the list and save it to a file",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to add to the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["task"]
            }
        }

    def load_todo_list(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_todo_list(self):
        with open(self.filename, 'w') as file:
            json.dump(self.todo_list, file, indent=2)

    def add_todo(self, task):
        timestamp = datetime.now().isoformat()
        new_id = str(len(self.todo_list) + 1)
        todo_item = {"id": new_id, "timestamp": timestamp, "task": task}
        self.todo_list.append(todo_item)
        self.save_todo_list()
        return f"Todo item added and saved: {json.dumps(todo_item)}"


class ReadTodoTool:
    """
    Provides a tool for reading the todo list from a file.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename

    def schema():
        return {
            "name": "read_todo_list",
            "description": "Read the current todo list from a file",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
                "required": []
            }
        }

    def load_todo_list(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def read_todo_list(self):
        """Reads the current todo list from the file."""
        todo_list = self.load_todo_list()
        if not todo_list:
            return "The todo list is empty."
        else:
            def format_task(task, indent=""):
                result = f"{indent}{task['id']}. {task['task']}\n"
                if "subtasks" in task:
                    for subtask in task["subtasks"]:
                        result += format_task(subtask, indent + "  ")
                return result

            formatted_list = "".join(format_task(task) for task in todo_list)
            return formatted_list


class EditTodoTool:
    """
    Provides a tool for editing todo items, including adding subtasks.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todo_list = self.load_todo_list()

    @staticmethod
    def schema():
        return {
            "name": "edit_todo",
            "description": "Edit a todo item or add a subtask",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to edit (e.g., '19' or '19.b')"
                    },
                    "new_task": {
                        "type": "string",
                        "description": "The new task description or subtask to add"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["edit", "add_subtask"],
                        "description": "Whether to edit the existing task or add a subtask"
                    }
                },
                "additionalProperties": False,
                "required": ["task_id", "new_task", "action"]
            }
        }

    def load_todo_list(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_todo_list(self):
        with open(self.filename, 'w') as file:
            json.dump(self.todo_list, file, indent=2)

    def edit_todo(self, task_id, new_task, action):
        """Edits a todo item or adds a subtask."""
        task = self.find_task(task_id)
        if task is None:
            return f"Task with ID {task_id} not found."

        if action == "edit":
            task["task"] = new_task
            task["timestamp"] = datetime.now().isoformat()
        elif action == "add_subtask":
            if "subtasks" not in task:
                task["subtasks"] = []
            new_subtask_id = f"{task_id}.{chr(97 + len(task['subtasks']))}"
            task["subtasks"].append({
                "id": new_subtask_id,
                "task": new_task,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return f"Invalid action: {action}"
        
        self.save_todo_list()
        return f"Task updated: {json.dumps(task)}"

    def find_task(self, task_id):
        """Finds a task by its ID in the todo list."""
        parts = task_id.split('.')
        current_list = self.todo_list
        for part in parts:
            task_found = False
            for item in current_list:
                if item.get("id") == part or item.get("id") == task_id:
                    if part == parts[-1]:
                        return item
                    current_list = item.get("subtasks", [])
                    task_found = True
                    break
            if not task_found:
                return None
        return None


class StorageHandler:
    """Handles the loading and saving of the todo list to/from a file."""

    def __init__(self, filename="todo_list.json"):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, todo_list):
        with open(self.filename, 'w') as file:
            json.dump(todo_list, file, indent=2)


class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""
    
    @staticmethod
    def find_task(todo_list, task_id):
        task_list = TaskFactory.create_task_list(todo_list)
        task_iterator = TaskIterator(task_list, task_id)
        return task_iterator.iterate()


class TaskList:
    """Manages a list of tasks and subtasks."""
    
    def __init__(self, tasks):
        self.tasks = [Task(task) for task in tasks]
    
    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


class TaskIterator:
    """Iterates through the tasks based on task ID parts."""
    
    def __init__(self, task_list, task_id):
        self.task_list = task_list
        self.task_id = task_id
    
    def iterate(self):
        current_tasks = self.task_list.tasks
        for task in current_tasks:
            result = task.find_task_by_id(self.task_id)
            if result:
                return result
        return None



class TaskEditor:
    """Handles editing existing tasks."""

    @staticmethod
    def edit_task(task, new_task):
        task["task"] = new_task
        task["timestamp"] = datetime.now().isoformat()


class Task:
    """Represents a task with optional subtasks."""
    
    def __init__(self, task_dict):
        # Ensure task_dict is a dictionary
        if isinstance(task_dict, dict):
            self.id = task_dict.get('id')
            self.task = task_dict.get('task')
            self.subtasks = [Task(subtask) for subtask in task_dict.get('subtasks', [])]
        else:
            raise ValueError("task_dict must be a dictionary")

    def find_task_by_id(self, task_id):
        if self.id == task_id:
            return self
        for subtask in self.subtasks:
            result = subtask.find_task_by_id(task_id)
            if result:
                return result
        return None

    def has_subtasks(self):
        """Return True if the task has subtasks."""
        return len(self.subtasks) > 0
    
    def get_id(self):
        """Return the task's ID."""
        return self.id

    def get_task(self):
        """Return the task description."""
        return self.task


class TaskFactory:
    """Factory for creating Task objects."""
    
    @staticmethod
    def create_task_list(todo_list):
        return TaskList(todo_list)
    

class RemoveTodoTool:
    """
    Provides a tool for removing a todo item from a list and updating the file.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todo_list = self.load_todo_list()

    def schema():
        return {
            "name": "remove_todo",
            "description": "Remove a todo item from the list and update the file",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to remove from the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["task"]
            }
        }

    def load_todo_list(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_todo_list(self):
        with open(self.filename, 'w') as file:
            json.dump(self.todo_list, file, indent=2)

    def remove_todo(self, task_id):
        """Removes a todo item from the list and updates the file."""
        def remove_recursive(task_list, target_id):
            for index, item in enumerate(task_list):
                if item["id"] == target_id:
                    removed_item = task_list.pop(index)
                    return removed_item
                if "subtasks" in item:
                    result = remove_recursive(item["subtasks"], target_id)
                    if result:
                        return result
            return None

        removed_item = remove_recursive(self.todo_list, task_id)
        if removed_item:
            self.save_todo_list()
            return f"Todo item removed and file updated: {json.dumps(removed_item)}"
        return f"Todo item not found: {task_id}"
```


