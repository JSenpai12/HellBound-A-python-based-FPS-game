from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self, health=100, **kwargs):
        super().__init__(**kwargs)
        self.max_health = health
        self.health = health

    def take_damage(self, amount):
        if self.health <= 0:
            return
        self.health -= amount
        print(f"Player took {amount} damage, health now {self.health}")
        if self.health <= 0:
            self.die()

    def die(self):
        print("Player died")
        self.enabled = False
