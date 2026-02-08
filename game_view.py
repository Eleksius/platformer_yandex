import arcade
from constants import *


class GameView(arcade.View):  # Новый класс для игрового процесса

    def __init__(self):
        super().__init__()

        self.tile_map = None

        self.scene = None

        self.level = 2

        self.all_coins = None

        self.collected_coins = 0

        self.hp = 3

        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.score = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.spike_sound = arcade.load_sound(":resources:sounds/gameover3.wav")
        self.end_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.background = arcade.load_texture("backgrounds/bg2.png")
        self.mega_sound = arcade.load_sound(":resources:sounds/coin3.wav")

    def setup(self, reset_coins=True):

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        map_name = "maps/map1.tmx"

        layer_options = {

            "Platforms": {

                "use_spatial_hash": True,

            },
            "spikes": {
                "use_spatial_hash": True,
            },

        }

        self.tile_map = arcade.load_tilemap(f"maps/map{self.level}.tmx", TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the spikes layer
        if "spikes" in self.tile_map.sprite_lists:
            self.scene.add_sprite_list("spikes", sprite_list=self.tile_map.sprite_lists["spikes"])

        # Keep track of the score
        if reset_coins:
            self.score = 0
        self.collected_coins = 0
        self.all_coins = len(self.scene["Coins"])

        # Set up the player with animated sprite
        from player_character import PlayerCharacter
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.physics_engine = arcade.PhysicsEnginePlatformer(

            # self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["floor"]

        )

    def on_draw(self):
        self.clear()

        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     SCREEN_WIDTH, SCREEN_HEIGHT,
        #                                     self.background)

        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()


        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            70,
            arcade.csscolor.WHITE,
            18,
        )

        coins_text = f"Coins: {self.collected_coins}/{self.all_coins}"
        arcade.draw_text(
            coins_text,
            10,
            40,
            arcade.csscolor.WHITE,
            18,
        )

        level_text = f"Level: {self.level}"
        arcade.draw_text(
            level_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        hp_text = f"HP: {self.hp}"
        arcade.draw_text(
            hp_text,
            10,
            620,
            arcade.csscolor.RED,
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
            # удаление монет
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1
            self.collected_coins += 1
            if len(self.scene["Coins"]) == 0:
                self.level += 1
                self.setup(reset_coins=False)

        # Проверка столкновения с шипами
        spike_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["spikes"]
        )

        mega_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["mega"]
        )

        if spike_hit_list:
            # Игрок умирает при касании шипов
            self.player_death()

        if mega_hit_list:
            self.score += 10
            for mega in mega_hit_list:
                mega.remove_from_sprite_lists()
            self.player_sprite.center_y = 128
            self.player_sprite.center_x = 128
            arcade.play_sound(self.mega_sound)

        # Центрирование камеры
        self.center_camera_to_player()

    def player_death(self):
        """Обработка смерти игрока"""
        self.hp -= 1
        if self.hp <= 0:
            arcade.play_sound(self.end_sound)
            from end_screen import EndScreen
            self.window.show_view(EndScreen(self.score))
        else:
            arcade.play_sound(self.spike_sound)
            self.player_sprite.center_x = 128
            self.player_sprite.center_y = 128
            # self.setup(reset_coins=True)
