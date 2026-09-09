from ursina import load_texture
from entities.enemy_base import EnemyBase


class Imp(EnemyBase):
    def __init__(self, position=(0, 1, 0)):
        super().__init__(health=30, position=position, scale=1.5)

        self.walk_frames = [
            load_texture('assets/textures/sprites/enemies/imp/TROOA1.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOB1.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOC1.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOD1.png'),
        ]
        self.sprite.texture = self.walk_frames[0]

        self.die_frames = [
            load_texture('assets/textures/sprites/enemies/imp/TROOI0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOJ0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOK0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOL0.png'),
            load_texture('assets/textures/sprites/enemies/imp/TROOM0.png'),
        ]
