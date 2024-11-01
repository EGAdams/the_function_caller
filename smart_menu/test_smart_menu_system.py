import sys
from MenuManager import MenuManager
# from Menu import Menu
from Menu import Menu
if __name__ == "__main__":
    # get the command line argument for the configuration file path
    config_path = sys.argv[ 1 ] or "/home/eg1972/linuxBash/python_menus/smart_menu/config.json"

    menu = Menu()
    menu_manager = MenuManager(menu, config_path )
    menu_manager.load_menus()
    menu.display_and_select(menu_manager)
