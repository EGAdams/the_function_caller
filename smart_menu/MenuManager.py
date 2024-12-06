import json
from ConfigReader import ConfigReader
from Menu import Menu
from MenuItem import MenuItem
from CommandExecutor import CommandExecutor
from SmartMenuItem import SmartMenuItem
# from DialogMenu import DialogMenu

# and for the DialogMenu...
import shutil
import os

class MenuManager:
    def __init__(self, menu: Menu, config_path: str):
        self.menu = menu
        self.config_path = config_path

    def load_menus(self):
        """Loads the menu items from the configuration file."""
        config_data = ConfigReader.read_config(self.config_path)
        for item_config in config_data:
            menu_item = MenuItem(
                title=item_config['title'],
                action=item_config['action'],
                working_directory=item_config.get('working_directory', ''),
                open_in_subprocess=item_config.get('open_in_subprocess', False),
                use_expect_library=item_config.get('use_expect_library', False),
            )
            self.menu.add_item(menu_item)

    def add_menu_item(self):
        """Adds a new menu item (simplified for this example)."""
        new_item = MenuItem("New Item", "echo 'New item executed'")
        self.menu.add_item(new_item)
        self.save_menus_to_config()

    def save_menus_to_config(self):
        """Serializes and saves the menu structure to the configuration file."""
        config_data = self.menu.to_dict_list()
        with open(self.config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        print("Menu configuration saved.")
