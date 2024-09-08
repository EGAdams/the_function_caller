from datetime import datetime

class TaskEditor:
    """Handles editing existing tasks."""

    @staticmethod
    def edit_task(task, new_task):
        task["task"] = new_task
        task["timestamp"] = datetime.now().isoformat()
