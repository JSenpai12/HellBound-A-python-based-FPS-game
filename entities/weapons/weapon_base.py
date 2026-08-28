from ursina import Entity, camera, mouse, raycast, distance

class WeaponBase(Entity):
    def __init__(self, damage=10, range=100, **kwargs):
        super().__init__(
            parent=camera.ui,
            model=None,
            **kwargs
        )

        self.damage = damage
        self.range = range

    def fire(self):
        hit_info = raycast(
            origin = camera.world_position,
            direction = camera.forward,
            distance = self.range,
            ignore = [camera]
        )
        if hit_info.hit:
            print(f"Hit {hit_info} for {self.damage} damage at distance {hit_info.distance}")
        else:
            print("Missed")
