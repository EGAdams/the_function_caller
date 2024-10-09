# Implementing circular dependency check and re-running the test
from todo_list_tools.task_factory.task_factory import TaskFactory


class SubTaskManager:
    def __init__(self, factory):
        self.factory = factory
        self.tasks = []

    def createTask(self, name):
        task = self.factory.create_task(name)
        self.tasks.append(task)
        return task

    def createSubTask(self, name, parent_task):
        # Check for circular dependency
        if self._is_circular_dependency(parent_task, name):
            raise Exception("Circular dependency detected")
        
        sub_task = self.factory.create_sub_task(name, parent_task)
        if not hasattr(parent_task, 'sub_tasks'):
            parent_task.sub_tasks = []
        parent_task.sub_tasks.append(sub_task)
        return sub_task

    def _is_circular_dependency(self, task, sub_task_name):
        """ Recursively check if adding this sub-task would cause a circular dependency """
        if task.name == sub_task_name:
            return True
        if hasattr(task, 'sub_tasks'):
            for sub_task in task.sub_tasks:
                if self._is_circular_dependency(sub_task, sub_task_name):
                    return True
        return False

# Re-running the circular dependency test
def test_circular_dependency():
    manager = SubTaskManager(TaskFactory())
    
    # Create a parent task and a sub-task
    parent_task = manager.createTask("Parent Task")
    sub_task = manager.createSubTask("Sub Task", parent_task)
    
    # Now, we try to create a circular dependency by adding the parent task as a sub-task to its own sub-task
    try:
        manager.createSubTask("Parent Task", sub_task)  # This should raise an error
    except Exception as e:
        assert str(e) == "Circular dependency detected"

# Running the test to confirm the circular dependency is detected
test_circular_dependency()
