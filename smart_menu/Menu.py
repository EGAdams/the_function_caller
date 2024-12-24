from MenuItem import MenuItem
from dialog import Dialog
import sys
from CommandExecutor import CommandExecutor  # Ensure this class is correctly imported


class Menu:
    def __init__(self, items=None):
        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)

    def display_and_select(self, menu_manager):
        # Initialize Dialog object
        d = Dialog(dialog="dialog")  # Specify the path to the 'dialog' executable if needed
        from time import sleep  # Import sleep function

        while True:
            # Build the menu items list
            menu_items = []
            for index, item in enumerate(self.items, start=1):
                menu_items.append((str(index), item.title))
            # Add exit and add item options
            menu_items.append((str(len(self.items) + 1), "Exit this menu"))
            menu_items.append((str(len(self.items) + 2), "Add a menu item"))

            # Display the menu
            code, tag = d.menu(
                "Please select an option:",
                choices=menu_items,
                title="Menu",
                cancel_label="Exit",
                ok_label="Select"
            )

            if code == d.CANCEL or code == d.ESC:
                # User chose to exit the menu
                break
            elif code == d.OK:
                try:
                    choice = int(tag)
                    if 1 <= choice <= len(self.items):
                        # Execute the selected menu item's action using CommandExecutor
                        menu_item = self.items[choice - 1]
                        output = "executing command: " + menu_item.title
                        sleep(0.5)
                        output = CommandExecutor.execute_command(menu_item)
                        print(output)
                        d.msgbox(output, title="Command Output", width=80)
                    elif choice == len(self.items) + 1:
                        # Exit this menu
                        break
                    elif choice == len(self.items) + 2:
                        # Add a new menu item
                        menu_manager.add_menu_item()
                        # Update the menu items after adding a new one
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
        print("Adding a new menu item...")
        title = input("Enter title for new item: ")
        action = input("Enter command to execute: ")
        working_directory = input("Enter the working directory (optional): ")
        open_in_subprocess = input("Open in a subprocess? (yes/no): ").lower() == 'yes'
        use_expect_library = input("Use the expect library? (yes/no): ").lower() == 'yes'
        new_item = MenuItem(
            title,
            action,
            working_directory,
            open_in_subprocess,
            use_expect_library
        )
        self.add_item(new_item)
        print("New menu item added successfully.")

    def to_dict_list(self):
        """Serializes the menu's items into a list of dictionaries."""
        return [item.to_dict() for item in self.items]

def main():
    # Import MenuManager here to avoid circular import
    from MenuManager import MenuManager

    # Create an instance of Menu
    menu = Menu()
    config_path = "menu_config.json"  # Path to the configuration file

    # Create a MenuManager
    menu_manager = MenuManager(menu, config_path)

    # Load menus from config
    menu_manager.load_menus()

    # Display the menu
    menu.display_and_select(menu_manager)

if __name__ == "__main__":
    main()
