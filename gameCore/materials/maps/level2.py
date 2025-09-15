import arcade
import math

# Configuración de paredes
WALL_THICKNESS = 5
COLOR = arcade.color.BLUE
SAFETY_MARGIN = 0  # hitbox reducido a línea exacta
COLLISION_RADIUS = WALL_THICKNESS / 2 + SAFETY_MARGIN

# Lista de segmentos (x1, y1, x2, y2)
WALLS_LEVEL2 = [
    # Bordes
    (30, 670, 910, 670),
    (30, 670, 30, 398),
    (910, 670, 910, 398),
    (30, 60, 910, 60),
    (30, 60, 30, 332),
    (910, 60, 910, 332),

    # Cuadrado superior
    (422, 602, 520, 602),
    (422, 670, 422, 602),
    (520, 670, 520, 602),

    # Cuadrado inferior
    (422, 128, 520, 128),
    (422, 60, 422, 128),
    (520, 60, 520, 128),

    # Centro vertical
    (471, 534, 471, 466),
    (324, 534, 618, 534),
    (471, 398, 471, 332),
    (422, 398, 520, 398),
    (422, 332, 520, 332),
    (471, 264, 471, 196),
    (324, 196, 618, 196),

    # Centro horizontal
    (128, 398, 128, 332),
    (814, 398, 814, 332),

    # Cuadrante superior izquierdo
    (226, 670, 226, 534),
    (128, 602, 324, 602),
    (128, 534, 128, 466),
    (128, 466, 373, 466),
    (226, 466, 226, 398),
    (226, 398, 324, 398),

    # Cuadrante superior derecho
    (716, 670, 716, 534),
    (618, 602, 814, 602),
    (814, 534, 814, 466),
    (569, 466, 814, 466),
    (716, 466, 716, 398),
    (618, 398, 716, 398),

    # Cuadrante inferior izquierdo
    (226, 60, 226, 128),
    (128, 128, 324, 128),
    (128, 196, 128, 264),
    (128, 264, 373, 264),
    (226, 264, 226, 332),
    (226, 332, 324, 332),

    # Cuadrante inferior derecho
    (716, 60, 716, 196),
    (618, 128, 814, 128),
    (814, 196, 814, 264),
    (569, 264, 814, 264),
    (716, 264, 716, 332),
    (618, 332, 716, 332),
]

# --- Funciones de dibujo y colisión ---

def draw_level2():
    """Dibuja las paredes del nivel 2."""
    for x1, y1, x2, y2 in WALLS_LEVEL2:
        arcade.draw_line(x1, y1, x2, y2, COLOR, WALL_THICKNESS)

def get_wall_hitboxes():
    """Devuelve una lista de sprites sólidos para las paredes."""
    hitboxes = []
    for x1, y1, x2, y2 in WALLS_LEVEL2:
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
    """Calcula la distancia mínima de un punto a un segmento."""
    vx, vy = x2 - x1, y2 - y1
    wx, wy = px - x1, py - y1
    v_len2 = vx * vx + vy * vy
    if v_len2 == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / v_len2))
    projx = x1 + t * vx
    projy = y1 + t * vy
    return math.hypot(px - projx, py - projy)

def _in_wall_level2(px, py):
    """Devuelve True si el punto está sobre una pared."""
    for x1, y1, x2, y2 in WALLS_LEVEL2:
        if _point_to_segment_distance(px, py, x1, y1, x2, y2) <= COLLISION_RADIUS:
            return True
    return False

def get_level2_matrix(width, height, tile_size):
    """Genera una matriz del nivel 2 para lógica de juego."""
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
            if _in_wall_level2(cx, cy):
                matrix[row][col] = 1
            else:
                matrix[row][col] = 0
    # Marcar esquinas con valor especial (ej. power pellets)
    corners = [(1, 1), (cols - 2, 1), (1, rows - 2), (cols - 2, rows - 2)]
    for c, r in corners:
        if matrix[r][c] == 0:
            matrix[r][c] = 2
    return matrix
