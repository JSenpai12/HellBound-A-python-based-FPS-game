from ursina import *
from levels.level_loader import load_level, get_random_open_positions
from entities.weapons.pistol import Pistol
from entities.enemies.imp import Imp
from entities.player import Player
from ui.hud import HUD
from levels.levels_objects import ExitTrigger
from ui.main_menu import MainMenu
import random
from entities.pickups.ammo import AmmoPickup
from entities.pickups.health import HealthPickup

app = Ursina()

LEVELS = [
    {
        'path': 'levels/level_data/e1m1.json',
        'exit_position': (120, 1, 44),
        'mode': 'exit',
        'enemy_count': 15,
    },
    {
        'path': 'levels/level_data/e1m2.json',
        'exit_position': (144, 1, 56),
        'mode': 'exit',
        'enemy_count': 30,
    },
    {
        'path': 'levels/level_data/e1m3.json',
        'exit_position': (32, 1, 28),
        'mode': 'exit',
        'enemy_count': 0,
    },
    {
        'path': 'levels/level_data/e1m4.json',
        'exit_position': (28, 1, 44),
        'mode': 'exit',
        'enemy_count': 0,
    },
    {
        'path': 'levels/level_data/e1m5.json',
        'exit_position': (144, 1, 60),
        'mode': 'exit',
        'enemy_count': 0,
    },
    {
        'path': 'levels/level_data/e1m52.json',
        'mode': 'exit',
        'exit_position': None,
        'enemy_count': 0,
    },
]

current_level_entities = []
exit_trigger = None
current_enemies = []
player = None
weapon = None
hud = None
active_pickups = []
AMMO_DROP_CHANCE = 0.35
HEALTH_DROP_CHANCE = 0.20

current_level_index = 0


def load_current_level():
    global current_level_entities, exit_trigger, active_pickups

    level = LEVELS[current_level_index]
    is_last = current_level_index == len(LEVELS) - 1

    for e in current_level_entities:
        destroy(e)
    for p in active_pickups:
        destroy(p)
    active_pickups = []
    if exit_trigger:
        destroy(exit_trigger)
        exit_trigger = None

    entities, start_pos = load_level(level['path'])
    current_level_entities = entities
    player.position = start_pos

    if not is_last and level.get('exit_position'):
        exit_trigger = ExitTrigger(
            on_trigger=lambda: complete_stage(),
            player=player,
            position=level['exit_position']
        )

    if level['enemy_count'] > 0:
        spawn_enemies(get_random_open_positions(level['path'], count=level['enemy_count']))
    else:
        spawn_enemies([])


def spawn_enemies(positions):
    global current_enemies
    for e in current_enemies:
        destroy(e)
    current_enemies = []
    for pos in positions:
        enemy = Imp(position=pos)
        enemy.target = player
        enemy.on_death = handle_enemy_death
        current_enemies.append(enemy)


def handle_enemy_death(position):
    global active_pickups

    roll = random.random()
    if roll < AMMO_DROP_CHANCE:
        pickup = AmmoPickup(position=position, amount=12, weapon=weapon)
        pickup.set_player(player)
        active_pickups.append(pickup)
    elif roll < AMMO_DROP_CHANCE + HEALTH_DROP_CHANCE:
        pickup = HealthPickup(position=position, amount=25, player=player)
        pickup.set_player(player)
        active_pickups.append(pickup)


def complete_stage():
    is_last = current_level_index == len(LEVELS) - 1
    player.stage_cleared = True
    player.has_next_level = not is_last
    player.enabled = False


def advance_to_next_stage():
    global current_level_index

    player.stage_cleared = False
    player.has_next_level = False
    player.enabled = True

    current_level_index += 1
    load_current_level()


def restart_game():
    global current_level_index

    current_level_index = 0
    player.health = player.max_health
    player.won = False
    player.stage_cleared = False
    player.has_next_level = False
    player.enabled = True
    load_current_level()

def jump_to_level(index):
    global current_level_index

    if index < 0 or index >= len(LEVELS):
        print(f"No level at index {index + 1} (valid range: 1-{len(LEVELS)})")
        return

    current_level_index = index
    player.health = player.max_health
    player.stage_cleared = False
    player.has_next_level = False
    player.enabled = True
    load_current_level()
    print(f"Jumped to level {index + 1}: {LEVELS[index]['path']}")

def teleport_to_exit():
    level = LEVELS[current_level_index]
    exit_pos = level.get('exit_position')

    if exit_pos is None:
        print(f"Level {current_level_index + 1} has no exit position set")
        return

    offset_distance = 6
    ex, ey, ez = exit_pos
    player.position = (ex - offset_distance, ey, ez)
    print(f"Teleported near exit at {player.position} (exit itself at {exit_pos})")


def return_to_menu():
    global current_level_entities, exit_trigger, current_enemies, active_pickups
    global player, weapon, hud

    for e in current_level_entities:
        destroy(e)
    current_level_entities = []

    for e in current_enemies:
        destroy(e)
    current_enemies = []

    for p in active_pickups:
        destroy(p)
    active_pickups = []

    if exit_trigger:
        destroy(exit_trigger)
        exit_trigger = None

    if hud:
        destroy(hud)
        hud = None

    if weapon:
        destroy(weapon)
        weapon = None

    if player:
        destroy(player)
        player = None

    mouse.locked = False
    menu.enabled = True


def start_game():
    global player, weapon, hud, current_level_index

    current_level_index = 0
    player = Player()
    player.gravity = 0.5
    weapon = Pistol(player=player)
    hud = HUD(player, weapon)

    load_current_level()

    mouse.locked = True


menu = MainMenu(on_start=start_game)
mouse.locked = False


def input(key):
    if weapon is None:
        return
    if key == 'left mouse down':
        if player.health > 0 and not player.stage_cleared:
            weapon.fire()
    if key == 'r':
        if player.health <= 0:
            weapon.ammo = 15
            restart_game()
    if key == 'space':
        if player.stage_cleared:
            if player.has_next_level:
                advance_to_next_stage()
            else:
                return_to_menu()
    if key == 'shift':
        player.start_sprint()
    if key == 'shift up':
        player.stop_sprint()

    if key.isdigit():
        jump_to_level(int(key) - 1)

    if key == 'e':
        teleport_to_exit()


app.run()
