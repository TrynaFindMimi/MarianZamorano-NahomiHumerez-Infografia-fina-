import arcade
import os
import random
from typing import Tuple

class Ghost(arcade.Sprite):
    def __init__(self, color: str, scale=1, tile_size=30):
        base_path = os.path.join(os.path.dirname(__file__), "..", "materials", "ghosts")
        base_path = os.path.abspath(base_path)

        self.tile_size = tile_size
        self.epsilon = 3
        self.ghost_color = color

        self.textures_up = [arcade.load_texture(os.path.join(base_path, f"fantasma_{color}_arriba.png"))]
        self.textures_down = [arcade.load_texture(os.path.join(base_path, f"fantasma_{color}_abajo.png"))]
        self.textures_left = [arcade.load_texture(os.path.join(base_path, f"fantasma_{color}_izquierda.png"))]
        self.textures_right = [arcade.load_texture(os.path.join(base_path, f"fantasma_{color}_derecha.png"))]
        self.weak_textures = [
            arcade.load_texture(os.path.join(base_path, "fantasma_debil.png")),
            arcade.load_texture(os.path.join(base_path, "fantasma_debil2.png")),
        ]

        initial_image = os.path.join(base_path, f"fantasma_{color}_abajo.png")
        super().__init__(initial_image, scale=scale)

        self.state = "waiting"  # waiting, normal, weak, dead
        self.speed = 2
        self.dx = 0
        self.dy = 0
        self.direction = "down"
        self.time_since_last_frame = 0
        self.animation_speed = 0.3
        self.current_texture_index = 0
        self.weak_timer = 0
        self.blinking = False

    def spawn(self, x: float, y: float):
        self.center_x = x
        self.center_y = y
        self.dx = 0
        self.dy = 0
        self.state = "waiting"

    def _aligned_axis(self, value: float) -> bool:
        remainder = (value - self.tile_size / 2) % self.tile_size
        return remainder < self.epsilon or remainder > (self.tile_size - self.epsilon)

    def _snap_axis(self, value: float) -> float:
        return round((value - self.tile_size / 2) / self.tile_size) * self.tile_size + self.tile_size / 2

    def _try_direction(self, walls: arcade.SpriteList, vx: float, vy: float) -> bool:
        old_x, old_y = self.center_x, self.center_y
        self.center_x += vx
        self.center_y += vy
        collided = len(arcade.check_for_collision_with_list(self, walls)) > 0
        self.center_x, self.center_y = old_x, old_y
        return not collided

    def _distance_to(self, target: arcade.Sprite, direction: Tuple[float, float]) -> float:
        x = self.center_x + direction[0]
        y = self.center_y + direction[1]
        return ((x - target.center_x) ** 2 + (y - target.center_y) ** 2) ** 0.5

    def choose_direction(self, pacman: arcade.Sprite, walls: arcade.SpriteList):
        if self.state == "waiting":
            return

        if not self._aligned_axis(self.center_x) or not self._aligned_axis(self.center_y):
            return

        options = [(0, self.speed), (0, -self.speed), (self.speed, 0), (-self.speed, 0)]
        valid = [d for d in options if self._try_direction(walls, *d)]

        if self.state == "weak":
            valid.sort(key=lambda d: -self._distance_to(pacman, d))
        elif self.state == "dead":
            valid.sort(key=lambda d: self._distance_to(pacman, d))
        else:
            random.shuffle(valid)

        if valid:
            self.dx, self.dy = valid[0]

    def move(self, walls: arcade.SpriteList):
        if self.state == "waiting":
            return

        if self.dx != 0 and self._aligned_axis(self.center_y):
            self.center_y = self._snap_axis(self.center_y)
        if self.dy != 0 and self._aligned_axis(self.center_x):
            self.center_x = self._snap_axis(self.center_x)

        old_x, old_y = self.center_x, self.center_y
        self.center_x += self.dx
        self.center_y += self.dy

        if arcade.check_for_collision_with_list(self, walls):
            self.center_x = old_x
            self.center_y = old_y
            self.dx = 0
            self.dy = 0

    def update_animation(self, delta_time: float = 1/60):
        self.time_since_last_frame += delta_time

        if self.state == "weak":
            self.weak_timer -= delta_time
            if self.weak_timer <= 0:
                self.set_state("normal")
            elif self.weak_timer <= 2:
                self.blinking = True
            else:
                self.blinking = False

        if self.state == "weak":
            if self.blinking:
                if self.time_since_last_frame >= self.animation_speed:
                    self.time_since_last_frame = 0
                    self.current_texture_index = (self.current_texture_index + 1) % len(self.weak_textures)
                self.texture = self.weak_textures[self.current_texture_index]
            else:
                self.texture = self.weak_textures[0]
        else:
            if self.dx > 0:
                self.texture = self.textures_right[0]
            elif self.dx < 0:
                self.texture = self.textures_left[0]
            elif self.dy > 0:
                self.texture = self.textures_up[0]
            elif self.dy < 0:
                self.texture = self.textures_down[0]

    def set_state(self, new_state: str, duration: float = 7.0):
        self.state = new_state
        if new_state == "dead":
            self.speed = 4
            self.weak_timer = 0
        elif new_state == "weak":
            self.speed = 1
            self.weak_timer = duration
        elif new_state == "normal":
            self.speed = 2
            self.weak_timer = 0