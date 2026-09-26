from ursina import Entity, color, destroy, curve, load_texture, time, invoke, raycast, distance, Vec3


class BulletProjectile(Entity):
    def __init__(self, start_pos, end_pos, travel_time=0.35, texture=None, **kwargs):
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


class FireballProjectile(Entity):
    flight_frames = None
    explode_frames = None

    PLAYER_EYE_HEIGHT = 1.6  # tune to match your actual player's eye/camera height
    SPLASH_RADIUS = 1.2      # how close the target must be to the explosion point to take damage

    def __init__(self, start_pos, target, travel_time=0.6, damage=15, **kwargs):
        super().__init__(
            model='quad',
            billboard=True,
            color=color.white,
            scale=2.0,
            position=start_pos,
            **kwargs
        )
        if FireballProjectile.flight_frames is None:
            FireballProjectile.flight_frames = [
                load_texture('assets/textures/sprites/effects/fireball/BAL7A1A5.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7A2A8.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7A3A7.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7A4A6.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7B1B5.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7B2B8.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7B3B7.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7B4B6.png'),
            ]
        if FireballProjectile.explode_frames is None:
            FireballProjectile.explode_frames = [
                load_texture('assets/textures/sprites/effects/fireball/BAL7C0.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7D0.png'),
                load_texture('assets/textures/sprites/effects/fireball/BAL7E0.png'),
            ]

        self.texture = FireballProjectile.flight_frames[0]
        self.flight_frame_index = 0
        self.flight_frame_timer = 0
        self.flight_frame_duration = 0.06

        self.target = target
        self.damage = damage
        self.exploding = False
        self.explode_frame_index = 0
        self.explode_frame_timer = 0
        self.explode_frame_duration = 0.06

        # Aim at eye height, not feet.
        raw_end_pos = target.position if target else start_pos
        end_pos = raw_end_pos + Vec3(0, self.PLAYER_EYE_HEIGHT, 0) if target else raw_end_pos

        # Wall check: clip travel to the first solid thing in the way.
        self.hit_wall = False
        travel_vector = end_pos - start_pos
        travel_distance = travel_vector.length()

        if travel_distance > 0.001:
            direction = travel_vector.normalized()
            ignore_list = [self]
            if target:
                ignore_list.append(target)

            hit_info = raycast(
                origin=start_pos,
                direction=direction,
                distance=travel_distance,
                ignore=ignore_list
            )

            if hit_info.hit:
                # Stop short of the wall surface instead of passing through it.
                end_pos = hit_info.world_point - direction * 0.1
                self.hit_wall = True
                clipped_distance = distance(start_pos, end_pos)
                # Keep travel speed consistent even though the distance is shorter.
                travel_time = travel_time * (clipped_distance / travel_distance)

        self.end_pos = end_pos
        self.animate_position(end_pos, duration=travel_time, curve=curve.linear)
        invoke(self.explode, delay=travel_time)

    def explode(self):
        self.exploding = True
        self.explode_frame_index = 0
        self.texture = FireballProjectile.explode_frames[0]

        # Only damage if the fireball reached the player (not stopped by a wall)
        # AND the player is still actually near the point of detonation (dodge check).
        if not self.hit_wall and self.target and hasattr(self.target, 'take_damage'):
            current_dist = distance(self.target.position + Vec3(0, self.PLAYER_EYE_HEIGHT, 0), self.end_pos)
            if current_dist <= self.SPLASH_RADIUS:
                self.target.take_damage(self.damage)

    def update(self):
        if self.exploding:
            self.explode_frame_timer += time.dt
            if self.explode_frame_timer >= self.explode_frame_duration:
                self.explode_frame_timer = 0
                self.explode_frame_index += 1
                if self.explode_frame_index >= len(FireballProjectile.explode_frames):
                    destroy(self)
                    return
                self.texture = FireballProjectile.explode_frames[self.explode_frame_index]
        else:
            self.flight_frame_timer += time.dt
            if self.flight_frame_timer >= self.flight_frame_duration:
                self.flight_frame_timer = 0
                self.flight_frame_index = (self.flight_frame_index + 1) % len(FireballProjectile.flight_frames)
                self.texture = FireballProjectile.flight_frames[self.flight_frame_index]
