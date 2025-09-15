import arcade
import math

WALLS_LEVEL1 = [
    (30, 670, 910, 670),
    (30, 670, 30, 398),
    (910, 670, 910, 398),
    (30, 60, 910, 60),
    (30, 60, 30, 332),
    (910, 60, 910, 332),
    (422, 398, 520, 398),
    (422, 332, 520, 332),
    (422, 398, 422, 332),
    (520, 398, 520, 332),
    (324, 670, 324, 602),
    (128, 602, 422, 602),
    (422, 602, 422, 534),
    (30, 534, 324, 534),
    (324, 534, 324, 466),
    (128, 466, 422, 466),
    (226, 466, 226, 398),
    (128, 398, 324, 398),
    (324, 60, 324, 128),
    (128, 128, 422, 128),
    (422, 128, 422, 196),
    (30, 196, 324, 196),
    (324, 196, 324, 264),
    (128, 264, 422, 264),
    (226, 264, 226, 332),
    (128, 332, 324, 332),
    (618, 670, 618, 602),
    (520, 602, 814, 602),
    (520, 602, 520, 534),
    (618, 534, 910, 534),
    (618, 534, 618, 466),
    (520, 466, 814, 466),
    (716, 466, 716, 398),
    (618, 398, 814, 398),
    (618, 60, 618, 128),
    (520, 128, 814, 128),
    (520, 128, 520, 196),
    (618, 196, 910, 196),
    (618, 196, 618, 264),
    (520, 264, 814, 264),
    (716, 264, 716, 332),
    (618, 332, 814, 332),
]

def draw_level1():
    for x1, y1, x2, y2 in WALLS_LEVEL1:
        arcade.draw_line(x1, y1, x2, y2, arcade.color.BLUE, 5)

def get_wall_hitboxes():
    hitboxes = []
    thickness = 5
    for x1, y1, x2, y2 in WALLS_LEVEL1:
        length = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        transparent_color = (0, 0, 0, 0)
        wall = arcade.SpriteSolidColor(int(length), thickness, transparent_color)
        wall.center_x = center_x
        wall.center_y = center_y
        wall.angle = angle
        hitboxes.append(wall)
    return hitboxes

def get_level_matrix(width, height, tile_size):
    wall_list = arcade.SpriteList()
    for wall in get_wall_hitboxes():
        wall_list.append(wall)
    rows = height // tile_size
    cols = width // tile_size
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            x = col * tile_size + tile_size // 2
            y = row * tile_size + tile_size // 2
            probe = arcade.SpriteSolidColor(tile_size, tile_size, (0, 0, 0, 0))
            probe.center_x = x
            probe.center_y = y
            if arcade.check_for_collision_with_list(probe, wall_list):
                matrix[row][col] = 1
            else:
                matrix[row][col] = 0
    for col in range(cols):
        pellet_placed = False
        for row in range(rows):
            if matrix[row][col] == 0:
                if not pellet_placed:
                    pellet_placed = True
                else:
                    matrix[row][col] = 2
    return matrix
