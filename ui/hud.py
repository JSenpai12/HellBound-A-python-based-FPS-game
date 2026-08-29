from ursina import Entity, Text, camera, color

class HUD(Entity):
    def __init__(self, player, weapon, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.player = player
        self.weapon = weapon

        self.health_text = Text(
            parent=self,
            text='',
            position=(-0.85, -0.45),
            scale=2,
            color=color.red,
        )

        self.ammo_text = Text(
            parent=self,
            text='',
            position=(0.6, -0.45),
            scale=2,
            color=color.azure,
        )

    def update(self):
        self.health_text.text = f'HP: {max(self.player.health, 0)}'
        self.ammo_text.text = f'AMMO: {self.weapon.ammo}'
