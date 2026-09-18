from ursina import Entity, color, destroy, curve, load_texture, time, billboard, invoke


class BulletProjectile(Entity):
    def __init__(self, start_pos, end_pos, travel_time=0.08, texture=None, **kwargs):
        super().__init__(
            model='quad',
            billboard=True,
            color=color.white,
            texture=texture,
            scale=0.15,
            position=start_pos,
            **kwargs
        )
        self.end_pos = end_pos
        self.animate_position(end_pos, duration=travel_time, curve=curve.linear)
        destroy(self, delay=travel_time)
        invoke(self.spawn_impact, delay=travel_time)

    def spawn_impact(self):
        ImpactEffect(position=self.end_pos)


class ImpactEffect(Entity):
    frames = None

    def __init__(self, position, **kwargs):
        super().__init__(
            model='quad',
            billboard=True,
            color=color.white,
            scale=0.3,
            position=position,
            **kwargs
        )
        if ImpactEffect.frames is None:
            ImpactEffect.frames = [
                load_texture('assets/textures/sprites/effects/PUFFA0.png'),
                load_texture('assets/textures/sprites/effects/PUFFB0.png'),
                load_texture('assets/textures/sprites/effects/PUFFC0.png'),
                load_texture('assets/textures/sprites/effects/PUFFD0.png'),
            ]

        self.texture = ImpactEffect.frames[0]
        self.frame_index = 0
        self.frame_duration = 0.05
        self.frame_timer = 0

    def update(self):
        self.frame_timer += time.dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(ImpactEffect.frames):
                destroy(self)
                return
            self.texture = ImpactEffect.frames[self.frame_index]
