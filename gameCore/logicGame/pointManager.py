import arcade

class PointManager:
    def __init__(self, tile_size, level_matrix):
        self.sprite_list = arcade.SpriteList()
        self.radius = 5
        self.tile_size = tile_size

        ghost_cell_x1 = 422
        ghost_cell_y1 = 332
        ghost_cell_x2 = 520
        ghost_cell_y2 = 398

        rows = len(level_matrix)
        cols = len(level_matrix[0])

        for row in range(rows):
            for col in range(cols):
                if level_matrix[row][col] == 0:  # libre
                    x = col * tile_size + tile_size // 2
                    y = row * tile_size + tile_size // 2

                    if ghost_cell_x1 <= x <= ghost_cell_x2 and ghost_cell_y1 <= y <= ghost_cell_y2:
                        continue

                    point = arcade.SpriteCircle(self.radius, arcade.color.YELLOW)
                    point.center_x = x
                    point.center_y = y
                    self.sprite_list.append(point)

    def draw_points(self):
        self.sprite_list.draw()

    def check_collision(self, pacman_sprite):
        hit_list = arcade.check_for_collision_with_list(pacman_sprite, self.sprite_list)
        for point in hit_list:
            point.remove_from_sprite_lists()
        return len(hit_list)
