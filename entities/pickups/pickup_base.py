from ursina import Entity, color, distance, destroy

class PickupBase(Entity):
    def __init__(self, position=(0, 1, 0), pickup_range=1.5, **kwargs):
        super().__init__(
            model='quad',
            billboard=True,
            color=color.white,
            position=position,
            **kwargs
        )
        self.pickup_range = pickup_range
        self.player = None

    def set_player(self, player):
        self.player = player

    def update(self):
        if self.player is None:
            return
        if distance(self.position, self.player.position) <= self.pickup_range:
            self.on_pickup()
            destroy(self)

    def on_pickup(self):
        """Override in subclasses to apply the actual effect."""
        pass
