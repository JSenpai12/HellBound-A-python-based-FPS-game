from ursina import Entity, Button, color, camera, application


class MainMenu(Entity):
    def __init__(self, on_start, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.on_start = on_start

        self.background = Entity(
            parent=self,
            model='quad',
            texture='assets/textures/ui/HellBoundTitle.png',
            scale=(2, 1.13),
            z=1,
        )


        self.start_button = Button(
            parent=self,
            texture='assets/textures/ui/M_NGAME.png',
            color=color.red,
            scale=(0.30, 0.06),
            position=(0, -0.1),
        )
        self.start_button.on_click = self.start_game

        self.quit_button = Button(
            parent=self,
            texture='assets/textures/ui/M_QUITG.png',
            color=color.gray,
            scale=(0.2, 0.08),
            position=(0, -0.22),
        )
        self.quit_button.on_click = application.quit

    def start_game(self):
        self.enabled = False
        self.on_start()
