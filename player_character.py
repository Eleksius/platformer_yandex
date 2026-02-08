import arcade
from constants import *

class PlayerCharacter(arcade.Sprite):
    """Персонаж с анимацией"""

    def __init__(self):
        super().__init__()

        self.cur_texture = 0

        # Отслеживание направления
        self.facing_direction = RIGHT_FACING

        # Дефолт
        self.idle_texture_pair = arcade.load_texture_pair(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        )

        # Ходьба
        self.walk_textures = []
        for i in range(1, 8):  # Walk frames 1-7
            texture_pair = arcade.load_texture_pair(
                f":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk{i}.png"
            )
            self.walk_textures.append(texture_pair)

        # Прыжок
        self.jump_texture_pair = arcade.load_texture_pair(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_jump.png"
        )

        # Падение
        self.fall_texture_pair = arcade.load_texture_pair(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_fall.png"
        )

        # Дефолтная текстура
        self.texture = self.idle_texture_pair[0]
        self.scale = CHARACTER_SCALING

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Check if moving horizontally
        is_moving = abs(self.change_x) > 0
        # Check if jumping or falling
        is_jumping_or_falling = self.change_y != 0

        # Handle animations based on state
        if is_jumping_or_falling:
            # Jumping animation
            if self.change_y > 0:
                self.texture = self.jump_texture_pair[self.facing_direction]
            # Falling animation
            elif self.change_y < 0:
                self.texture = self.fall_texture_pair[self.facing_direction]
        elif is_moving:
            # Walking animation
            self.cur_texture += 1
            if self.cur_texture >= len(self.walk_textures):
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
        else:
            # Idle animation
            self.texture = self.idle_texture_pair[self.facing_direction]