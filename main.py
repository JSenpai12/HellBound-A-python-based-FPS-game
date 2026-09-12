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
            on_trigger=lambda: win_game(),
            player=player,
            position=exit_position
        )
    elif exit_position and next_level_path:
        exit_trigger = ExitTrigger(
            on_trigger=lambda: (
                load_new_level(next_level_path, exit_position=(144, 1, 56), is_final=True),
                spawn_enemies(get_random_open_positions('levels/level_data/e1m2.json', count=25))
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


def win_game():
    player.won = True
    player.enabled = False


def restart_game():
    player.health = player.max_health
    player.won = False
    player.enabled = True
    load_new_level(
        'levels/level_data/e1m1.json',
        exit_position=(120, 1, 44),
        next_level_path='levels/level_data/e1m2.json'
    )
    spawn_enemies(get_random_open_positions('levels/level_data/e1m1.json', count=15))


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
        weapon.fire()
    if key == 'r':
        if player.health <= 0 or player.won:
            weapon.ammo = 15
            restart_game()
    if key == 'shift':
        player.start_sprint()
    if key == 'shift up':
        player.stop_sprint()



app.run()
