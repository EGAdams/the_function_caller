import os
import subprocess
class MenuItem:
    def __init__(
        self, title, action, working_directory='', open_in_subprocess=False, use_expect_library=False
    ):
        self.title = title
        self.action = action
        self.working_directory = working_directory
        self.open_in_subprocess = open_in_subprocess
        self.use_expect_library = use_expect_library

    def to_dict(self):
        """Serializes the MenuItem into a dictionary."""
        return {
            "title": self.title,
            "action": self.action,
            "working_directory": self.working_directory,
            "open_in_subprocess": self.open_in_subprocess,
            "use_expect_library": self.use_expect_library
        }