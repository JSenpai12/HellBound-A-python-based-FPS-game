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

current_level_entities = []
exit_trigger = None
current_enemies = []
player = None
weapon = None
hud = None
active_pickups = []
AMMO_DROP_CHANCE = 0.35
HEALTH_DROP_CHANCE = 0.20
pending_next_level = None
pending_next_exit_position = None
pending_next_is_final = False
pending_enemy_level_path = None
pending_enemy_count = 0


def load_new_level(path, exit_position=None, next_level_path=None, is_final=False):
    global current_level_entities, exit_trigger, active_pickups

    for e in current_level_entities:
        destroy(e)
    for p in active_pickups:
        destroy(p)
    active_pickups = []
    if exit_trigger:
        destroy(exit_trigger)
        exit_trigger = None
    entities, start_pos = load_level(path)
    current_level_entities = entities
    player.position = start_pos

    if exit_position and is_final:
        exit_trigger = ExitTrigger(
            on_trigger=lambda: complete_stage(next_level_path=None),
            player=player,
            position=exit_position
        )
    elif exit_position and next_level_path:
        exit_trigger = ExitTrigger(
            on_trigger=lambda: complete_stage(
                next_level_path=next_level_path,
                next_exit_position=(144, 1, 56),
                next_is_final=True,
                enemy_level_path=next_level_path,
                enemy_count=6
            ),
            player=player,
            position=exit_position
        )


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


def complete_stage(next_level_path=None, next_exit_position=None, next_is_final=False, enemy_level_path=None, enemy_count=0):
    global pending_next_level, pending_next_exit_position, pending_next_is_final
    global pending_enemy_level_path, pending_enemy_count

    player.stage_cleared = True
    player.has_next_level = next_level_path is not None
    player.enabled = False

    pending_next_level = next_level_path
    pending_next_exit_position = next_exit_position
    pending_next_is_final = next_is_final
    pending_enemy_level_path = enemy_level_path
    pending_enemy_count = enemy_count


def advance_to_next_stage():
    player.stage_cleared = False
    player.has_next_level = False
    player.enabled = True

    load_new_level(
        pending_next_level,
        exit_position=pending_next_exit_position,
        is_final=pending_next_is_final
    )
    spawn_enemies(get_random_open_positions(pending_enemy_level_path, count=pending_enemy_count))


def restart_game():
    player.health = player.max_health
    player.won = False
    player.stage_cleared = False
    player.has_next_level = False
    player.enabled = True
    load_new_level(
        'levels/level_data/e1m1.json',
        exit_position=(120, 1, 44),
        next_level_path='levels/level_data/e1m2.json'
    )
    spawn_enemies(get_random_open_positions('levels/level_data/e1m1.json', count=15))


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
    global player, weapon, hud

    player = Player()
    player.gravity = 0.5
    weapon = Pistol(player=player)
    hud = HUD(player, weapon)

    load_new_level(
        'levels/level_data/e1m1.json',
        exit_position=(120, 1, 44),
        next_level_path='levels/level_data/e1m2.json'
    )
    spawn_enemies(get_random_open_positions('levels/level_data/e1m1.json', count=15))

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


app.run()
