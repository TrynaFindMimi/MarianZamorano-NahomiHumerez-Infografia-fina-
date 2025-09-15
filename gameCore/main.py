import arcade
from logicGame.mapManager import MapManager
from logicGame.pointManager import PointManager
from characters.pacman import Pacman

SCREEN_WIDTH = 940
SCREEN_HEIGHT = 750
TILE_SIZE = 30
GHOST_CELL_BOUNDS = ((12, 13), (17, 16))

class PacmanGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pacman")
        arcade.set_background_color(arcade.color.BLACK)

        self.mapManager = MapManager(2)
        self.wall_list = self.mapManager.get_current_walls()

        self.pointManager = PointManager(
            TILE_SIZE,
            None,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            ghost_cell_bounds=GHOST_CELL_BOUNDS
        )

        self.pacman_list = arcade.SpriteList()
        self.pacman = Pacman(scale=0.3)
        self.pacman.center_x = 200
        self.pacman.center_y = 100
        self.pacman_list.append(self.pacman)
        self.speed = 4

        self.physics_engine = arcade.PhysicsEngineSimple(self.pacman, self.wall_list)
        self.pressed_keys = set()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
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

        self.pacman.change_x = dx
        self.pacman.change_y = dy
        self.physics_engine.update()
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
