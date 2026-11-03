import json
import math
from ursina import Entity, camera, color, destroy


class Minimap(Entity):
    def __init__(self, player, get_enemies=None, map_width=0.45, show_enemies=True, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.get_enemies = get_enemies
        self.map_width = map_width
        self.show_enemies = show_enemies

        self.cell_size = 4
        self.cu = 0.01  # UI units per grid cell, recalculated on load()

        # Everything lives under one container so it can be hidden as a unit
        self.container = Entity(parent=self)
        self.bg = None
        self.wall_quads = []
        self.enemy_dots = []

        self.exit_marker = Entity(parent=self.container, model='quad', color=color.lime, z=-0.02, enabled=False)
        self.player_dot = Entity(parent=self.container, model='quad', color=color.yellow, z=-0.04)
        self.player_nose = Entity(parent=self.container, model='quad', color=color.orange, z=-0.05)

    def load(self, path, exit_position=None):
        with open(path) as f:
            data = json.load(f)

        grid = data['grid']
        self.cell_size = data.get('cell_size', 4)

        width = len(grid[0])
        depth = len(grid)
        self.cu = self.map_width / width
        cu = self.cu
        map_w = width * cu
        map_h = depth * cu

        # Clear the previous level's drawing
        for q in self.wall_quads:
            destroy(q)
        self.wall_quads = []
        if self.bg:
            destroy(self.bg)

        # Top-right corner of the screen
        self.container.position = (0.87 - map_w, 0.47 - map_h)

        self.bg = Entity(
            parent=self.container,
            model='quad',
            color=color.black,
            scale=(map_w, map_h),
            position=(map_w / 2, map_h / 2, 0),
        )
        self.bg.alpha = 0.6

        # One quad per horizontal run of wall cells
        for gz, row in enumerate(grid):
            gx = 0
            while gx < width:
                if row[gx] == '1':
                    start = gx
                    while gx < width and row[gx] == '1':
                        gx += 1
                    run = gx - start
                    quad = Entity(
                        parent=self.container,
                        model='quad',
                        color=color.gray,
                        scale=(run * cu, cu),
                        position=((start + run / 2) * cu, (gz + 0.5) * cu, -0.01),
                    )
                    self.wall_quads.append(quad)
                else:
                    gx += 1

        # Marker sizes depend on cu
        self.player_dot.scale = (2.2 * cu, 2.2 * cu)
        self.player_nose.scale = (1.2 * cu, 1.2 * cu)

        if exit_position:
            self.exit_marker.scale = (2.4 * cu, 2.4 * cu)
            self.exit_marker.position = self.to_map(exit_position, -0.02)
            self.exit_marker.enabled = True
        else:
            self.exit_marker.enabled = False

    def to_map(self, pos, z):
        # World position -> position inside the container (x right, z up)
        return (
            (pos[0] / self.cell_size + 0.5) * self.cu,
            (pos[2] / self.cell_size + 0.5) * self.cu,
            z,
        )

    def update(self):
        visible = self.player.health > 0 and not self.player.stage_cleared
        if self.container.enabled != visible:
            self.container.enabled = visible
        if not visible:
            return

        cu = self.cu

        # Player dot + a small marker offset in the facing direction
        self.player_dot.position = self.to_map(self.player.position, -0.04)
        yaw = math.radians(self.player.rotation_y)
        self.player_nose.position = (
            self.player_dot.x + math.sin(yaw) * 1.8 * cu,
            self.player_dot.y + math.cos(yaw) * 1.8 * cu,
            -0.05,
        )

        # Enemies: reuse a pool of dots
        enemies = []
        if self.show_enemies and self.get_enemies:
            enemies = [e for e in self.get_enemies() if not e.dying]

        while len(self.enemy_dots) < len(enemies):
            self.enemy_dots.append(
                Entity(parent=self.container, model='quad', color=color.red, z=-0.03)
            )

        for i, dot in enumerate(self.enemy_dots):
            if i < len(enemies):
                dot.scale = (1.6 * cu, 1.6 * cu)
                dot.position = self.to_map(enemies[i].position, -0.03)
                dot.enabled = True
            else:
                dot.enabled = False
