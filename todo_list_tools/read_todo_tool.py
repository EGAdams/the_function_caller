import json

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
