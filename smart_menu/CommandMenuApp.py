from CommandExecutor import CommandExecutor
from Menu import Menu
from MenuManager import MenuManager
# import npyscreen
import subprocess
import sys

# CommandMenuApp class
class CommandMenuApp(npyscreen.NPSAppManaged):
    def __init__(self, menu, menu_manager):
        super().__init__()
        self.menu = menu
        self.menu_manager = menu_manager

    def onStart(self):
        # Add the main form to the application
        self.addForm(
            "MAIN",
            CommandMenuForm,
            name="Command Menu",
            menu=self.menu,
            menu_manager=self.menu_manager,
        )

# CommandMenuForm class
class CommandMenuForm(npyscreen.FormBaseNew):
    def create(self):
        # Access menu and menu manager from the parent application
        self.menu = self.parentApp.menu
        self.menu_manager = self.parentApp.menu_manager

        # Create the menu widget using MultiLineAction
        self.menu_box = self.add(
            MenuBoxWidget, name="Menu", relx=2, rely=2, max_width=30, max_height=None
        )

        # Populate the menu items
        self.update_menu_items()

        # Create the output box to display command outputs
        self.output_box = self.add(
            npyscreen.BoxTitle, name="Output", relx=35, rely=2, max_height=None
        )

    def update_menu_items(self):
        # Build the list of menu item titles
        menu_titles = [item.title for item in self.menu.items]
        menu_titles.append("Exit this menu")
        menu_titles.append("Add a menu item")
        # Update the menu box with the new values
        self.menu_box.values = menu_titles
        self.menu_box.display()

    def afterEditing(self):
        # Exit the application after editing is complete
        self.parentApp.setNextForm(None)

# MenuBoxWidget class
class MenuBoxWidget(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, keypress):
        # This method is called when a menu item is selected
        form = self.parent
        index = self.values.index(act_on_this)
        if index is not None:
            if 0 <= index < len(form.menu.items):
                # Execute the selected menu item's action using CommandExecutor
                menu_item = form.menu.items[index]
                command_output = CommandExecutor.execute_command(menu_item)
                # Display the output in the output box
                form.output_box.values = command_output.split('\n')
                form.output_box.display()
            elif index == len(form.menu.items):
                # Exit this menu
                form.parentApp.setNextForm(None)
                form.editing = False
            elif index == len(form.menu.items) + 1:
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

# Main execution block
if __name__ == '__main__':
    # Create an instance of Menu

    # use the 1st argument for the configuration file
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "config.json"  # Default path if no argument provided

    menu = Menu()
    
    # Create a MenuManager
    menu_manager = MenuManager(menu, config_path)
    
    # Load menus from config
    menu_manager.load_menus()
    
    # Start the application
    app = CommandMenuApp(menu, menu_manager)
    app.run()