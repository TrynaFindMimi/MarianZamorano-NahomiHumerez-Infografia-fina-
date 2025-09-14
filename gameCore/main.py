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
        self.mapManager = MapManager(1)
        self.pointManager = PointManager(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)

        # Crear una SpriteList para Pac-Man
        self.pacman_list = arcade.SpriteList()
        self.pacman = Pacman(scale=0.3)
        self.pacman.center_x = 60
        self.pacman.center_y = 60
        self.pacman_list.append(self.pacman)
        self.speed = 4

        self.pressed_keys = set()

    def setup(self):
        pass

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.mapManager.draw_current_map()
        self.pointManager.draw_points()
        self.pacman_list.draw()

    def on_update(self, delta_time):
        dx = dy = 0
        if arcade.key.UP in self.pressed_keys:
            dy = self.speed
        if arcade.key.DOWN in self.pressed_keys:
            dy = -self.speed
        if arcade.key.LEFT in self.pressed_keys:
            dx = -self.speed
        if arcade.key.RIGHT in self.pressed_keys:
            dx = self.speed

        self.pacman.move(dx, dy)
        self.pacman.update_animation(delta_time)

        puntos_comidos = self.pointManager.check_collision(self.pacman)
        if puntos_comidos > 0:
            print(f"Comiste {puntos_comidos} punto(s)")

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        self.pressed_keys.discard(key)

if __name__ == "__main__":
    game = PacmanGame()
    game.setup()
    arcade.run()