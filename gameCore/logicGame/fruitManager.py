import time
import arcade
import random
import os

class FruitManager:
    def __init__(self, map_manager):
        from materials.maps.level1 import get_wall_segments_level1, COLLISION_RADIUS
        self.segments = get_wall_segments_level1()
        self.collision_radius = COLLISION_RADIUS

        self.fruit_list = arcade.SpriteList()
        self.fruit_effects = {
            "cereza": self.freeze_ghosts,
            "frutilla": self.teleport_pacman,
            "pera": self.double_points
        }

        self.spawn_fruits()

    def spawn_fruits(self):
        fruit_types = ["cereza", "frutilla", "pera"]
        positions = self._valid_positions()
        selected_positions = random.sample(positions, len(fruit_types))

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "materials", "fruits"))

        for fruit_type, (x, y) in zip(fruit_types, selected_positions):
            image_path = os.path.join(base_path, f"{fruit_type}.png")
            fruit = arcade.Sprite(image_path, scale=0.15)
            fruit.center_x = x
            fruit.center_y = y
            fruit.fruit_type = fruit_type
            self.fruit_list.append(fruit)

    def _valid_positions(self):
        x_positions = list(range(30, 910 - 49, 49))
        y_positions = list(range(60, 670 - 34, 34))
        valid = []
        for cy in y_positions:
            for cx in x_positions:
                if 422 <= cx <= 520 and 332 <= cy <= 398:
                    continue
                if self._in_wall(cx, cy):
                    continue
                valid.append((cx, cy))
        return valid

    def _point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        vx, vy = x2 - x1, y2 - y1
        wx, wy = px - x1, py - y1
        v_len2 = vx * vx + vy * vy
        if v_len2 == 0:
            return ((px - x1)**2 + (py - y1)**2)**0.5
        t = max(0.0, min(1.0, (wx * vx + wy * vy) / v_len2))
        projx = x1 + t * vx
        projy = y1 + t * vy
        return ((px - projx)**2 + (py - projy)**2)**0.5

    def _in_wall(self, px, py):
        for x1, y1, x2, y2 in self.segments:
            if self._point_to_segment_distance(px, py, x1, y1, x2, y2) <= self.collision_radius:
                return True
        return False

    def draw_fruits(self):
        self.fruit_list.draw()

    def check_collision(self, pacman, ghost_list):
        hit_fruits = arcade.check_for_collision_with_list(pacman, self.fruit_list)
        for fruit in hit_fruits:
            fruit_type = fruit.fruit_type
            fruit.remove_from_sprite_lists()
            if fruit_type in self.fruit_effects:
                self.fruit_effects[fruit_type](pacman, ghost_list)

    def freeze_ghosts(self, pacman, ghost_list):
        for ghost in ghost_list:
            ghost.freeze(duration=3.0)

    def teleport_pacman(self, pacman, ghost_list):
        farthest = max(self._valid_positions(), key=lambda pos: ((pacman.center_x - pos[0])**2 + (pacman.center_y - pos[1])**2))
        pacman.center_x, pacman.center_y = farthest

    def double_points(self, pacman, ghost_list):
        pacman.double_points_until = time.time() + 7.0
        print("🍐 ¡Multiplicador de puntos activado por 7 segundos!")

