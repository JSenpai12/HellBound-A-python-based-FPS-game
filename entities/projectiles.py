from ursina import Entity, color, destroy, curve


class BulletProjectile(Entity):
    def __init__(self, start_pos, end_pos, travel_time=0.08, **kwargs):
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.05,
            position=start_pos,
            **kwargs
        )
        self.animate_position(end_pos, duration=travel_time, curve=curve.linear)
        destroy(self, delay=travel_time)
