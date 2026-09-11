from ursina import *
from levels.level_loader import load_level
from entities.weapons.pistol import Pistol
from entities.enemies.imp import Imp
from entities.player import Player
from ui.hud import HUD
from levels.levels_objects import ExitTrigger
from ui.main_menu import MainMenu

app = Ursina()

current_level_entities = []
exit_trigger = None
current_enemies = []
player = None
weapon = None
hud = None

E1M1_ENEMIES = [
    (24, 1, 8),
    (56, 1, 28),
    (4, 1, 44),
]
E1M2_ENEMIES = [
    (12, 1, 20),
    (84, 1, 8),
    (136, 1, 4),
    (144, 1, 24),
    (4, 1, 48),
    (92, 1, 48),
]


def load_new_level(path, exit_position=None, next_level_path=None, is_final=False):
    global current_level_entities, exit_trigger
    for e in current_level_entities:
        destroy(e)
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
                spawn_enemies(E1M2_ENEMIES)
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
        current_enemies.append(enemy)


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
    spawn_enemies(E1M1_ENEMIES)


def start_game():
    global player, weapon, hud

    player = Player()
    player.gravity = 0.5
    weapon = Pistol()
    hud = HUD(player, weapon)

    load_new_level(
        'levels/level_data/e1m1.json',
        exit_position=(120, 1, 44),
        next_level_path='levels/level_data/e1m2.json'
    )
    spawn_enemies(E1M1_ENEMIES)

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
            restart_game()
    if key == 'shift':
        player.start_sprint()
    if key == 'shift up':
        player.stop_sprint()


app.run()
