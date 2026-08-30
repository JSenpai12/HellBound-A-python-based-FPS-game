from ursina import Entity, color, distance


class ExitTrigger(Entity):
    def __init__(self, on_trigger, player, trigger_range=1.5, position=(0, 1, 0), **kwargs):
        super().__init__(
            model='cube',
            color=color.green,
            scale=1,
            position=position,
            **kwargs
        )
        self.on_trigger = on_trigger
        self.player = player
        self.trigger_range = trigger_range
        self.triggered = False

    def update(self):
        if self.triggered:
            return
        if distance(self.position, self.player.position) <= self.trigger_range:
            self.triggered = True
            self.on_trigger()
