import random
from ursina import Entity, Vec3, color, camera, raycast, invoke, load_texture, time
from entities.weapons.weapon_base import WeaponBase
from entities.projectiles import BulletProjectile

TEX = 'assets/textures/sprites/weapons/shotgun/'

PX = 0.0065      # UI units per source pixel: raise/lower to resize the whole gun
X_SHIFT = 0.0    # nudge the gun left/right on screen
Y_SHIFT = 0.0    # nudge the gun up/down on screen

# letter: (width_px, height_px, left_px, lift_px)
# left_px = where the sprite's left edge sits on Doom's 320-wide screen
# lift_px = how far the sprite's bottom edge sits above the bottom of the screen
GUN_FRAMES = {
    'A': (74, 50, 125, 0),
    'B': (70, 39, 129, 0),
    'C': (69, 52, 148, 0),
    'D': (132, 58, 114, 0),
    'E': (112, 62, 152, 0),
    'F': (92, 62, 175, 0),
    'G': (93, 57, 154, 0),
    'H': (90, 52, 126, 0),
}
FLASH_FRAMES = {
    'I': (48, 39, 137, 25.5),
    'J': (70, 45, 126, 25.5),
}
FIRE_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
FLASH_BY_INDEX = {0: 'I', 1: 'J'}   # flash I on the first fire frame, J on the second


class Shotgun(WeaponBase):
    def __init__(self, player=None):
        super().__init__(damage=6, range=30, ammo=8, player=player)
        self.max_ammo = 16
        self.pickup_ammo = 4

        self.pellets = 14
        self.spread_x = 0.11
        self.spread_y = 0.045
        self.fire_cooldown = 1.0
        self.cooldown_timer = 0
        self.fire_frame_duration = 0.12

        self.gun_textures = {k: load_texture(f'{TEX}SHT2{k}0.png') for k in GUN_FRAMES}
        self.flash_textures = {k: load_texture(f'{TEX}SHT2{k}0.png') for k in FLASH_FRAMES}
        self.idle_texture = self.gun_textures['A']
        self.fire_frames = [self.gun_textures[k] for k in FIRE_ORDER]
        self.projectile_texture = load_texture('assets/textures/sprites/effects/PUFFA0.png')

        # origin=(-0.5, -0.5) pins each quad by its bottom-left corner,
        # so frames of different sizes line up the way they do in Doom
        self.sprite = Entity(
            parent=self,
            model='quad',
            origin=(-0.5, -0.5),
            color=color.white,
            texture=self.idle_texture,
        )
        self.flash_sprite = Entity(
            parent=self,
            model='quad',
            origin=(-0.5, -0.5),
            color=color.white,
            texture=self.flash_textures['I'],
            visible=False,
        )
        self.flash_base = Vec3(0, 0, -0.01)

        self.place_gun('A')
        self.place_flash('I')

    def place_gun(self, letter):
        w, h, left, lift = GUN_FRAMES[letter]
        self.sprite.scale = (w * PX, h * PX)
        self.sprite.position = ((left - 160) * PX + X_SHIFT, -0.5 + lift * PX + Y_SHIFT, 0)
        self.base_position = self.sprite.position   # keeps the walking bob centred on this frame

    def place_flash(self, letter):
        w, h, left, lift = FLASH_FRAMES[letter]
        self.flash_sprite.scale = (w * PX, h * PX)
        self.flash_base = Vec3((left - 160) * PX + X_SHIFT, -0.5 + lift * PX + Y_SHIFT, -0.01)
        self.flash_sprite.position = self.flash_base

    def fire(self):
        if self.cooldown_timer > 0:
            return
        if self.ammo <= 0:
            print("Out of ammo")
            return

        self.ammo -= 1
        self.cooldown_timer = self.fire_cooldown
        self.start_fire_animation()

        travel_time = 0.08
        origin = camera.world_position
        start_pos = origin + camera.forward * 1

        for _ in range(self.pellets):
            direction = (
                camera.forward
                + camera.right * random.uniform(-self.spread_x, self.spread_x)
                + camera.up * random.uniform(-self.spread_y, self.spread_y)
            ).normalized()

            hit_info = raycast(
                origin=origin,
                direction=direction,
                distance=self.range,
                ignore=[camera],
            )
            if not hit_info.hit:
                continue

            if hasattr(hit_info.entity, 'take_damage'):
                invoke(hit_info.entity.take_damage, self.damage, delay=travel_time)

            BulletProjectile(
                start_pos=start_pos,
                end_pos=hit_info.world_point - direction * 0.3,
                travel_time=travel_time,
                texture=self.projectile_texture,
            )

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= time.dt
        super().update()

        # Keep the flash glued to the gun while the walking bob moves it
        if self.flash_sprite.visible and self.base_position is not None:
            bob = self.sprite.position - self.base_position
            self.flash_sprite.position = self.flash_base + bob

    def on_fire_frame_changed(self, index):
        # index is None when the animation ends (or the weapon is put away)
        letter = 'A' if index is None else FIRE_ORDER[index]
        self.place_gun(letter)

        flash_letter = None if index is None else FLASH_BY_INDEX.get(index)
        if flash_letter:
            self.flash_sprite.texture = self.flash_textures[flash_letter]
            self.place_flash(flash_letter)
            self.flash_sprite.visible = True
        else:
            self.flash_sprite.visible = False
