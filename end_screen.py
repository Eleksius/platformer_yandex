import arcade

class EndScreen(arcade.View):
    def __init__(self, points):
        super().__init__()
        self.points = points

    def on_show_view(self):
        """Вызывается, когда представление показывается"""
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def on_draw(self):
        """Отрисовка главного меню"""
        self.clear()

        # Заголовок игры
        arcade.draw_text(
            "Игра окончена",
            self.window.width / 2,
            self.window.height / 2 + 100,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            f"Ваш счет: {self.points}",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            f"нажмите ENTER для возврата в меню",
            self.window.width / 2,
            self.window.height / 2 - 300,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from mainmenu_view import MainMenuView
            self.window.show_view(MainMenuView())