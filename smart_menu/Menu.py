# import MenuItem
from MenuItem import MenuItem
from dialog import Dialog
import sys

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

if __name__ == "__main__":
    main()