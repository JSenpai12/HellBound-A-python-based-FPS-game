from ursina import load_texture
from entities.enemy_base import EnemyBase


class Demon(EnemyBase):
    def __init__(self, position=(0, 1, 0)):
        super().__init__(health=45, position=position, scale=1.7)

        self.speed = 6
        self.walk_rotation_frames = {
            'A': {
                1: load_texture('assets/textures/sprites/enemies/demon/SARGA1.png'),
                2: load_texture('assets/textures/sprites/enemies/demon/SARGA2A8.png'),
                3: load_texture('assets/textures/sprites/enemies/demon/SARGA3A7.png'),
                4: load_texture('assets/textures/sprites/enemies/demon/SARGA4A6.png'),
                5: load_texture('assets/textures/sprites/enemies/demon/SARGA5.png'),
            },
            'B': {
                1: load_texture('assets/textures/sprites/enemies/demon/SARGB1.png'),
                2: load_texture('assets/textures/sprites/enemies/demon/SARGB2B8.png'),
                3: load_texture('assets/textures/sprites/enemies/demon/SARGB3B7.png'),
                4: load_texture('assets/textures/sprites/enemies/demon/SARGB4B6.png'),
                5: load_texture('assets/textures/sprites/enemies/demon/SARGB5.png'),
            },
            'C': {
                1: load_texture('assets/textures/sprites/enemies/demon/SARGC1.png'),
                2: load_texture('assets/textures/sprites/enemies/demon/SARGC2C8.png'),
                3: load_texture('assets/textures/sprites/enemies/demon/SARGC3C7.png'),
                4: load_texture('assets/textures/sprites/enemies/demon/SARGC4C6.png'),
                5: load_texture('assets/textures/sprites/enemies/demon/SARGC5.png'),
            },
            'D': {
                1: load_texture('assets/textures/sprites/enemies/demon/SARGD1.png'),
                2: load_texture('assets/textures/sprites/enemies/demon/SARGD2D8.png'),
                3: load_texture('assets/textures/sprites/enemies/demon/SARGD3D7.png'),
                4: load_texture('assets/textures/sprites/enemies/demon/SARGD4D6.png'),
                5: load_texture('assets/textures/sprites/enemies/demon/SARGD5.png'),
            },
        }
        self.walk_pose_order = ['A', 'B', 'C', 'D']
        self.sprite.texture = self.walk_rotation_frames['A'][1]

        self.die_frames = [
            load_texture('assets/textures/sprites/enemies/demon/SARGI0.png'),
            load_texture('assets/textures/sprites/enemies/demon/SARGJ0.png'),
            load_texture('assets/textures/sprites/enemies/demon/SARGK0.png'),
            load_texture('assets/textures/sprites/enemies/demon/SARGL0.png'),
            load_texture('assets/textures/sprites/enemies/demon/SARGM0.png'),
        ]

