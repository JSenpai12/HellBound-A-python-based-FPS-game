from ursina import load_texture
from entities.enemy_base import EnemyBase


class Imp(EnemyBase):
    def __init__(self, position=(0, 1, 0)):
        super().__init__(health=30, position=position, scale=1.5)

        self.speed = 4

        self.walk_rotation_frames = {
            'A': {
                1: load_texture('assets/textures/sprites/enemies/imp/TROOA1.png'),
                2: load_texture('assets/textures/sprites/enemies/imp/TROOA2A8.png'),
                3: load_texture('assets/textures/sprites/enemies/imp/TROOA3A7.png'),
                4: load_texture('assets/textures/sprites/enemies/imp/TROOA4A6.png'),
                5: load_texture('assets/textures/sprites/enemies/imp/TROOA5.png'),
            },
            'B': {
                1: load_texture('assets/textures/sprites/enemies/imp/TROOB1.png'),
                2: load_texture('assets/textures/sprites/enemies/imp/TROOB2B8.png'),
                3: load_texture('assets/textures/sprites/enemies/imp/TROOB3B7.png'),
                4: load_texture('assets/textures/sprites/enemies/imp/TROOB4B6.png'),
                5: load_texture('assets/textures/sprites/enemies/imp/TROOB5.png'),
            },
            'C': {
                1: load_texture('assets/textures/sprites/enemies/imp/TROOC1.png'),
                2: load_texture('assets/textures/sprites/enemies/imp/TROOC2C8.png'),
                3: load_texture('assets/textures/sprites/enemies/imp/TROOC3C7.png'),
                4: load_texture('assets/textures/sprites/enemies/imp/TROOC4C6.png'),
                5: load_texture('assets/textures/sprites/enemies/imp/TROOC5.png'),
            },
            'D': {
                1: load_texture('assets/textures/sprites/enemies/imp/TROOD1.png'),
                2: load_texture('assets/textures/sprites/enemies/imp/TROOD2D8.png'),
                3: load_texture('assets/textures/sprites/enemies/imp/TROOD3D7.png'),
                4: load_texture('assets/textures/sprites/enemies/imp/TROOD4D6.png'),
                5: load_texture('assets/textures/sprites/enemies/imp/TROOD5.png'),
            },
        }
        self.walk_pose_order = ['A', 'B', 'C', 'D']
        self.sprite.texture = self.walk_rotation_frames['A'][1]

        self.die_frames = [
            load_texture('assets/textures/sprites/enemies/imp/TROOI0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOJ0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOK0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOL0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOM0.png'),
        ]
