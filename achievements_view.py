import arcade
from constants import get_achievements


class AchievementsView(arcade.View):
    """Представление для отображения списка достижений"""

    def __init__(self):
        super().__init__()
        self.achievements = get_achievements()

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        """Отрисовка экрана достижений"""
        self.clear()

        # Заголовок
        arcade.draw_text(
            "Достижения",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center",
            anchor_y="center"
        )

        # Отображение списка достижений
        y_position = self.window.height - 120
        if self.achievements:
            for name, description in self.achievements.items():
                # Название достижения
                arcade.draw_text(
                    name,
                    50,
                    y_position,
                    arcade.color.YELLOW,
                    font_size=20,
                    anchor_x="left"
                )
                
                # Описание достижения
                arcade.draw_text(
                    f"  - {description}",
                    50,
                    y_position - 25,
                    arcade.color.LIGHT_GRAY,
                    font_size=16,
                    anchor_x="left"
                )
                
                y_position -= 60  # Пространство между достижениями
        else:
            arcade.draw_text(
                "Нет полученных достижений",
                self.window.width / 2,
                self.window.height / 2,
                arcade.color.WHITE,
                font_size=25,
                anchor_x="center",
                anchor_y="center"
            )

        # Кнопка "Назад"
        arcade.draw_rectangle_outline(
            self.window.width / 2,
            50,
            200,
            50,
            arcade.color.WHITE
        )
        arcade.draw_text(
            "Назад",
            self.window.width / 2,
            50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия мыши."""
        # Проверяем, была ли нажата кнопка "Назад"
        if (self.window.width / 2 - 100 < x < self.window.width / 2 + 100 and
                50 - 25 < y < 50 + 25):
            from mainmenu_view import MainMenuView
            self.window.show_view(MainMenuView())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from mainmenu_view import MainMenuView
            self.window.show_view(MainMenuView())