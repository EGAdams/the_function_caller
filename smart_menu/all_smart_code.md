# Persona
- World-class Object-Oriented Programmer 
- Seasoned user of The Gang of Four Design Patterns
- Expert Python Developer

# The App that we want to modify for flexiibility
We have the Python code for a command menu system that has an excellent user interface that we want to keep.  The problem is that the menu items need to be added manually and we want to be able to dynamically add menu items at runtime.  We also want the menu to be able to read a JSON configuration file to dynamically build the initial menu items.

# Source code for the command menu system that we want to modify for flexiibility
The following is the Python code for the Objects that we want to use to enhance the command menu system to make it more flexiible.

## CommandMenuApp
```python
import npyscreen
import subprocess

class CommandMenuApp(npyscreen.NPSAppManaged):
    def __init__(self, menu_items, menu_manager):
        super().__init__()
        self.menu_items = menu_items
        self.menu_manager = menu_manager

    def onStart(self):
        # Add the main form to the application
        self.addForm("MAIN", CommandMenuForm, name="Command Menu",
                     menu_items=self.menu_items, menu_manager=self.menu_manager)

class CommandMenuForm(npyscreen.FormBaseNew):
    def create(self):
        # Access menu items and manager from the parent application
        self.menu_items = self.parentApp.menu_items
        self.menu_manager = self.parentApp.menu_manager

        # Create the menu widget using MultiLineAction
        self.menu_box = self.add(MenuBoxWidget, name="Menu",
                                 relx=2, rely=2, max_width=30, max_height=None)

        # Populate the menu items
        self.update_menu_items()

        # Create the output box to display command outputs
        self.output_box = self.add(npyscreen.MultiLineEditableBoxed,
                                   name="Output",
                                   relx=35, rely=2,
                                   max_height=None)

    def update_menu_items(self):
        # Build the list of menu item titles
        menu_titles = [item.title for item in self.menu_items]
        menu_titles.append("Exit this menu")
        menu_titles.append("Add a menu item")
        # Update the menu box with the new values
        self.menu_box.values = menu_titles
        self.menu_box.display()

    def afterEditing(self):
        # Exit the application after editing is complete
        self.parentApp.setNextForm(None)

class MenuBoxWidget(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, keypress):
        # This method is called when a menu item is selected
        form = self.parent
        index = self.values.index(act_on_this)
        if index is not None:
            if 0 <= index < len(form.menu_items):
                # Execute the selected menu item's action and capture output
                command_output = form.menu_items[index].execute()
                # Display the output in the output box
                form.output_box.values = command_output.split('\n')
                form.output_box.display()
            elif index == len(form.menu_items):
                # Exit this menu
                form.parentApp.setNextForm(None)
                form.editing = False
            elif index == len(form.menu_items) + 1:
                # Add a new menu item
                form.menu_manager.add_menu_item()
                # Update the menu items
                form.update_menu_items()
            else:
                # Invalid selection
                npyscreen.notify_confirm("Invalid selection. Please try again.", title="Error")
        else:
            # No selection made
            npyscreen.notify_confirm("No selection made. Please try again.", title="Error")

# MenuItem class representing individual menu items
class MenuItem:
    def __init__(self, title, command):
        self.title = title
        self.command = command  # Command to execute

    def execute(self):
        # Execute the command and return the output
        try:
            output = subprocess.check_output(self.command, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return e.output.decode('utf-8')

# MenuManager class to manage the list of menu items
class MenuManager:
    def __init__(self):
        self.items = []

    def add_menu_item(self):
        # Logic to add a new menu item
        # For demonstration, we'll add a dummy item
        new_item = MenuItem("New Item", "echo 'New item executed'")
        self.items.append(new_item)

# Main execution block
if __name__ == '__main__':
    # Create an instance of MenuManager and add initial menu items
    menu_manager = MenuManager()
    menu_manager.items = [
        MenuItem("List Files", "ls -l"),
        MenuItem("Show Date", "date"),
        MenuItem("Print Working Directory", "pwd")
    ]

    # Start the application
    app = CommandMenuApp(menu_manager.items, menu_manager)
    app.run()
```

# Existing Python code to use in our system
## CommandExecutor class
```python
class CommandExecutor:
    @staticmethod
    def execute_command(menu_item):
        """Executes the command associated with a given MenuItem."""
        if not isinstance(menu_item, MenuItem):
            raise ValueError("menu_item must be an instance of MenuItem")

        original_dir = os.getcwd()  # Save the original directory
        try:
            # Change the working directory if specified
            if menu_item.working_directory:
                os.chdir(menu_item.working_directory)
            
            # Execute command in a subprocess or current process
            if menu_item.open_in_subprocess:
                subprocess.run(menu_item.action, shell=True, check=True)
            else:
                # This is a placeholder for executing the command without opening a new subprocess.
                # In reality, this might involve more direct execution methods depending on the command.
                os.system(menu_item.action)
        except Exception as e:
            print(f"Error executing command {menu_item.action}: {e}")
        finally:
            os.chdir(original_dir)
```

## ConfigReader class
```python
class ConfigReader:
    @staticmethod
    def read_config(file_path):
        """
        Reads a configuration file and returns its contents as a data structure.
        
        This method attempts to open and read a JSON configuration file specified by `file_path`. 
        If successful, it returns the contents of the file as a Python data structure (typically a dictionary or a list, 
        depending on the JSON structure). If the file cannot be found, or if the file is not valid JSON, appropriate 
        error messages are printed, and an empty list is returned.
        
        Parameters:
        - file_path (str): The path to the configuration file that is to be read.
        
        Returns:
        - list/dict: The content of the configuration file parsed from JSON. If an error occurs, an empty list is returned.
        
        Exceptions:
        - FileNotFoundError: If the file specified by `file_path` does not exist, a message is printed indicating that 
          the file was not found, and an empty list is returned.
        - json.JSONDecodeError: If the file specified by `file_path` is not valid JSON, a message is printed indicating 
          that there was an error decoding the file, and an empty list is returned.
        """
        try:
            with open(file_path, 'r') as config_file:
                config_data = json.load(config_file)
                return config_data
        except FileNotFoundError:
            print(f"The configuration file {file_path} was not found.")
            return []
        except json.JSONDecodeError:
            print("Error decoding the configuration file. Please ensure it is valid JSON.")
            return []
```

# DialogMenu class
```python
class DialogMenu:
    def __init__(self, items=None):
        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)


    def display_and_select(self, menu_manager):
        d = dialog.Dialog(dialog="dialog")

        # Prepare the menu items along with an "Exit" and "Add menu item" option
        menu_items = [(str(index + 1), item.title) for index, item in enumerate(self.items)]
        menu_items.append(("Exit", "Exit this menu"))
        menu_items.append(("Add", "Add a menu item"))

        while True:
            code, tag = d.menu("Please select an option:", choices=menu_items)

            if code == d.OK:
                if tag == "Exit":
                    break
                elif tag == "Add":
                    menu_manager.add_menu_item()
                else:
                    # Convert tag back to index and execute the selected item
                    index = int(tag) - 1
                    if index < len(self.items):
                        self.items[index].execute()
            else:
                # This handles the case where the user presses 'Cancel' or closes the dialog
                print( "Operation cancelled or closed. Exiting..." )
                break

    def add_new_item(self):
        title = input("Enter title for new item: ")
        command = input("Enter command to execute: ")
        working_directory = input("Enter the working directory (optional): ")
        open_in_subprocess = input("Open in a subprocess? (yes/no): ").lower() == 'yes'
        use_expect_library = input("Use the expect library? (yes/no): ").lower() == 'yes'
        new_item = MenuItem( title, command, working_directory, open_in_subprocess, use_expect_library )
        self.add_item( new_item )
    
    def to_dict_list(self):
        """Serializes the menu's items into a list of dictionaries."""
        return [item.to_dict() for item in self.items]

def main():
    menu = Menu()
    # Example adding initial menu items
    menu.add_item(MenuItem("List current directory", "ls"))
    menu.display_and_select()
```

## Menu class
```python
class Menu:
    def __init__(self, items=None):
        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)


    def display_and_select(self, menu_manager):
        # Initialize Dialog object
        d = Dialog(dialog="dialog")  # You can specify the path to the 'dialog' executable if needed

        while True:
            # Build the menu items list
            menu_items = []
            for index, item in enumerate(self.items, start=1):
                menu_items.append((str(index), item.title))
            # Add exit and add item options
            menu_items.append((str(len(self.items) + 1), "Exit this menu"))
            menu_items.append((str(len(self.items) + 2), "Add a menu item"))

            # Display the menu
            code, tag = d.menu("Please select an option:",
                            choices=menu_items,
                            title="Menu",
                            cancel_label="Exit",
                            ok_label="Select")

            if code == d.CANCEL or code == d.ESC:
                # User chose to exit the menu
                break
            elif code == d.OK:
                try:
                    choice = int(tag)
                    if 1 <= choice <= len(self.items):
                        # Execute the selected menu item's action
                        self.items[choice - 1].execute()
                    elif choice == len(self.items) + 1:
                        # Exit this menu
                        break
                    elif choice == len(self.items) + 2:
                        # Add a new menu item
                        menu_manager.add_menu_item()
                    else:
                        # Invalid selection
                        d.msgbox("Invalid selection. Please try again.", title="Error")
                except ValueError:
                    # Non-integer input captured
                    d.msgbox("Invalid input. Please select a valid option.", title="Error")
            else:
                # Handle any other dialog return codes if necessary
                d.msgbox("An unexpected error occurred.", title="Error")

    
    

    def add_new_item(self):
        title = input("Enter title for new item: ")
        command = input("Enter command to execute: ")
        working_directory = input("Enter the working directory (optional): ")
        open_in_subprocess = input("Open in a subprocess? (yes/no): ").lower() == 'no'
        use_expect_library = input("Use the expect library? (yes/no): ").lower() == 'yes'
        new_item = MenuItem( title, command, working_directory, open_in_subprocess, use_expect_library )
        self.add_item( new_item )
    
    def to_dict_list(self):
        """Serializes the menu's items into a list of dictionaries."""
        return [item.to_dict() for item in self.items]

def main():
    menu = Menu()
    # Example adding initial menu items
    menu.add_item(MenuItem("List current directory", "ls"))
    menu.display_and_select()
```

## MenuItem class
```python
class MenuItem:
    """
    Represents a menu item that can be executed, with options to change the working directory, open in a subprocess, and use the expect library.

    The `MenuItem` class provides a way to encapsulate a command or action that can be executed, with various options to control how the command is run. The class has the following attributes:

    - `title`: The title or label of the menu item.
    - `action`: The command or action to be executed.
    - `working_directory`: The working directory to change to before executing the action.
    - `open_in_subprocess`: A boolean indicating whether to open the command in a new subprocess.
    - `use_expect_library`: A boolean indicating whether to use the expect library to handle the command.

    The `execute()` method is responsible for running the command or action, with the specified options. It changes the working directory if necessary, and then either runs the command in a new subprocess or in the current process, depending on the `open_in_subprocess` option. If an error occurs during execution, it is caught and printed.

    The `to_dict()` method serializes the `MenuItem` instance into a dictionary, which can be useful for storing or transmitting the menu item data.
    """
    def __init__(self, title, action, working_directory, open_in_subprocess, use_expect_library):
        self.title = title
        self.action = action
        self.working_directory = working_directory
        self.open_in_subprocess = open_in_subprocess
        self.use_expect_library = use_expect_library

    def execute(self):
        try:
            final_command = self.action
            # Change directory if specified and necessary
            if self.working_directory:
                os.chdir(self.working_directory)
            
            if self.open_in_subprocess:
                # Open the command in a new subprocess
                process = subprocess.Popen(final_command, shell=True)
                process.communicate()  # Wait for the command to complete if needed
            else:
                # Execute the command in the current process
                subprocess.run(final_command, shell=True, check=True)
            
            print(f"Command executed: {self.action}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        finally:
            # If we changed directories, change back to the original
            if self.working_directory:
                os.chdir(os.path.dirname(__file__))
        
    def to_dict(self):
        """Serializes the MenuItem into a dictionary."""
        return {
            "title": self.title,
            "action": self.action,
            "working_directory": self.working_directory,
            "open_in_subprocess": self.open_in_subprocess,
            "use_expect_library": self.use_expect_library
        }
```

## MenuManager class
```python
class MenuManager:
    def __init__(self, menu: Menu, config_path: str):
        self.menu = menu
        self.config_path = config_path

    def load_menus(self):
        """Loads the menu items from the configuration file."""
        config_data = ConfigReader.read_config(self.config_path)
        for item_config in config_data:
            print( item_config.get('working_directory', '' ))
            menu_item = MenuItem(
                title=item_config['title'],
                action=item_config['action'],
                working_directory=item_config.get('working_directory', ''),
                open_in_subprocess=item_config.get('open_in_subprocess', False),
                use_expect_library=item_config.get('use_expect_library', False)
            )
            self.menu.add_item(menu_item)

    def display_menu(self):
        """Displays the menu and handles user input."""
        while True:
            # self.menu.display_and_select()
            choice = input("Please select an option: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(self.menu.items):
                    self.menu.items[choice - 1].execute()
                elif choice == len(self.menu.items) + 1:
                    break  # Exit the menu
                elif choice == len(self.menu.items) + 2:
                    self.add_menu_item()
            else:
                print("Invalid selection. Please try again.")

    def add_menu_item(self):
        print("Adding a new menu item...")
        title = input("Enter the title for the new menu item: ")
        is_submenu = input("Is this a submenu? (yes/no): ").lower() == 'yes'

        if is_submenu:
            new_menu_item = SmartMenuItem(title, sub_menu=Menu())
            print("Submenu added. Remember to add items to this submenu.")
        else:
            action = input("Enter the command to execute: ")
            working_directory = input("Enter the full path to the directory: ")
            open_in_subprocess = input("Should this command open in a separate window (yes/no)? ").lower() == 'yes'
            use_expect_library = input("Should use the Expect library (yes/no)? ").lower() == 'yes'
            new_menu_item = SmartMenuItem(title, action, working_directory, open_in_subprocess, use_expect_library)

        self.menu.add_item(new_menu_item)
        print("New menu item added successfully.")
        self.save_menus_to_config()

    def save_menus_to_config(self):
        """Serializes and saves the menu structure to the configuration file."""
        config_data = [item.to_dict() for item in self.menu.items]
        with open(self.config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        print("Menu configuration saved.")

    def save_to_config(self):
        """Saves the current menu configuration to a file."""
        with open(self.config_path, 'w') as config_file:
            json.dump(self.menu.to_dict_list(), config_file, indent=4)
        print("Menu configuration saved.")

def main():
    menu = Menu()
    menu_manager = MenuManager(menu, "path_to_config.json")
    menu_manager.load_menus()
    menu.display_and_select(menu_manager)
```

## SmartMenuItem class
```python
class SmartMenuItem( MenuItem ):
    def __init__(self, title, action=None, working_directory='', open_in_subprocess=False, use_expect_library=False, sub_menu=None):
        super().__init__(title, action, working_directory, open_in_subprocess, use_expect_library)
        self.sub_menu = sub_menu  # This can be another Menu object or None

    def execute(self):
        if self.sub_menu:
            self.sub_menu.display_and_select()
        else:
            super().execute()

    def to_dict(self):
        item_dict = super().to_dict()
        # Optionally add serialization for sub_menu if needed
        return item_dict
```

# Your Task
Rewrite the original CommandMenuApp to use the new Objects like Menu and MenuItem to make the system more modular, flexible, and easier to test and maintain.
