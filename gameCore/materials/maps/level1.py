import arcade

def draw_level1():
    #Bordes
        arcade.draw_line(30, 670, 910, 670, arcade.color.BLUE, 5)  # Borde superior horizontal
        arcade.draw_line(30, 670, 30, 398, arcade.color.BLUE, 5)  # Borde izquierdo superior
        arcade.draw_line(910, 670, 910, 398, arcade.color.BLUE, 5)  # Borde derecho superior
        
        arcade.draw_line(30, 60, 910, 60, arcade.color.BLUE, 5)  # Borde inferior horizontal
        arcade.draw_line(30, 60, 30, 332, arcade.color.BLUE, 5)  # Borde izquierdo inferior
        arcade.draw_line(910, 60, 910, 332, arcade.color.BLUE, 5)  # Borde derecho inferior
        
        # Cuadrado al centro con líneas
        arcade.draw_line(422, 398, 520, 398, arcade.color.RED, 5)  # Borde superior horizontal
        arcade.draw_line(422, 332, 520, 332, arcade.color.BLUE, 5)  # Borde inferior horizontal
        arcade.draw_line(422, 398, 422, 332, arcade.color.BLUE, 5)  # Borde izquierdo
        arcade.draw_line(520, 398, 520, 332, arcade.color.BLUE, 5)  # Borde derecho
        
        # Cuadrante izquierdo superior
        arcade.draw_line(324, 670, 324, 602, arcade.color.BLUE, 5)  # Linea vertical 1
        arcade.draw_line(128, 602, 422, 602, arcade.color.BLUE, 5)  # Linea horizontal 1
        arcade.draw_line(422, 602, 422, 534, arcade.color.BLUE, 5)  # Linea vertical 2
        arcade.draw_line(30, 534, 324, 534, arcade.color.BLUE, 5)  # Linea horizontal 2
        arcade.draw_line(324, 534, 324, 466, arcade.color.BLUE, 5)  # Linea vertical 3
        arcade.draw_line(128, 466, 422, 466, arcade.color.BLUE, 5)  # Linea horizontal 3
        arcade.draw_line(226, 466, 226, 398, arcade.color.BLUE, 5)  # Linea vertical 4
        arcade.draw_line(128, 398, 324, 398, arcade.color.BLUE, 5)  # Linea horizontal 4
        
        # Cuadrante izquierdo inferior
        arcade.draw_line(324, 60, 324, 128, arcade.color.BLUE, 5)  # línea vertical 1
        arcade.draw_line(128, 128, 422, 128, arcade.color.BLUE, 5)  # Linea horizontal 1
        arcade.draw_line(422, 128, 422, 196, arcade.color.BLUE, 5)  # línea vertical 2
        arcade.draw_line(30, 196, 324, 196, arcade.color.BLUE, 5)  # Linea horizontal 2
        arcade.draw_line(324, 196, 324, 264, arcade.color.BLUE, 5)  # línea vertical 3
        arcade.draw_line(128, 264, 422, 264, arcade.color.BLUE, 5)  # Linea horizontal 3
        arcade.draw_line(226, 264, 226, 332, arcade.color.BLUE, 5)  # línea vertical 4
        arcade.draw_line(128, 332, 324, 332, arcade.color.BLUE, 5)  # Linea horizontal 4
        
        # Cuadrante derecho superior
        arcade.draw_line(618, 670, 618, 602, arcade.color.BLUE, 5)  # Linea vertical 1
        arcade.draw_line(520, 602, 814, 602, arcade.color.BLUE, 5)  # Linea horizontal 1
        arcade.draw_line(520, 602, 520, 534, arcade.color.BLUE, 5)  # Linea vertical 2
        arcade.draw_line(618, 534, 910, 534, arcade.color.BLUE, 5)  # Linea horizontal 2
        arcade.draw_line(618, 534, 618, 466, arcade.color.BLUE, 5)  # Linea vertical 3
        arcade.draw_line(520, 466, 814, 466, arcade.color.BLUE, 5)  # Linea horizontal 3
        arcade.draw_line(716, 466, 716, 398, arcade.color.BLUE, 5)  # Linea vertical 4
        arcade.draw_line(618, 398, 814, 398, arcade.color.BLUE, 5)  # Linea horizontal 4
        
        # Cuadrante derecho inferior
        arcade.draw_line(618, 60, 618, 128, arcade.color.BLUE, 5)  # Linea vertical 1
        arcade.draw_line(520, 128, 814, 128, arcade.color.BLUE, 5)  # Linea horizontal 1
        arcade.draw_line(520, 128, 520, 196, arcade.color.BLUE, 5)  # Linea vertical 2
        arcade.draw_line(618, 196, 910, 196, arcade.color.BLUE, 5)  # Linea horizontal 2
        arcade.draw_line(618, 196, 618, 264, arcade.color.BLUE, 5)  # Linea vertical 3
        arcade.draw_line(520, 264, 814, 264, arcade.color.BLUE, 5)  # Linea horizontal 3
        arcade.draw_line(716, 264, 716, 332, arcade.color.BLUE, 5)  # Linea vertical 4
        arcade.draw_line(618, 332, 814, 332, arcade.color.BLUE, 5)  # Linea horizontal 4