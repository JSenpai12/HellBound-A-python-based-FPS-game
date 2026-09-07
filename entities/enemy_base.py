import math
import random
from ursina import Entity, color, destroy, distance, time, raycast, Vec3


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
            color=color.red,
        )
        self.max_health = health
        self.health = health
        self.state = 'roam'
        self.speed = 2
        self.attack_range = 3
        self.sight_range = 15
        self.target = None

        self.attack_damage = 10
        self.attack_speed = 1.5
        self.attack_cooldown = 0

        self.roam_center = self.position
        self.roam_radius = 8
        self.roam_target = None
        self.roam_wait_time = 0

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self} took {amount} damage, health now {self.health}")
        if self.health <= 0:
            self.die()

    def die(self):
        print(f"{self} died")
        destroy(self)

    def update(self):
        if self.health <= 0:
            return

        dist_to_target = None
        if self.target:
            dist_to_target = distance(self.position, self.target.position)

        if self.state == 'roam':
            if dist_to_target is not None and dist_to_target <= self.sight_range:
                self.state = 'chase'
            else:
                self.do_roam()

        elif self.state == 'chase':
            if dist_to_target is None:
                self.state = 'roam'
            elif dist_to_target <= self.attack_range:
                self.state = 'attack'
            else:
                self.move_toward(self.target.position)

        elif self.state == 'attack':
            if dist_to_target is None or dist_to_target > self.attack_range:
                self.state = 'chase'
            else:
                self.attack_cooldown -= time.dt
                if self.attack_cooldown <= 0:
                    self.perform_attack()
                    self.attack_cooldown = self.attack_speed

    def perform_attack(self):
        if hasattr(self.target, 'take_damage'):
            self.target.take_damage(self.attack_damage)

    def move_toward(self, target_position):
        self.look_at_2d(target_position)
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

    def do_roam(self):
        if self.roam_target is None:
            if self.roam_wait_time > 0:
                self.roam_wait_time -= time.dt
                return
            self.pick_new_roam_target()
        else:
            dist_to_roam = distance(self.position, self.roam_target)
            if dist_to_roam < 0.5:
                self.roam_target = None
                self.roam_wait_time = random.uniform(1, 3)
            else:
                before_pos = self.position
                self.move_toward(self.roam_target)
                if self.position == before_pos:
                    self.roam_target = None
                    self.roam_wait_time = random.uniform(0.5, 1)

    def pick_new_roam_target(self):
        angle = random.uniform(0, 360)
        rad = math.radians(angle)
        offset_x = math.cos(rad) * self.roam_radius
        offset_z = math.sin(rad) * self.roam_radius
        self.roam_target = self.roam_center + Vec3(offset_x, 0, offset_z)

    def look_at_2d(self, target_position):
        direction = target_position - self.position
        angle = math.degrees(math.atan2(direction.x, direction.z))
        self.rotation_y = angle
