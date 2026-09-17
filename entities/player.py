from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import time, held_keys


class Player(FirstPersonController):
    def __init__(self, health=100, **kwargs):
        super().__init__(**kwargs)
        self.max_health = health
        self.health = health
        self.won = False

        #Stamina Attributes
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_drain_rate = 30
        self.stamina_regen_rate = 15
        self.stamina_regen_delay = 1.0
        self.stamina_regen_timer = 0
        self.sprinting = False
        self.sprint_requested = False

        self.base_speed = self.speed
        self.sprint_multiplier = 1.6

        self.stage_cleared = False
        self.has_next_level = False

    def take_damage(self, amount):
        if self.health <= 0 or self.stage_cleared:
            return
        self.health -= amount
        print(f"Player took {amount} damage, health now {self.health}")
        if self.health <= 0:
            self.die()

    def die(self):
        print("Player died")
        self.enabled = False

    def is_moving_input(self):
        return held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']

    def update(self):
        super().update()

        if self.sprint_requested and self.is_moving_input() and self.stamina > 0:
            self.sprinting = True
            self.speed = self.base_speed * self.sprint_multiplier
        elif self.sprinting and not self.is_moving_input():
            self.sprinting = False
            self.speed = self.base_speed

        if self.sprinting and self.stamina > 0:
            self.stamina -= time.dt * self.stamina_drain_rate
            self.stamina_regen_timer = self.stamina_regen_delay
            if self.stamina <= 0:
                self.stamina = 0
                self.sprinting = False
                self.speed = self.base_speed
        else:
            if self.stamina_regen_timer > 0:
                self.stamina_regen_timer -= time.dt
            else:
                self.stamina = min(self.max_stamina, self.stamina + time.dt * self.stamina_regen_rate)

    def start_sprint(self):
        self.sprint_requested = True
        if self.is_moving_input() and self.stamina > 0:
            self.sprinting = True
            self.speed = self.base_speed * self.sprint_multiplier

    def stop_sprint(self):
        self.sprint_requested = False
        self.sprinting = False
        self.speed = self.base_speed
