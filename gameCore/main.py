import arcade
from logicGame.mapManager import MapManager
from logicGame.pointManager import PointManager
from characters.pacman import Pacman
from characters.ghost import Ghost

SCREEN_WIDTH = 940
SCREEN_HEIGHT = 750
TILE_SIZE = 30

class PacmanGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pacman")

        # Inicializar mapa y puntos
        self.mapManager = MapManager(1)  # Cambia a 2 si quieres probar el nivel 2
        self.pointManager = PointManager(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, self.mapManager)

        # Inicializar Pacman
        self.pacman_list = arcade.SpriteList()
        self.pacman = Pacman(scale=0.35)
        self.pacman.center_x = 200
        self.pacman.center_y = 100
        self.pacman_list.append(self.pacman)

        self.speed = 8

        # Inicializar fantasmas
        self.ghosts = arcade.SpriteList()
        colors = ["rojo", "lila", "celeste", "purpura"]
        spawn_x, spawn_y = self.mapManager.get_ghost_spawn()

        for color in colors:
            ghost = Ghost(color=color, scale=0.35)
            ghost.spawn(spawn_x, spawn_y)
            self.ghosts.append(ghost)

    def setup(self):
        pass

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        self.mapManager.draw_current_map()
        self.pointManager.draw_points()
        self.pacman_list.draw()
        self.ghosts.draw()

    def on_update(self, delta_time):
        self.pacman.move(self.mapManager.get_walls(), TILE_SIZE)
        self.pacman.update_animation(delta_time)

        puntos_comidos = self.pointManager.check_collision(self.pacman)
        if puntos_comidos > 0:
            print(f"Comiste {puntos_comidos} punto(s)")

            if puntos_comidos >= 2:
                for ghost in self.ghosts:
                    ghost.set_state("normal", duration=7.0)

        for ghost in self.ghosts:
            ghost.choose_direction(self.pacman, self.mapManager.get_walls())
            ghost.move(self.mapManager.get_walls())
            ghost.update_animation(delta_time)

            if arcade.check_for_collision(ghost, self.pacman):
                if ghost.state == "normal":
                    print(f"¡{ghost.ghost_color.capitalize()} atrapó a Pac-Man!")
                elif ghost.state == "weak":
                    ghost.set_state("dead")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.pacman.started = True
            for ghost in self.ghosts:
                if ghost.state == "waiting":
                    ghost.set_state("normal")
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