from time import sleep
from MenuItem import MenuItem
import sys
from CommandExecutor import CommandExecutor  # Ensure this class is correctly imported


class Menu:
    def __init__(self, items=None):
        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)

    def display_and_select(self, menu_manager):
        while True:
            # Print the menu options as plain text
            print( "\n\n--------------------------------------------------------------------" )
            print("\Please select an option:")
            print( "--------------------------------------------------------------------" )
            for index, item in enumerate(self.items, start=1):
                print(f"{index}. {item.title}")
            print(f"{len(self.items) + 2}. Add a menu item")
            print( "--------------------------------------------------------------------" )
            print(f"x. Exit this menu")
            print( "--------------------------------------------------------------------\n" )

            choice = input("Enter your choice number or 'x' to exit: ").strip()

            if choice.lower() == 'x':
                break

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.items):
                    menu_item = self.items[choice_num - 1]
                    sleep(0.5)  # Slight delay if needed

                    # Execute the selected menu item’s action
                    CommandExecutor.execute_command(menu_item)

                    # Pause after the command finishes so the user can see the output
                    input("Press Enter to return to the menu...")

                elif choice_num == len(self.items) + 2:
                    # Add a new menu item
                    menu_manager.add_menu_item()
                    # Then loop again with the updated list

                else:
                    print("Invalid selection. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a valid option number or 'x' to exit.")

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
