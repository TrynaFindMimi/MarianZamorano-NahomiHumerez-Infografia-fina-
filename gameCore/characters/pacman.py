import arcade
import os
from typing import Tuple

class Pacman(arcade.Sprite):
    def __init__(self, scale=1, tile_size=30):
        base_path = os.path.join(os.path.dirname(__file__), "..", "materials", "pacman")
        base_path = os.path.abspath(base_path)

        # Textura inicial
        self.start_texture = arcade.load_texture(os.path.join(base_path, "pacman_inicio.png"))
        initial_image = os.path.join(base_path, "pacman_inicio.png")
        super().__init__(initial_image, scale=scale)

        # Animaciones
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

        # Estado
        self.direction = "right"
        self.current_texture_index = 0
        self.animation_speed = 0.15
        self.time_since_last_frame = 0

        self.started = False

        # Velocidades actual y deseada
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0

        # Grilla
        self.tile_size = tile_size
        self.epsilon = 3

    def _aligned_axis(self, value: float) -> bool:
        remainder = (value - self.tile_size / 2) % self.tile_size
        return remainder < self.epsilon or remainder > (self.tile_size - self.epsilon)

    def _snap_axis(self, value: float) -> float:
        snapped = round((value - self.tile_size / 2) / self.tile_size) * self.tile_size + self.tile_size / 2
        return snapped

    def _try_direction(self, walls: arcade.SpriteList, vx: float, vy: float) -> bool:
        if vx == 0 and vy == 0:
            return False
        old_x, old_y = self.center_x, self.center_y
        self.center_x += vx
        self.center_y += vy
        collided = len(arcade.check_for_collision_with_list(self, walls)) > 0
        self.center_x, self.center_y = old_x, old_y
        return not collided

    def set_next_direction(self, dx: float, dy: float):
        if dx != 0 and dy != 0:
            return
        self.next_dx = dx
        self.next_dy = dy

    def update_animation(self, delta_time: float = 1/60):
        if not self.started:
            self.texture = self.start_texture
            return

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

    def move(self, walls: arcade.SpriteList, tile_size: int = None):
        if tile_size is not None and tile_size != self.tile_size:
            self.tile_size = tile_size

        if not self.started:
            return
        
        if self.dx == 0 and self.dy == 0 and (self.next_dx != 0 or self.next_dy != 0):
            if self._try_direction(walls, self.next_dx, self.next_dy):
                self.dx, self.dy = self.next_dx, self.next_dy

        turning_horizontal = self.next_dx != 0 and self.next_dy == 0
        turning_vertical = self.next_dy != 0 and self.next_dx == 0

        if turning_horizontal and self._aligned_axis(self.center_y):
            if not self._aligned_axis(self.center_y):
                self.center_y = self._snap_axis(self.center_y)
            if self._try_direction(walls, self.next_dx, 0):
                self.dx, self.dy = self.next_dx, 0

        elif turning_vertical and self._aligned_axis(self.center_x):
            if not self._aligned_axis(self.center_x):
                self.center_x = self._snap_axis(self.center_x)
            if self._try_direction(walls, 0, self.next_dy):
                self.dx, self.dy = 0, self.next_dy

        if self.dx > 0:
            self.direction = "right"
        elif self.dx < 0:
            self.direction = "left"
        elif self.dy > 0:
            self.direction = "up"
        elif self.dy < 0:
            self.direction = "down"

        if self.dx != 0:
            old_x = self.center_x
            self.center_x += self.dx
            if arcade.check_for_collision_with_list(self, walls):
                self.center_x = old_x
                self.dx = 0

        if self.dy != 0:
            old_y = self.center_y
            self.center_y += self.dy
            if arcade.check_for_collision_with_list(self, walls):
                self.center_y = old_y
                self.dy = 0

        puerta_y_min = 332
        puerta_y_max = 398
        if self.center_x <= 30 and puerta_y_min <= self.center_y <= puerta_y_max:
            self.center_x = 910
        elif self.center_x >= 910 and puerta_y_min <= self.center_y <= puerta_y_max:
            self.center_x = 30

        if self.dx != 0 and self._aligned_axis(self.center_y):
            self.center_y = self._snap_axis(self.center_y)
        if self.dy != 0 and self._aligned_axis(self.center_x):
            self.center_x = self._snap_axis(self.center_x)