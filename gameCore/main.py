import arcade
from logicGame.mapManager import MapManager
from logicGame.pointManager import PointManager
from characters.pacman import Pacman

SCREEN_WIDTH = 940
SCREEN_HEIGHT = 750
TILE_SIZE = 30

class PacmanGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pacman")

        # Cargar mapa y puntos
        self.mapManager = MapManager(2)  # Nivel 2
        self.pointManager = PointManager(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)

        # Obtener hitboxes reales de las paredes
        self.walls_hitbox = self.mapManager.get_walls()  # Debe devolver SpriteList de hitboxes

        # Crear Pacman
        self.pacman_list = arcade.SpriteList()
        self.pacman = Pacman(scale=0.25)  # Más pequeño
        self.pacman.center_x = 200
        self.pacman.center_y = 100
        self.pacman_list.append(self.pacman)

        self.speed = 4

    def setup(self):
        pass

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.mapManager.draw_current_map()
        self.pointManager.draw_points()
        self.pacman_list.draw()

    def on_update(self, delta_time):
        # Mover Pacman usando el hitbox real
        self.pacman.move(self.walls_hitbox, TILE_SIZE)
        self.pacman.update_animation(delta_time)

        puntos_comidos = self.pointManager.check_collision(self.pacman)
        if puntos_comidos > 0:
            print(f"Comiste {puntos_comidos} punto(s)")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.pacman.started = True
        elif key == arcade.key.UP:
            self.pacman.set_next_direction(0, self.speed)
        elif key == arcade.key.DOWN:
            self.pacman.set_next_direction(0, -self.speed)
        elif key == arcade.key.LEFT:
            self.pacman.set_next_direction(-self.speed, 0)
        elif key == arcade.key.RIGHT:
            self.pacman.set_next_direction(self.speed, 0)

    def on_key_release(self, key, modifiers):
        pass


if __name__ == "__main__":
    game = PacmanGame()
    game.setup()
    arcade.run()
