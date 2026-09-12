from ursina import load_texture
from entities.pickups.pickup_base import PickupBase


class HealthPickup(PickupBase):
    def __init__(self, position=(0, 1, 0), amount=25, player=None):
        super().__init__(position=position, scale=0.6)
        self.amount = amount
        self.texture = load_texture('assets/textures/sprites/items/health/MEDIA0.png')

    def on_pickup(self):
        if self.player:
            self.player.health = min(self.player.max_health, self.player.health + self.amount)
            print(f"Picked up health, now {self.player.health}")
