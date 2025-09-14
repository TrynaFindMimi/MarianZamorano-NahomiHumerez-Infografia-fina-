import arcade

def draw_level2():
    #Bordes
    arcade.draw_line(30, 670, 910, 670, arcade.color.BLUE, 5)  # Borde superior horizontal
    arcade.draw_line(30, 670, 30, 398, arcade.color.BLUE, 5)  # Borde izquierdo superior
    arcade.draw_line(910, 670, 910, 398, arcade.color.BLUE, 5)  # Borde derecho superior
        
    arcade.draw_line(30, 60, 910, 60, arcade.color.BLUE, 5)  # Borde inferior horizontal
    arcade.draw_line(30, 60, 30, 332, arcade.color.BLUE, 5)  # Borde izquierdo inferior
    arcade.draw_line(910, 60, 910, 332, arcade.color.BLUE, 5)  # Borde derecho inferior
    
    # Cuadrado superior
    arcade.draw_line(422, 602, 520, 602, arcade.color.RED, 5)  # Borde inferior horizontal
    arcade.draw_line(422, 670, 422, 602, arcade.color.BLUE, 5)  # Borde izquierdo
    arcade.draw_line(520, 670, 520, 602, arcade.color.BLUE, 5)  # Borde derecho
    
    # Cuadrado inferior
    arcade.draw_line(422, 128, 520, 128, arcade.color.RED, 5)  # Borde superior horizontal
    arcade.draw_line(422, 60, 422, 128, arcade.color.BLUE, 5)  # Borde izquierdo
    arcade.draw_line(520, 60, 520, 128, arcade.color.BLUE, 5)  # Borde derecho
    
    # Centro vertical
    arcade.draw_line(471, 534, 471, 466, arcade.color.BLUE, 5)  # Linea vertical 1
    arcade.draw_line(324, 534, 618, 534, arcade.color.BLUE, 5)  # Linea horizontal 1
    arcade.draw_line(471, 398, 471, 332, arcade.color.BLUE, 5)  # Linea vertical 2
    arcade.draw_line(422, 398, 520, 398, arcade.color.BLUE, 5)  # Linea horizontal 2
    arcade.draw_line(422, 332, 520, 332, arcade.color.BLUE, 5)  # Linea horizontal 3
    arcade.draw_line(471, 264, 471, 196, arcade.color.BLUE, 5)  # Linea vertical 3
    arcade.draw_line(324, 196, 618, 196, arcade.color.BLUE, 5)  # Linea horizontal 4
    
    # Centro horizontal
    arcade.draw_line(128, 398, 128, 332, arcade.color.BLUE, 5)  # Linea vertical 1
    arcade.draw_line(814, 398, 814, 332, arcade.color.BLUE, 5)  # Linea vertical 2
    
    # Cuadrante superior izquierdo
    arcade.draw_line(226, 670, 226, 534, arcade.color.BLUE, 5)  # Linea vertical 1
    arcade.draw_line(128, 602, 324, 602, arcade.color.BLUE, 5)  # Linea horizontal 1
    arcade.draw_line(128, 534, 128, 466, arcade.color.BLUE, 5)  # Linea vertical 2
    arcade.draw_line(128, 466, 373, 466, arcade.color.BLUE, 5)  # Linea horizontal 2
    arcade.draw_line(226, 466, 226, 398, arcade.color.BLUE, 5)  # Linea vertical 3
    arcade.draw_line(226, 398, 324, 398, arcade.color.BLUE, 5)  # Linea horizontal 3
    
    # Cuadrante superior derecho
    arcade.draw_line(716, 670, 716, 534, arcade.color.BLUE, 5)  # Linea vertical 1
    arcade.draw_line(618, 602, 814, 602, arcade.color.BLUE, 5)  # Linea horizontal 1
    arcade.draw_line(814, 534, 814, 466, arcade.color.BLUE, 5)  # Linea vertical 2
    arcade.draw_line(569, 466, 814, 466, arcade.color.BLUE, 5)  # Linea horizontal 2
    arcade.draw_line(716, 466, 716, 398, arcade.color.BLUE, 5)  # Linea vertical 3
    arcade.draw_line(618, 398, 716, 398, arcade.color.BLUE, 5)  # Linea horizontal 3
    
    # Cuadrante inferior izquierdo
    arcade.draw_line(226, 60, 226, 128, arcade.color.BLUE, 5)  # Linea vertical 1
    arcade.draw_line(128, 128, 324, 128, arcade.color.BLUE, 5)  # Linea horizontal 1
    arcade.draw_line(128, 196, 128, 264, arcade.color.BLUE, 5)  # Linea vertical 2
    arcade.draw_line(128, 264, 373, 264, arcade.color.BLUE, 5)  # Linea horizontal 2
    arcade.draw_line(226, 264, 226, 332, arcade.color.BLUE, 5)  # Linea vertical 3
    arcade.draw_line(226, 332, 324, 332, arcade.color.BLUE, 5)  # Linea horizontal 3
    
    # Cuadrante inferior derecho
    arcade.draw_line(716, 60, 716, 196, arcade.color.BLUE, 5)  # Linea vertical 1
    arcade.draw_line(618, 128, 814, 128, arcade.color.BLUE, 5)  # Linea horizontal 1
    arcade.draw_line(814, 196, 814, 264, arcade.color.BLUE, 5)  # Linea vertical 2
    arcade.draw_line(569, 264, 814, 264, arcade.color.BLUE, 5)  # Linea horizontal 2
    arcade.draw_line(716, 264, 716, 332, arcade.color.BLUE, 5)  # Linea vertical 3
    arcade.draw_line(618, 332, 716, 332, arcade.color.BLUE, 5)  # Linea horizontal 3