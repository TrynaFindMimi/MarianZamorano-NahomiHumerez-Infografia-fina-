import arcade
import time
from logicGame.mapManager import MapManager
from logicGame.pointManager import PointManager
from characters.pacman import Pacman
from characters.ghost import Ghost
from logicGame.fruitManager import FruitManager

SCREEN_WIDTH = 940
SCREEN_HEIGHT = 750
TILE_SIZE = 30

class PacmanGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pacman")
        self.speed = 8
        self.pacman_spawn = (200, 100)
        self.ghost_spawn = None
        self.setup()

    def setup(self):
        self.mapManager = MapManager(1)
        self.pointManager = PointManager(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, self.mapManager)

        self.pacman_list = arcade.SpriteList()
        self.pacman = Pacman(scale=0.25)
        self.pacman.center_x, self.pacman.center_y = self.pacman_spawn
        self.pacman_list.append(self.pacman)

        self.ghosts = arcade.SpriteList()
        colors = ["rojo", "lila", "celeste", "purpura"]
        spawn_x, spawn_y = self.mapManager.get_ghost_spawn()
        self.ghost_spawn = (spawn_x, spawn_y)

        delay = 0
        for color in colors:
            ghost = Ghost(color=color)
            ghost.spawn(spawn_x, spawn_y, release_delay=delay)
            ghost.target_pacman = self.pacman
            self.ghosts.append(ghost)
            delay += 5
            
        self.fruitManager = FruitManager(self.mapManager)

    def restart_level(self):
        self.setup()

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.mapManager.draw_current_map()
        self.pointManager.draw_points()
        self.pacman_list.draw()
        self.ghosts.draw()
        self.fruitManager.draw_fruits()

    def on_update(self, delta_time):
        walls = self.mapManager.get_walls()

        self.pacman.move(walls, TILE_SIZE)
        self.pacman.update_animation(delta_time)

        if self.pacman.lives <= 0:
            self.restart_level()
            return

        puntos, power_pellets = self.pointManager.check_collision(self.pacman)

        if puntos > 0:
            print(f"Comiste {puntos} punto(s)")

        if power_pellets > 0:
            print(f"Comiste {power_pellets} power pellet(s)")
            for ghost in self.ghosts:
                ghost.set_state("weak", duration=7.0)

        for ghost in self.ghosts:
            ghost.move(walls)
            ghost.update_animation(delta_time)

            if arcade.check_for_collision(ghost, self.pacman):
                if ghost.state == "normal":
                    self.pacman.die(*self.pacman_spawn)
                elif ghost.state == "weak":
                    ghost.set_state("dead") 
                elif ghost.state == "dead":
                    pass
        
        self.fruitManager.check_collision(self.pacman, self.ghosts)

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
    arcade.run()
