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
