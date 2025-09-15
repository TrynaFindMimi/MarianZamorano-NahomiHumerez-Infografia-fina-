import arcade
import math

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

        # Define positions with steps of 49x and 34y, constrained within playable area
        x_positions = list(range(30, 910 - 49, 49))  # Start at 30, end before 910, step 49
        y_positions = list(range(60, 670 - 34, 34))  # Start at 60, end before 670, step 34

        cols = len(x_positions)
        rows = len(y_positions)

        # Count points and power pellets before placement
        total_points = 0
        for row, cy in enumerate(y_positions):
            for col, cx in enumerate(x_positions):
                # Skip central/ghost area
                if 422 <= cx <= 520 and 332 <= cy <= 398:
                    continue
                # Skip if in wall
                if self._in_wall(cx, cy):
                    continue
                total_points += 1

        # Print total number of points (regular + power pellets)
        print(f"Total points to be placed in the map: {total_points}")

        # Place points and power pellets
        for row, cy in enumerate(y_positions):
            for col, cx in enumerate(x_positions):
                # Skip central/ghost area
                if 422 <= cx <= 520 and 332 <= cy <= 398:
                    continue
                # Skip if in wall
                if self._in_wall(cx, cy):
                    continue
                # Power pellets at corners
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
        for x1, y1, x2, y2 in self.segments:
            if self._point_to_segment_distance(px, py, x1, y1, x2, y2) <= self.collision_radius:
                return True
        return False

    def draw_points(self):
        self.sprite_list.draw()
        self.power_pellet_list.draw()

    def check_collision(self, pacman_sprite):
        """Elimina puntos que colisionen con Pac-Man y devuelve cuántos comió"""
        hit_list = arcade.check_for_collision_with_list(pacman_sprite, self.sprite_list)
        for point in hit_list:
            point.remove_from_sprite_lists()
        hit_power = arcade.check_for_collision_with_list(pacman_sprite, self.power_pellet_list)
        for p in hit_power:
            p.remove_from_sprite_lists()
        return len(hit_list) + len(hit_power)