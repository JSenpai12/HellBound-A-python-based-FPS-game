from ursina import Entity, color, load_texture
from entities.weapons.weapon_base import WeaponBase


class Pistol(WeaponBase):
    def __init__(self):
        super().__init__(damage=15, range=50, ammo=100)

        self.idle_texture = load_texture('assets/textures/sprites/weapons/pistol/PISGA0.png')
        self.fire_frames = [
            load_texture('assets/textures/sprites/weapons/pistol/PISGB0.png'),
            load_texture('assets/textures/sprites/weapons/pistol/PISGC0.png'),
            load_texture('assets/textures/sprites/weapons/pistol/PISGD0.png'),
            load_texture('assets/textures/sprites/weapons/pistol/PISGE0.png'),
        ]
        self.flash_texture = load_texture('assets/textures/sprites/weapons/pistol/PISFA0.png')

        # base gun sprite
        self.sprite = Entity(
            parent=self,
            model='quad',
            color=color.white,
            texture=self.idle_texture,
            scale=(0.3, 0.3),
            position=(0.4, -0.35),
        )

        # muzzle flash overlay, sits in front of the gun sprite (lower z = closer to camera)
        self.flash_sprite = Entity(
            parent=self,
            model='quad',
            color=color.white,
            texture=self.flash_texture,
            scale=(0.3, 0.3),
            position=(0.38, -0.20, -0.01),
            visible=False,
        )

        # which fire_frames index(es) should show the flash
        self.flash_frame_indices = {0}   # flash shows on the first fire frame, like Doom's muzzle-flash state

    def on_fire_frame_changed(self, index):
        if index in self.flash_frame_indices:
            self.flash_sprite.visible = True
        else:
            self.flash_sprite.visible = False
