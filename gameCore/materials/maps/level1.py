import arcade

THICKNESS = 5
COLOR = arcade.color.BLUE

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

def build_level1_walls() -> arcade.SpriteList:
    walls = arcade.SpriteList(use_spatial_hash=True)

    segments = [
        # Bordes
        (30, 670, 910, 670),  # Borde superior horizontal
        (30, 670, 30, 398),   # Borde izquierdo superior
        (910, 670, 910, 398), # Borde derecho superior
        (30, 60, 910, 60),    # Borde inferior horizontal
        (30, 60, 30, 332),    # Borde izquierdo inferior
        (910, 60, 910, 332),  # Borde derecho inferior

        # Cuadrado central
        (422, 398, 520, 398),  # Borde superior horizontal
        (422, 332, 520, 332),  # Borde inferior horizontal
        (422, 398, 422, 332),  # Borde izquierdo
        (520, 398, 520, 332),  # Borde derecho

        # Cuadrante izquierdo superior
        (324, 670, 324, 602),  # Línea vertical 1
        (128, 602, 422, 602),  # Línea horizontal 1
        (422, 602, 422, 534),  # Línea vertical 2
        (30, 534, 324, 534),   # Línea horizontal 2
        (324, 534, 324, 466),  # Línea vertical 3
        (128, 466, 422, 466),  # Línea horizontal 3
        (226, 466, 226, 398),  # Línea vertical 4
        (128, 398, 324, 398),  # Línea horizontal 4

        # Cuadrante izquierdo inferior
        (324, 60, 324, 128),   # Línea vertical 1
        (128, 128, 422, 128),  # Línea horizontal 1
        (422, 128, 422, 196),  # Línea vertical 2
        (30, 196, 324, 196),   # Línea horizontal 2
        (324, 196, 324, 264),  # Línea vertical 3
        (128, 264, 422, 264),  # Línea horizontal 3
        (226, 264, 226, 332),  # Línea vertical 4
        (128, 332, 324, 332),  # Línea horizontal 4

        # Cuadrante derecho superior
        (618, 670, 618, 602),  # Línea vertical 1
        (520, 602, 814, 602),  # Línea horizontal 1
        (520, 602, 520, 534),  # Línea vertical 2
        (618, 534, 910, 534),  # Línea horizontal 2
        (618, 534, 618, 466),  # Línea vertical 3
        (520, 466, 814, 466),  # Línea horizontal 3
        (716, 466, 716, 398),  # Línea vertical 4
        (618, 398, 814, 398),  # Línea horizontal 4

        # Cuadrante derecho inferior
        (618, 60, 618, 128),   # Línea vertical 1
        (520, 128, 814, 128),  # Línea horizontal 1
        (520, 128, 520, 196),  # Línea vertical 2
        (618, 196, 910, 196),  # Línea horizontal 2
        (618, 196, 618, 264),  # Línea vertical 3
        (520, 264, 814, 264),  # Línea horizontal 3
        (716, 264, 716, 332),  # Línea vertical 4
        (618, 332, 814, 332),  # Línea horizontal 4
    ]

    for x1, y1, x2, y2 in segments:
        walls.append(_rect_from_segment(x1, y1, x2, y2))

    return walls