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


class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our TileMap Object

        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load

        # map_name = ":resources:tiled_maps/map.json"
        map_name = "maps/map1.tmx"

        # Layer specific options are defined based on Layer names in a dictionary

        # Doing this will make the SpriteList for the platforms layer

        # use spatial hashing for detection.

        layer_options = {

            "Platforms": {

                "use_spatial_hash": True,

            },

        }

        # Read in the tiled map

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers

        # from the map as SpriteLists in the scene in the proper order.

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Set up the player with animated sprite
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff

        # Set the background color

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'

        self.physics_engine = arcade.PhysicsEnginePlatformer(

            # self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["floor"]

        )

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Движение и логика игры"""

        self.physics_engine.update()

        # Обновление анимации
        self.player_sprite.update_animation(delta_time)

        # Если коснулся монеты
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # Центрирование камеры
        self.center_camera_to_player()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
