from ursina import Entity, color, destroy

class EnemyBase(Entity):
    def __init__(self, health=30, **kwargs):
        super().__init__(
            model='quad',
            billboard=True,
            color=color.red,
            collider='box',
            **kwargs
        )
        self.max_health = health
        self.health = health

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self} took {amount} damange, health now {self.health}")
        if self.health <= 0:
            self.die()

    def die(self):
        print(f"{self} died")
        destroy(self)
