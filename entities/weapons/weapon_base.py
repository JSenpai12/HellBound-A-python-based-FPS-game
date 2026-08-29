from ursina import Entity, camera, mouse, raycast, distance

class WeaponBase(Entity):
    def __init__(self, damage=10, range=100, ammo=12, **kwargs):
        super().__init__(
            parent=camera.ui,
            model=None,
            **kwargs
        )

        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.max_ammo = ammo

    def fire(self):
        if self.ammo <= 0:
            print("Out of ammo")
            return

        self.ammo -= 1
        hit_info = raycast(
            origin = camera.world_position,
            direction = camera.forward,
            distance = self.range,
            ignore = [camera]
        )
        if hit_info.hit:
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(self.damage)
            else:
                print(f"Hit {hit_info.entity}, but cant take damage")
        else:
            print("Missed")
