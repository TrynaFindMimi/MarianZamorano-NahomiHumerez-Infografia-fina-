import arcade
import os
import time
from util.gameState import GameState

SCREEN_WIDTH = 940
SCREEN_HEIGHT = 750

class Pacman(arcade.Sprite):
    def __init__(self, scale=1, tile_size=30):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "materials", "pacman"))
        self.start_texture = arcade.load_texture(os.path.join(base_path, "pacman_inicio.png"))
        initial_image = os.path.join(base_path, "pacman_inicio.png")
        super().__init__(initial_image, scale=scale)

        self.textures_up = [arcade.load_texture(os.path.join(base_path, f"pacman_arriba_{s}.png")) for s in ["a", "a2", "c"]]
        self.textures_down = [arcade.load_texture(os.path.join(base_path, f"pacman_abajo_{s}.png")) for s in ["a", "a2", "c"]]
        self.textures_left = [arcade.load_texture(os.path.join(base_path, f"pacman_izquierda_{s}.png")) for s in ["a", "a2", "c"]]
        self.textures_right = [arcade.load_texture(os.path.join(base_path, f"pacman_derecha_{s}.png")) for s in ["a", "a2", "c"]]
        self.death_textures = [arcade.load_texture(os.path.join(base_path, f"pacman_muerto{i}.png")) for i in range(1, 6)]

        self.direction = "right"
        self.current_texture_index = 0
        self.animation_speed = 0.15
        self.time_since_last_frame = 0

        self.started = False
        self.dx = self.dy = self.next_dx = self.next_dy = 0
        self.speed = 0.5
        self.tile_size = tile_size
        self.epsilon = 3

        self.lives = 3
        self.is_dying = False
        self.death_frame_index = 0
        self.death_frame_time = 0.2
        self.death_timer = 0.0
        self.invulnerable_until = 0.0
        self.respawn_x = self.respawn_y = None
        self._invuln_time = 1.5
        self.double_points_until = 0.0

    def is_invulnerable(self):
        return time.time() < self.invulnerable_until

    def die(self, spawn_x, spawn_y, invuln_time=1.5):
        if self.is_dying or self.is_invulnerable():
            return
        self.is_dying = True
        self.death_frame_index = 0
        self.death_timer = self.death_frame_time
        self.dx = self.dy = self.next_dx = self.next_dy = 0
        self.started = False
        self.respawn_x, self.respawn_y = spawn_x, spawn_y
        self._invuln_time = invuln_time
        self.texture = self.death_textures[0]

    def _handle_respawn(self):
        self.lives = max(0, self.lives - 1)
        GameState.lives = self.lives

        if self.lives <= 0:
            self.is_dying = False
            return

        if self.respawn_x is not None and self.respawn_y is not None:
            self.center_x = self.respawn_x
            self.center_y = self.respawn_y

        self.invulnerable_until = time.time() + self._invuln_time
        self.is_dying = False
        self.started = True
        self.dx = self.dy = self.next_dx = self.next_dy = 0
        self.texture = self.start_texture

    def update_animation(self, delta_time: float = 1/60):
        if self.is_dying:
            self.death_timer -= delta_time
            if self.death_timer <= 0:
                self.death_frame_index += 1
                if self.death_frame_index < len(self.death_textures):
                    self.texture = self.death_textures[self.death_frame_index]
                    self.death_timer = self.death_frame_time
                else:
                    self._handle_respawn()
            return

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

    def set_next_direction(self, dx: float, dy: float):
        if dx != 0 and dy != 0:
            return
        self.next_dx = dx * self.speed
        self.next_dy = dy * self.speed

    def move(self, walls: arcade.SpriteList, tile_size: int = None):
        if tile_size is not None:
            self.tile_size = tile_size
        if not self.started or self.is_dying:
            return

        if self.dx == 0 and self.dy == 0 and (self.next_dx != 0 or self.next_dy != 0):
            if self._try_direction(walls, self.next_dx, self.next_dy):
                self.dx, self.dy = self.next_dx, self.next_dy

        if self.next_dx != 0 and self.next_dy == 0 and self._aligned_axis(self.center_y):
            if self._try_direction(walls, self.next_dx, 0):
                self.dx, self.dy = self.next_dx, 0
        elif self.next_dy != 0 and self.next_dx == 0 and self._aligned_axis(self.center_x):
            if self._try_direction(walls, 0, self.next_dy):
                self.dx, self.dy = 0, self.next_dy

        if self.dx > 0: self.direction = "right"
        elif self.dx < 0: self.direction = "left"
        elif self.dy > 0: self.direction = "up"
        elif self.dy < 0: self.direction = "down"

        self.center_x += self.dx
        if arcade.check_for_collision_with_list(self, walls):
            self.center_x -= self.dx
            self.dx = 0

        self.center_y += self.dy
        if arcade.check_for_collision_with_list(self, walls):
            self.center_y -= self.dy
            self.dy = 0

        puerta_y_min = 332
        puerta_y_max = 398
        if self.center_x <= 30 and puerta_y_min <= self.center_y <= puerta_y_max:
            self.center_x = SCREEN_WIDTH - 30
        elif self.center_x >= SCREEN_WIDTH - 30 and puerta_y_min <= self.center_y <= puerta_y_max:
            self.center_x = 30

        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = 0
        elif self.center_y <= 0:
            self.center_y = SCREEN_HEIGHT

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

    def teleport_to(self, x, y):
        self.center_x = x
        self.center_y = y
        self.dx = self.dy = self.next_dx = self.next_dy = 0