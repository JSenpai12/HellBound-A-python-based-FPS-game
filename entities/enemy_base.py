import math
from ursina import Entity, color, destroy, distance, time, raycast

class EnemyBase(Entity):
    def __init__(self, health=30, **kwargs):
        super().__init__(
            collider='box',
            **kwargs
        )
        self.sprite = Entity(
            parent=self,
            model='quad',
            billboard=True,
            color=color.red
        )
        self.max_health = health
        self.health = health
        self.state = 'idle'
        self.speed = 2
        self.attack_range = 3
        self.sight_range = 15
        self.target = None 
        self.attack_damage = 10
        self.attack_speed = 1.5
        self.attack_cooldown = 0

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self} took {amount} damange, health now {self.health}")
        if self.health <= 0:
            self.die()

    def die(self):
        print(f"{self} died")
        destroy(self)

    def update(self):
        if self.target is None or self.health <= 0:
            return

        dist_to_target = distance(self.position, self.target.position)

        if self.state == 'idle':
            if dist_to_target <= self.sight_range:
                self.state = 'chase'

        elif self.state == 'chase':
            if dist_to_target <= self.attack_range:
                self.state = 'attack'
            else:   
                self.look_at_2d(self.target.position)
                move_direction = self.forward
                move_distance = time.dt * self.speed

                hit_info = raycast(
                    origin=self.position + (0, 0.5, 0),
                    direction=move_direction,
                    distance=move_distance + 0.5,
                    ignore=[self, self.sprite]
                )

                if not hit_info.hit:
                    self.position += move_direction * move_distance

        elif self.state == 'attack':
            if dist_to_target > self.attack_range:
                self.state = 'chase'
            else:
                self.attack_cooldown -= time.dt
                if self.attack_cooldown <= 0:
                    self.perform_attack()
                    self.attack_cooldown = self.attack_speed

    def look_at_2d(self, target_position):
        direction = target_position - self.position
        angle = math.degrees(math.atan2(direction.x, direction.z))
        self.rotation_y = angle

    def perform_attack(self):
        if hasattr(self.target, 'take_damage'):
            self.target.take_damage(self.attack_damage)
