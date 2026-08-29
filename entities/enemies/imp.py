from entities.enemy_base import EnemyBase

class Imp(EnemyBase):
    def __init__(self, position=(0, 1, 0)):
        super().__init__(health=30, position=position, scale=1.5)
