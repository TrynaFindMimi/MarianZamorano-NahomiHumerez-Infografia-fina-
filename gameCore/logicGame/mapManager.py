from materials.maps.level1 import draw_level1
from materials.maps.level2 import draw_level2

class MapManager:
    def __init__(self, current_level=1):
        self.current_level = current_level
        self.level_drawers = {
            1: draw_level1,
            2: draw_level2
        }

    def draw_current_map(self):
        if self.current_level in self.level_drawers:
            self.level_drawers[self.current_level]()
        else:
            raise ValueError(f"Level {self.current_level} not defined")