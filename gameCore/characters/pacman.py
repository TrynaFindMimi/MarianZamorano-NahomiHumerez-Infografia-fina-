# gameCore/characters/pacman.py
import arcade
import os

class Pacman(arcade.Sprite):
    def __init__(self, scale=1):
        base_path = os.path.join(os.path.dirname(__file__), "..", "materials", "pacman")
        base_path = os.path.abspath(base_path)

        initial_image = os.path.join(base_path, "pacman_derecha_a.png")
        super().__init__(initial_image, scale=scale)

        self.textures_up = [
            arcade.load_texture(os.path.join(base_path, "pacman_arriba_a.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_arriba_a2.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_arriba_c.png")),
        ]
        self.textures_down = [
            arcade.load_texture(os.path.join(base_path, "pacman_abajo_a.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_abajo_a2.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_abajo_c.png")),
        ]
        self.textures_left = [
            arcade.load_texture(os.path.join(base_path, "pacman_izquierda_a.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_izquierda_a2.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_izquierda_c.png")),
        ]
        self.textures_right = [
            arcade.load_texture(os.path.join(base_path, "pacman_derecha_a.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_derecha_a2.png")),
            arcade.load_texture(os.path.join(base_path, "pacman_derecha_c.png")),
        ]

        self.direction = "right"
        self.current_texture_index = 0
        self.animation_speed = 0.15
        self.time_since_last_frame = 0

    def update_animation(self, delta_time: float = 1/60):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_texture_index = (self.current_texture_index + 1) % len(self.textures_right)

            if self.direction == "up":
                self.texture = self.textures_up[self.current_texture_index]
            elif self.direction == "down":
                self.texture = self.textures_down[self.current_texture_index]
            elif self.direction == "left":
                self.texture = self.textures_left[self.current_texture_index]
            elif self.direction == "right":
                self.texture = self.textures_right[self.current_texture_index]

    def move(self, dx, dy, walls: arcade.SpriteList):
        """Mueve a Pacman con colisiones contra muros, eje por eje."""
        # Dirección según intento de movimiento
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "up"
        elif dy < 0:
            self.direction = "down"

        if dx == 0 and dy == 0:
            return

        if dx != 0:
            old_x = self.center_x
            self.center_x += dx
            if arcade.check_for_collision_with_list(self, walls):
                self.center_x = old_x

        if dy != 0:
            old_y = self.center_y
            self.center_y += dy
            if arcade.check_for_collision_with_list(self, walls):
                self.center_y = old_y
