from abc import ABC, abstractmethod

class IFunctionHandler(ABC):
    @abstractmethod
    def execute(self, parameters: dict) -> str:
            raise NotImplementedError("Subclasses should implement this method.")
    """
    Execute the function with the given parameters.

    Args:
        parameters (dict): A dictionary of parameters required for execution.

    Returns:
        str: The result of the function execution.
    """
    pass
