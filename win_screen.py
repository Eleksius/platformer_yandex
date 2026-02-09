import arcade
from constants import get_achievements, add_achievement

class WinScreen(arcade.View):
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.ach = arcade.load_sound(":resources:sounds/upgrade5.wav")

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.GREEN)

    def on_draw(self):
        """Отрисовка главного меню"""
        self.clear()

        if self.points >= 100 and "100 points" not in get_achievements():
            add_achievement("100 points", "collect more than 100 points in one race")
            arcade.play_sound(self.ach)

        if self.points >= 116 and "points master" not in get_achievements():
            add_achievement("points master", "collect all points in the game")
            arcade.play_sound(self.ach)

        # Заголовок игры
        arcade.draw_text(
            "Игра пройдена",
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

        with open("best_score.txt", "r+") as file:
            text = file.read()
            if text:
                if self.points > int(text):
                    file.seek(0)
                    file.write(str(self.points))
            else:
                file.write(str(self.points))

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
