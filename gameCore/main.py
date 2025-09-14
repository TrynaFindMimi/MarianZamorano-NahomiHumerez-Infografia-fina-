import arcade
from logicGame.mapManager import MapManager

SCREEN_WIDTH = 940
SCREEN_HEIGHT = 750
TILE_SIZE = 30

class PacmanGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pacman")
        self.mapManager = MapManager(2)

    def setup(self):
        pass

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.mapManager.draw_current_map()
        
    def on_update(self, delta_time):
        pass

if __name__ == "__main__":
    game = PacmanGame()
    game.setup()
    arcade.run()