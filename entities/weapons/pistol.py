from ursina import Entity, color
from entities.weapons.weapon_base import WeaponBase

class Pistol(WeaponBase):
    def __init__(self):
        super().__init__(damage=15, range=50)
        self.sprite = Entity(
            parent=self,
            model='quad',
            color=color.green,
            scale=(0.3, 0.3),
            position=(0.4, -0.3),
        )
