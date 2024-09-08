class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""

    @staticmethod
    def find_task(todo_list, task_id):
        parts = task_id.split('.')
        current_list = todo_list
        
        for part in parts:
            task_found = False
            for item in current_list:
                # Only consider the relevant part at each level
                if item.get("id") == part:
                    if part == parts[-1]:  # If it's the last part, return the item
                        return item
                    current_list = item.get("subtasks", [])
                    task_found = True
                    break
            if not task_found:
                return None
        return None
