#pip install pythondialog
import os
import sys
from MenuManager import MenuManager
# from Menu import Menu
from Menu import Menu
if __name__ == "__main__":
    # put the home directory (~) into a variable
    home_directory = os.path.expanduser("~")
    # get the command line argument for the configuration file path
    config_path_directory = home_directory + "linuxBash/python_menus/smart_menu/config.json"
    config_path = sys.argv[ 1 ] or config_path_directory

    menu = Menu()
    menu_manager = MenuManager(menu, config_path )
    menu_manager.load_menus()
    menu.display_and_select(menu_manager)
