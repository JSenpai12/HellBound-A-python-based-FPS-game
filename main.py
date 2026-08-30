from ursina import *
from levels.level_loader import load_level
from entities.weapons.pistol import Pistol
from entities.enemies.imp import Imp
from entities.player import Player
from ui.hud import HUD
from levels.levels_objects import ExitTrigger

app = Ursina()

current_level_entities = []
exit_trigger = None
current_enemy = None

def load_new_level(path, exit_position=None, next_level_path=None):
    global current_level_entities, exit_trigger

    for e in current_level_entities:
        destroy(e)
    if exit_trigger:
        destroy(exit_trigger)
        exit_trigger = None

    entities, start_pos = load_level(path)
    current_level_entities = entities
    player.position = start_pos

    if exit_position and next_level_path:
        exit_trigger = ExitTrigger(
            on_trigger=lambda: load_new_level(next_level_path),
            player=player,
            position=exit_position
        )
        print(f"Exit trigger created at {exit_position}")

def spawn_enemy(position):
    global current_enemy
    if current_enemy:
        destroy(current_enemy)
    current_enemy = Imp(position=position)
    current_enemy.target = player

def restart_game():
    player.health = player.max_health
    player.enabled = True
    load_new_level(
    'levels/level_data/e1m1.json',
    exit_position=(24, 1, 4),
    next_level_path='levels/level_data/e1m2.json'
    )
    spawn_enemy(position=(24, 1, 16))


player = Player()
player.gravity = 0.5
weapon = Pistol()
hud = HUD(player, weapon)

load_new_level(
    'levels/level_data/e1m1.json',
    exit_position=(24, 1, 4),
    next_level_path='levels/level_data/e1m2.json'
)
spawn_enemy(position=(24, 1, 16))

def input(key):
    if key == 'left mouse down':
        weapon.fire()
    if key == 'r'.lower():
        if player.health <= 0:
            restart_game()

app.run()
