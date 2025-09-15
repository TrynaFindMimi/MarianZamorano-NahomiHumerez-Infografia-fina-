import arcade
from materials.maps.level1 import build_level1_walls
from materials.maps.level2 import build_level2_walls

class MapManager:
    def __init__(self, current_level=1):
        self.current_level = current_level
        self.builders = {
            1: build_level1_walls,
            2: build_level2_walls,
        }
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.load_level(self.current_level)

    def load_level(self, level: int):
        if level not in self.builders:
            raise ValueError(f"Level {level} not defined")
        self.current_level = level
        self.walls = self.builders[level]()

    def draw_current_map(self):
        self.walls.draw()

    def get_walls(self) -> arcade.SpriteList:
        return self.walls
