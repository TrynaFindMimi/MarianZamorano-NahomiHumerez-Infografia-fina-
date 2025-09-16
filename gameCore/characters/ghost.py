import arcade, os, random, time
from typing import Optional

SCREEN_WIDTH = 940

class Ghost(arcade.Sprite):
    def __init__(self, color: str, scale=0.25, tile_size=30):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "materials", "ghosts"))
        self.tile_size, self.epsilon, self.ghost_color = tile_size, 3, color
        self.textures_up    = [arcade.load_texture(os.path.join(base, f"fantasma_{color}_arriba.png"))]
        self.textures_down  = [arcade.load_texture(os.path.join(base, f"fantasma_{color}_abajo.png"))]
        self.textures_left  = [arcade.load_texture(os.path.join(base, f"fantasma_{color}_izquierda.png"))]
        self.textures_right = [arcade.load_texture(os.path.join(base, f"fantasma_{color}_derecha.png"))]
        self.weak_textures  = [
            arcade.load_texture(os.path.join(base, "fantasma_debil.png")),
            arcade.load_texture(os.path.join(base, "fantasma_debil2.png"))
        ]
        self.dead_texture   = arcade.load_texture(os.path.join(base, "fantasma_debil2.png"))
        super().__init__(os.path.join(base, f"fantasma_{color}_abajo.png"), scale=scale)
        self.state, self.speed = "normal", 2
        self.dx = self.dy = 0
        self.time_since_last_frame = 0
        self.animation_speed = 0.3
        self.current_texture_index = 0
        self.weak_timer = 0
        self.blinking = False
        self.spawn_time = self.release_time = 0
        self.last_dir_change = time.time()
        self.target_pacman: Optional[arcade.Sprite] = None
        self.spawn_x = self.spawn_y = 0
        self.spawn_radius = 55  # zona más amplia
        self.respawn_delay = 2.0
        self.respawn_timer = 0.0

    def _aligned_axis(self, v):
        return (v - self.tile_size/2) % self.tile_size < self.epsilon or (v - self.tile_size/2) % self.tile_size > self.tile_size - self.epsilon

    def _snap_axis(self, v):
        return round((v - self.tile_size/2) / self.tile_size) * self.tile_size + self.tile_size/2

    def _near_spawn(self):
        return abs(self.center_x - self.spawn_x) <= self.spawn_radius and abs(self.center_y - self.spawn_y) <= self.spawn_radius

    def _distance_to(self, tx, ty, d):
        return ((self.center_x + d[0] - tx)**2 + (self.center_y + d[1] - ty)**2) ** 0.5

    def _try_direction(self, walls, vx, vy):
        if self._near_spawn():
            return True
        ox, oy = self.center_x, self.center_y
        self.center_x += vx
        self.center_y += vy
        col = arcade.check_for_collision_with_list(self, walls)
        self.center_x, self.center_y = ox, oy
        return not col

    def set_state(self, s, duration=7.0):
        self.state, self.current_texture_index, self.time_since_last_frame = s, 0, 0
        if s == "dead":
            self.speed, self.dx, self.dy, self.weak_timer = 4, 0, 0, 0
        elif s == "weak":
            self.speed, self.weak_timer, self.blinking = 1, duration, False
        elif s == "normal":
            self.speed, self.weak_timer, self.blinking = 2, 0, False

    def spawn(self, x, y, release_delay):
        self.center_x, self.center_y, self.spawn_x, self.spawn_y = x, y, x, y
        self.set_state("normal")
        self.spawn_time = time.time()
        self.release_time = self.spawn_time + release_delay
        self.dx, self.dy = random.choice([(0,self.speed),(0,-self.speed),(self.speed,0),(-self.speed,0)])

    def choose_direction(self, pacman, walls):
        opts = [(0,self.speed),(0,-self.speed),(self.speed,0),(-self.speed,0)]
        valid = [d for d in opts if self._try_direction(walls,*d)]
        if not valid:
            return
        if self.state == "dead":
            valid.sort(key=lambda d: self._distance_to(self.spawn_x, self.spawn_y, d))
        elif self.state == "weak" and pacman:
            valid.sort(key=lambda d: -self._distance_to(pacman.center_x, pacman.center_y, d))
        elif pacman:
            valid.sort(key=lambda d: self._distance_to(pacman.center_x, pacman.center_y, d))
        else:
            random.shuffle(valid)
        self.dx, self.dy = valid[0]

    def _teleport_if_needed(self):
        if self.center_x <= 0 and 332 <= self.center_y <= 398:
            self.center_x = SCREEN_WIDTH
        elif self.center_x >= SCREEN_WIDTH and 332 <= self.center_y <= 398:
            self.center_x = 0

    def move(self, walls):
        now = time.time()
        if self.state == "respawning":
            self.respawn_timer -= (now - self.last_dir_change)
            self.last_dir_change = now
            if self.respawn_timer <= 0:
                self.set_state("normal")
            return
        if self.state == "dead" or (now - self.last_dir_change) >= 3:
            self.choose_direction(self.target_pacman if self.state != "dead" else None, walls)
            self.last_dir_change = now
        if self.dx and self._aligned_axis(self.center_y):
            self.center_y = self._snap_axis(self.center_y)
        if self.dy and self._aligned_axis(self.center_x):
            self.center_x = self._snap_axis(self.center_x)
        ox, oy = self.center_x, self.center_y
        self.center_x += self.dx
        self.center_y += self.dy
        self._teleport_if_needed()
        if not self._near_spawn() and arcade.check_for_collision_with_list(self, walls):
            self.center_x, self.center_y = ox, oy
            self.choose_direction(self.target_pacman if self.state != "dead" else None, walls)
        if self.state == "dead" and self._near_spawn():
            self.state = "respawning"
            self.respawn_timer = self.respawn_delay
            self.last_dir_change = now
            self.dx, self.dy = 0, 0

    def update_animation(self, dt=1/60):
        self.time_since_last_frame += dt
        def cycle_textures(tex_list):
            if self.time_since_last_frame >= self.animation_speed:
                self.time_since_last_frame = 0
                self.current_texture_index = (self.current_texture_index + 1) % len(tex_list)
            self.texture = tex_list[self.current_texture_index]
        if self.state == "weak":
            self.weak_timer -= dt
            if self.weak_timer <= 0:
                self.set_state("normal")
            elif self.weak_timer <= 2:
                self.blinking = True
            else:
                self.blinking = False
            cycle_textures(self.weak_textures if self.blinking else [self.weak_textures[0]])
        elif self.state == "dead":
            self.texture = self.dead_texture
        elif self.state == "respawning":
            cycle_textures(self.weak_textures)
        else:
            if   self.dx > 0: self.texture = self.textures_right[0]
            elif self.dx < 0: self.texture = self.textures_left[0]
            elif self.dy > 0: self.texture = self.textures_up[0]
            elif self.dy < 0: self.texture = self.textures_down[0]
