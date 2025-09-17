import time
import arcade
import math
import random
from util.gameState import GameState

class PointManager:
    def __init__(self, width, height, tile_size, map_manager):
        if map_manager.current_level == 1:
            from materials.maps.level1 import get_wall_segments_level1, COLLISION_RADIUS
            self.segments = get_wall_segments_level1()
            self.collision_radius = COLLISION_RADIUS
        elif map_manager.current_level == 2:
            from materials.maps.level2 import get_wall_segments_level2, COLLISION_RADIUS
            self.segments = get_wall_segments_level2()
            self.collision_radius = COLLISION_RADIUS
        else:
            raise ValueError(f"Level {map_manager.current_level} not supported for points")

        self.sprite_list = arcade.SpriteList()
        self.power_pellet_list = arcade.SpriteList()

        x_positions = list(range(30, 910 - 49, 49))
        y_positions = list(range(60, 670 - 34, 34))

        point_positions = []
        for cy in y_positions:
            for cx in x_positions:
                if 422 <= cx <= 520 and 332 <= cy <= 398:
                    continue
                if self._in_wall(cx, cy):
                    continue
                point_positions.append((cx, cy))

        power_positions = random.sample(point_positions, 4)

        total_points = 0
        for cx, cy in point_positions:
            if (cx, cy) in power_positions:
                pellet = arcade.SpriteCircle(10, arcade.color.WHITE)
                pellet.center_x = cx
                pellet.center_y = cy
                self.power_pellet_list.append(pellet)
            else:
                point = arcade.SpriteCircle(3, arcade.color.YELLOW)
                point.center_x = cx
                point.center_y = cy
                self.sprite_list.append(point)
                total_points += 1

        print(f"Total pacdots: {total_points}")
        print(f"Total super pacdots: {len(self.power_pellet_list)}")

    def _generate_wall_sprites(self):
        wall_sprites = arcade.SpriteList()
        for x1, y1, x2, y2 in self.segments:
            if y1 == y2:
                length = int(abs(x2 - x1))
                width, height = length, 5
                cx = (x1 + x2) / 2
                cy = y1
            elif x1 == x2:
                length = int(abs(y2 - y1))
                width, height = 5, length
                cx = x1
                cy = (y1 + y2) / 2
            else:
                continue
            wall = arcade.SpriteSolidColor(width, height, arcade.color.BLUE)
            wall.center_x = cx
            wall.center_y = cy
            wall_sprites.append(wall)
        return wall_sprites

    def _point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        vx, vy = x2 - x1, y2 - y1
        wx, wy = px - x1, py - y1
        v_len2 = vx * vx + vy * vy
        if v_len2 == 0:
            return math.hypot(px - x1, py - y1)
        t = max(0.0, min(1.0, (wx * vx + wy * vy) / v_len2))
        projx = x1 + t * vx
        projy = y1 + t * vy
        return math.hypot(px - projx, py - projy)

    def _in_wall(self, px, py):
        for x1, y1, x2, y2 in self.segments:
            if self._point_to_segment_distance(px, py, x1, y1, x2, y2) <= self.collision_radius:
                return True
        return False

    def draw_points(self):
        self.sprite_list.draw()
        self.power_pellet_list.draw()

    def check_collision(self, pacman_sprite):
        hit_points = arcade.check_for_collision_with_list(pacman_sprite, self.sprite_list)
        for point in hit_points:
            point.remove_from_sprite_lists()
            
        hit_power = arcade.check_for_collision_with_list(pacman_sprite, self.power_pellet_list)
        for pellet in hit_power:
            pellet.remove_from_sprite_lists()
        
        puntos = len(hit_points)
        power_pellets = len(hit_power)

        if hasattr(pacman_sprite, "double_points_until") and time.time() < pacman_sprite.double_points_until:
            puntos *= 2
            print("🍐 ¡Puntos duplicados por efecto de la pera!")

        GameState.add_score(puntos * 10)
        GameState.add_score(power_pellets * 50)

        return len(hit_points), len(hit_power)