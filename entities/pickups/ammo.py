from ursina import load_texture
from entities.pickups.pickup_base import PickupBase


class AmmoPickup(PickupBase):
    def __init__(self, position=(0, 1, 0), amount=12, weapon=None):
        super().__init__(position=position, scale=0.6)
        self.amount = amount
        self.weapon = weapon
        self.texture = load_texture('assets/textures/sprites/items/ammo/CLIPA0.png')

    def on_pickup(self):
        if self.weapon:
            self.weapon.ammo = min(self.weapon.max_ammo, self.weapon.ammo + self.amount)
            print(f"Picked up ammo, now {self.weapon.ammo}")
