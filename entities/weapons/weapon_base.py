import math
from ursina import Entity, camera, mouse, raycast, distance, time, held_keys, Vec2


class WeaponBase(Entity):
    def __init__(self, damage=10, range=100, ammo=12, player=None, **kwargs):
        super().__init__(
            parent=camera.ui,
            model=None,
            **kwargs
        )

        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.max_ammo = ammo
        self.player = player

        self.sprite = None
        self.idle_texture = None
        self.fire_frames = []
        self.fire_frame_index = 0
        self.fire_frame_timer = 0
        self.fire_frame_duration = 0.05
        self.firing = False

        self.bob_timer = 0
        self.bob_speed = 6
        self.bob_amount = 0.015
        self.base_position = None

    def fire(self):
        if self.ammo <= 0:
            print("Out of ammo")
            return

        self.ammo -= 1
        self.start_fire_animation()

        hit_info = raycast(
            origin=camera.world_position,
            direction=camera.forward,
            distance=self.range,
            ignore=[camera]
        )
        if hit_info.hit:
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(self.damage)
            else:
                print(f"Hit {hit_info.entity}, but it can't take damage")
        else:
            print("Missed")

    def start_fire_animation(self):
        if not self.fire_frames or self.sprite is None:
            return
        self.firing = True
        self.fire_frame_index = 0
        self.fire_frame_timer = 0
        self.sprite.texture = self.fire_frames[0]
        self.on_fire_frame_changed(0)

    def update(self):
        if self.sprite and self.base_position is None:
            self.base_position = self.sprite.position

        if self.firing:
            self.fire_frame_timer += time.dt
            if self.fire_frame_timer >= self.fire_frame_duration:
                self.fire_frame_timer = 0
                self.fire_frame_index += 1

                if self.fire_frame_index >= len(self.fire_frames):
                    self.firing = False
                    if self.sprite and self.idle_texture:
                        self.sprite.texture = self.idle_texture
                    self.on_fire_frame_changed(None)
                else:
                    self.sprite.texture = self.fire_frames[self.fire_frame_index]
                    self.on_fire_frame_changed(self.fire_frame_index)

        self.apply_bob()

    def apply_bob(self):
        if self.base_position is None or self.player is None:
            return

        is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']

        if is_moving:
            speed_factor = self.bob_speed * (1.8 if self.player.sprinting else 1)
            self.bob_timer += time.dt * speed_factor
            bob_x = math.sin(self.bob_timer) * self.bob_amount
            bob_y = abs(math.cos(self.bob_timer)) * self.bob_amount
            self.sprite.position = self.base_position + Vec2(bob_x, bob_y)
        else:
            self.bob_timer = 0
            self.sprite.position = self.base_position

    def on_fire_frame_changed(self, index):
        """Override in subclasses that need to react to frame changes (e.g. muzzle flash overlays)."""
        pass
