import arcade

class PointManager:
    def __init__(self, width, height, tile_size):
        self.sprite_list = arcade.SpriteList()
        self.radius = 5

        # Generar puntos en una cuadrícula
        for x in range(tile_size, width, tile_size):
            for y in range(tile_size, height, tile_size):
                # Aquí podrías evitar muros si tienes un mapa lógico
                point = arcade.SpriteCircle(self.radius, arcade.color.YELLOW)
                point.center_x = x
                point.center_y = y
                self.sprite_list.append(point)

    def draw_points(self):
        self.sprite_list.draw()

    def check_collision(self, pacman_sprite):
        """Elimina puntos que colisionen con Pac-Man y devuelve cuántos comió"""
        hit_list = arcade.check_for_collision_with_list(pacman_sprite, self.sprite_list)
        for point in hit_list:
            point.remove_from_sprite_lists()
        return len(hit_list)