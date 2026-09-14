from ursina import Entity, Text, camera, color, time


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

        self.game_over_text = Text(
            parent=self,
            text='',
            position=(-0.3, 0),
            scale=3,
            color=color.red,
            z=-0.1,
        )

        self.win_text = Text(
            parent=self,
            text='',
            position=(-0.3, 0),
            scale=3,
            color=color.lime,
        )
        self.stamina_text = Text(
            parent=self,
            text='',
            position=(-0.85, -0.4),
            scale=1.5,
            color=color.yellow,
        )

        self.death_screen = Entity(
            parent=self,
            model='quad',
            texture='assets/textures/ui/death_screen_ui.png',
            color=color.white,
            scale=(2, 1.13),
            z=0.5,
            enabled=False,
        )

    def update(self):
        is_dead = self.player.health <= 0

        self.health_text.enabled = not is_dead
        self.ammo_text.enabled = not is_dead
        self.stamina_text.enabled = not is_dead

        self.health_text.text = f'HP: {max(self.player.health, 0)}'
        self.ammo_text.text = f'AMMO: {self.weapon.ammo}'
        self.stamina_text.text = f'STAMINA: {int(self.player.stamina)}'

        self.death_screen.enabled = is_dead

        if getattr(self.player, 'won', False):
            self.win_text.text = 'LEVEL COMPLETE! Press R to Restart'
        else:
            self.win_text.text = ''
