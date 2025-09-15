import arcade
import math
from materials.maps.level1 import WALLS_LEVEL1, COLLISION_RADIUS

class PointManager:
    def __init__(self, tile_size, level_matrix, map_width, map_height, ghost_cell_bounds=None):
        self.sprite_list = arcade.SpriteList()
        self.power_pellet_list = arcade.SpriteList()

        x_positions = [79, 149, 210, 289, 359, 429, 499, 569, 639, 699, 779, 849]
        y_positions = [89, 159, 229, 299, 369, 439, 509, 579, 649]


        if ghost_cell_bounds:
            (gc_col_min, gc_row_min), (gc_col_max, gc_row_max) = ghost_cell_bounds
        else:
            gc_col_min = gc_row_min = gc_col_max = gc_row_max = -1

        cols = len(x_positions)
        rows = len(y_positions)

        for row, cy in enumerate(y_positions):
            for col, cx in enumerate(x_positions):
                if gc_col_min <= col <= gc_col_max and gc_row_min <= row <= gc_row_max:
                    continue
                if 422 <= cx <= 520 and 323 <= cy <= 398:
                    continue
                if self._in_wall(cx, cy):
                    continue
                if (col, row) in [(0, 0), (cols - 1, 0), (0, rows - 1), (cols - 1, rows - 1)]:
                    pellet = arcade.SpriteCircle(7, arcade.color.WHITE)
                    pellet.center_x = cx
                    pellet.center_y = cy
                    self.power_pellet_list.append(pellet)
                else:
                    point = arcade.SpriteCircle(3, arcade.color.YELLOW)
                    point.center_x = cx
                    point.center_y = cy
                    self.sprite_list.append(point)

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
        for x1, y1, x2, y2 in WALLS_LEVEL1:
            if self._point_to_segment_distance(px, py, x1, y1, x2, y2) <= COLLISION_RADIUS:
                return True
        return False

    def draw_points(self):
        self.sprite_list.draw()
        self.power_pellet_list.draw()

    def check_collision(self, pacman_sprite):
        eaten = arcade.check_for_collision_with_list(pacman_sprite, self.sprite_list)
        for p in eaten:
            p.remove_from_sprite_lists()
        eaten_power = arcade.check_for_collision_with_list(pacman_sprite, self.power_pellet_list)
        for p in eaten_power:
            p.remove_from_sprite_lists()
        return len(eaten) + len(eaten_power)
