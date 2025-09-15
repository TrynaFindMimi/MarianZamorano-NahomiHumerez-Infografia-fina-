import arcade

THICKNESS = 5
COLOR = arcade.color.BLUE
SAFETY_MARGIN = 2
COLLISION_RADIUS = THICKNESS / 2 + SAFETY_MARGIN

WALLS_LEVEL2 = [
    # Bordes
    (30, 670, 910, 670),  # Borde superior horizontal
    (30, 670, 30, 398),   # Borde izquierdo superior
    (910, 670, 910, 398), # Borde derecho superior
    (30, 60, 910, 60),    # Borde inferior horizontal
    (30, 60, 30, 332),    # Borde izquierdo inferior
    (910, 60, 910, 332),  # Borde derecho inferior

    # Cuadrado superior
    (422, 602, 520, 602),  # Borde inferior horizontal
    (422, 670, 422, 602),  # Borde izquierdo
    (520, 670, 520, 602),  # Borde derecho

    # Cuadrado inferior
    (422, 128, 520, 128),  # Borde superior horizontal
    (422, 60, 422, 128),   # Borde izquierdo
    (520, 60, 520, 128),   # Borde derecho

    # Centro vertical
    (471, 534, 471, 466),  # Linea vertical 1
    (324, 534, 618, 534),  # Linea horizontal 1
    (471, 398, 471, 332),  # Linea vertical 2
    (422, 398, 520, 398),  # Linea horizontal 2
    (422, 332, 520, 332),  # Linea horizontal 3
    (471, 264, 471, 196),  # Linea vertical 3
    (324, 196, 618, 196),  # Linea horizontal 4

    # Centro horizontal
    (128, 398, 128, 332),  # Linea vertical 1
    (814, 398, 814, 332),  # Linea vertical 2

    # Cuadrante superior izquierdo
    (226, 670, 226, 534),  # Linea vertical 1
    (128, 602, 324, 602),  # Linea horizontal 1
    (128, 534, 128, 466),  # Linea vertical 2
    (128, 466, 373, 466),  # Linea horizontal 2
    (226, 466, 226, 398),  # Linea vertical 3
    (226, 398, 324, 398),  # Linea horizontal 3

    # Cuadrante superior derecho
    (716, 670, 716, 534),  # Linea vertical 1
    (618, 602, 814, 602),  # Linea horizontal 1
    (814, 534, 814, 466),  # Linea vertical 2
    (569, 466, 814, 466),  # Linea horizontal 2
    (716, 466, 716, 398),  # Linea vertical 3
    (618, 398, 716, 398),  # Linea horizontal 3

    # Cuadrante inferior izquierdo
    (226, 60, 226, 128),   # Linea vertical 1
    (128, 128, 324, 128),  # Linea horizontal 1
    (128, 196, 128, 264),  # Linea vertical 2
    (128, 264, 373, 264),  # Linea horizontal 2
    (226, 264, 226, 332),  # Linea vertical 3
    (226, 332, 324, 332),  # Linea horizontal 3

    # Cuadrante inferior derecho
    (716, 60, 716, 196),   # Linea vertical 1
    (618, 128, 814, 128),  # Linea horizontal 1
    (814, 196, 814, 264),  # Linea vertical 2
    (569, 264, 814, 264),  # Linea horizontal 2
    (716, 264, 716, 332),  # Linea vertical 3
    (618, 332, 716, 332),  # Linea horizontal 3
]

def _rect_from_segment(x1, y1, x2, y2, thickness=THICKNESS, color=COLOR) -> arcade.Sprite:
    if y1 == y2:
        # Horizontal
        length = int(abs(x2 - x1))
        width, height = length, thickness
        cx = (x1 + x2) / 2
        cy = y1
    elif x1 == x2:
        # Vertical
        length = int(abs(y2 - y1))
        width, height = thickness, length
        cx = x1
        cy = (y1 + y2) / 2
    else:
        raise ValueError("Solo segmentos horizontales o verticales.")
    sprite = arcade.SpriteSolidColor(width, height, color)
    sprite.center_x = cx
    sprite.center_y = cy
    return sprite

def build_level2_walls() -> arcade.SpriteList:
    walls = arcade.SpriteList(use_spatial_hash=True)

    for x1, y1, x2, y2 in WALLS_LEVEL2:
        walls.append(_rect_from_segment(x1, y1, x2, y2))

    return walls

def get_wall_segments_level2():
    return WALLS_LEVEL2

def get_ghost_spawn_level2():
    return 471, 636