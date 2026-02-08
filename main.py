import arcade
from constants import *
from mainmenu_view import MainMenuView


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
