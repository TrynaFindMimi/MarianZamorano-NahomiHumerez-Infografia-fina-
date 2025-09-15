import arcade
import math

WALLS_LEVEL1 = [
    (15, 675, 915, 675),
    (15, 675, 15, 395),
    (915, 675, 915, 395),
    (15, 65, 915, 65),
    (15, 65, 15, 335),
    (915, 65, 915, 335),
    (425, 395, 525, 395),
    (425, 335, 525, 335),
    (425, 395, 425, 335),
    (525, 395, 525, 335),
    (325, 675, 325, 605),
    (125, 605, 425, 605),
    (425, 605, 425, 535),
    (15, 535, 325, 535),
    (325, 535, 325, 465),
    (125, 465, 425, 465),
    (225, 465, 225, 395),
    (125, 395, 325, 395),
    (325, 65, 325, 125),
    (125, 125, 425, 125),
    (425, 125, 425, 195),
    (15, 195, 325, 195),
    (325, 195, 325, 265),
    (125, 265, 425, 265),
    (225, 265, 225, 335),
    (125, 335, 325, 335),
    (615, 675, 615, 605),
    (525, 605, 815, 605),
    (525, 605, 525, 535),
    (615, 535, 915, 535),
    (615, 535, 615, 465),
    (525, 465, 815, 465),
    (715, 465, 715, 395),
    (615, 395, 815, 395),
    (615, 65, 615, 125),
    (525, 125, 815, 125),
    (525, 125, 525, 195),
    (615, 195, 915, 195),
    (615, 195, 615, 265),
    (525, 265, 815, 265),
    (715, 265, 715, 335),
    (615, 335, 815, 335),
]

WALL_THICKNESS = 5
SAFETY_MARGIN = 2
COLLISION_RADIUS = WALL_THICKNESS / 2 + SAFETY_MARGIN

def draw_level1():
    for x1, y1, x2, y2 in WALLS_LEVEL1:
        arcade.draw_line(x1, y1, x2, y2, arcade.color.BLUE, WALL_THICKNESS)

def get_wall_hitboxes():
    hitboxes = []
    for x1, y1, x2, y2 in WALLS_LEVEL1:
        length = math.hypot(x2 - x1, y2 - y1)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        wall = arcade.SpriteSolidColor(int(length), WALL_THICKNESS, (0, 0, 0, 0))
        wall.center_x = cx
        wall.center_y = cy
        wall.angle = angle
        hitboxes.append(wall)
    return hitboxes

def _point_to_segment_distance(px, py, x1, y1, x2, y2):
    vx, vy = x2 - x1, y2 - y1
    wx, wy = px - x1, py - y1
    v_len2 = vx * vx + vy * vy
    if v_len2 == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / v_len2))
    projx = x1 + t * vx
    projy = y1 + t * vy
    return math.hypot(px - projx, py - projy)

def _in_wall(px, py):
    for x1, y1, x2, y2 in WALLS_LEVEL1:
        if _point_to_segment_distance(px, py, x1, y1, x2, y2) <= COLLISION_RADIUS:
            return True
    return False

def get_level_matrix(width, height, tile_size):
    rows = height // tile_size
    cols = width // tile_size
    matrix = [[1 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        cy = row * tile_size + tile_size / 2
        for col in range(cols):
            cx = col * tile_size + tile_size / 2
            if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                matrix[row][col] = 1
                continue
            if _in_wall(cx, cy):
                matrix[row][col] = 1
            else:
                matrix[row][col] = 0
    corners = [(1, 1), (cols - 2, 1), (1, rows - 2), (cols - 2, rows - 2)]
    for c, r in corners:
        if matrix[r][c] == 0:
            matrix[r][c] = 2
    return matrix
