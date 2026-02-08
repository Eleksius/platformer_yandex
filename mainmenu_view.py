import arcade
from game_view import GameView

class MainMenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        """Вызывается, когда представление показывается"""
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def on_draw(self):
        """Отрисовка главного меню"""
        self.clear()

        # Заголовок игры
        arcade.draw_text(
            "Platformer",
            self.window.width / 2,
            self.window.height / 2 + 100,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            anchor_y="center"
        )

        # Заголовок игры
        with open("best_score.txt", 'r') as file:
            best_score = file.read()
            arcade.draw_text(
                f"Best_score: {best_score}",
                100,
                620,
                arcade.color.WHITE,
                font_size=20,
                anchor_x="center",
                anchor_y="center"
            )

        # Кнопка "Играть"
        arcade.draw_rectangle_outline(
            self.window.width / 2,
            self.window.height / 2,
            200,
            50,
            arcade.color.WHITE
        )
        arcade.draw_text(
            "Играть",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

        # Кнопка "Выйти"
        arcade.draw_rectangle_outline(
            self.window.width / 2,
            self.window.height / 2 - 80,
            200,
            50,
            arcade.color.WHITE
        )
        arcade.draw_text(
            "Выйти",
            self.window.width / 2,
            self.window.height / 2 - 80,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия мыши"""
        # Проверяем, была ли нажата кнопка "Играть"
        if (self.window.width / 2 - 100 < x < self.window.width / 2 + 100 and
                self.window.height / 2 - 25 < y < self.window.height / 2 + 25):
            # Создаем и запускаем игру
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        # Проверяем, была ли нажата кнопка "Выйти"
        elif (self.window.width / 2 - 100 < x < self.window.width / 2 + 100 and
              self.window.height / 2 - 80 - 25 < y < self.window.height / 2 - 80 + 25):
            # Выходим из игры
            arcade.close_window()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)