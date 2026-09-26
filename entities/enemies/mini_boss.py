from ursina import load_texture, distance, time
from entities.enemy_base import EnemyBase
from entities.projectiles import FireballProjectile


class MiniBoss(EnemyBase):
    def __init__(self, position=(0, 1, 0)):
        super().__init__(health=300, position=position, scale=2.2)

        self.speed = 1.5
        self.attack_range = 3.5       # still used to stop movement when close, no longer deals damage
        self.attack_speed = 2.0
        self.sight_range = 30
        self.pain_chance = 0.15

        self.ranged_range = 14
        self.ranged_cooldown = 0
        self.ranged_cooldown_max = 2.5
        self.ranged_damage = 20

        # --- Walk cycle: rotation slots 1-5 only (base class mirrors 6-8 via flip) ---
        self.walk_rotation_frames = {
            "A": {i: load_texture(f"assets/textures/sprites/enemies/miniboss/BOSSA{i}.png") for i in range(1, 6)},
            "B": {i: load_texture(f"assets/textures/sprites/enemies/miniboss/BOSSB{i}.png") for i in range(1, 6)},
        }
        self.walk_pose_order = ["A", "B"]
        self.sprite.texture = self.walk_rotation_frames["A"][1]

        # --- Shoot/fireball-cast animation (C-H, 6 frames, same 1-5 rotation scheme) ---
        self.shoot_rotation_frames = {
            letter: {i: load_texture(f"assets/textures/sprites/enemies/miniboss/BOSS{letter}{i}.png") for i in range(1, 6)}
            for letter in ["C", "D", "E", "F", "G", "H"]
        }
        self.shoot_pose_order = ["C", "D", "E", "F", "G", "H"]

        self.is_shooting = False
        self.shoot_frame_index = 0
        self.shoot_frame_timer = 0
        self.shoot_frame_duration = 0.08
        self.pending_target = None

        self.die_frames = [
            load_texture("assets/textures/sprites/enemies/miniboss/BOSSI0.png"),
            load_texture("assets/textures/sprites/enemies/miniboss/BOSSJ0.png"),
            load_texture("assets/textures/sprites/enemies/miniboss/BOSSK0.png"),
            load_texture("assets/textures/sprites/enemies/miniboss/BOSSL0.png"),
            load_texture("assets/textures/sprites/enemies/miniboss/BOSSM0.png"),
        ]

    def perform_attack(self):
        # Override on purpose: the boss deals damage only through the fireball impact
        # (see FireballProjectile.explode -> target.take_damage), never via base-class melee.
        pass

    def update(self):
        if self.dying or self.health <= 0:
            super().update()
            return

        if self.is_shooting:
            if self.in_pain:
                self.pain_timer += time.dt
                if self.pain_timer >= self.pain_duration:
                    self.in_pain = False

            if self.ranged_cooldown > 0:
                self.ranged_cooldown -= time.dt

            self._step_shoot_animation()
            return

        super().update()

        if self.target is None:
            return

        if self.ranged_cooldown > 0:
            self.ranged_cooldown -= time.dt

        # Fires from ANY state (chase or attack) as long as the target is within ranged_range.
        # This is now the boss's only source of damage.
        if self.state in ("chase", "attack") and self.ranged_cooldown <= 0:
            dist = distance(self.position, self.target.position)
            if dist <= self.ranged_range:
                self.start_ranged_attack()

    def start_ranged_attack(self):
        self.ranged_cooldown = self.ranged_cooldown_max
        self.pending_target = self.target
        self.is_shooting = True
        self.is_moving = False
        self.shoot_frame_index = 0
        self.shoot_frame_timer = 0
        self._set_shoot_frame_texture()

    def _step_shoot_animation(self):
        self.shoot_frame_timer += time.dt
        if self.shoot_frame_timer < self.shoot_frame_duration:
            return

        self.shoot_frame_timer = 0
        self.shoot_frame_index += 1

        if self.shoot_frame_index >= len(self.shoot_pose_order):
            self.is_shooting = False
            self.fire_ranged_attack()
            return

        self._set_shoot_frame_texture()

    def _set_shoot_frame_texture(self):
        pose_letter = self.shoot_pose_order[self.shoot_frame_index]
        rotation_slot, flip = self.get_rotation_slot()
        texture = self.shoot_rotation_frames[pose_letter].get(rotation_slot)
        if texture:
            self.sprite.texture = texture
            self.sprite.texture_scale = (-1, 1) if flip else (1, 1)

    def fire_ranged_attack(self):
        FireballProjectile(
            start_pos=self.position + (0, 1.2, 0),
            target=self.pending_target,
            travel_time=0.6,
            damage=self.ranged_damage,
        )
