import random

from ursina import *

from entities.enemies.demon import Demon
from entities.enemies.imp import Imp
from entities.pickups.ammo import AmmoPickup
from entities.pickups.health import HealthPickup
from entities.player import Player
from entities.weapons.pistol import Pistol
from entities.weapons.shotgun import Shotgun
from levels.level_loader import get_random_open_positions, load_level
from levels.levels_objects import ExitTrigger
from ui.hud import HUD
from ui.main_menu import MainMenu
from entities.enemies.mini_boss import MiniBoss
from ui.minimap import Minimap

app = Ursina()

LEVELS = [
    {
        "path": "levels/level_data/e1m1.json",
        "exit_position": (120, 1, 44),
        "mode": "exit",
        "enemy_count": 15,
    },
    {
        "path": "levels/level_data/e1m2.json",
        "exit_position": (144, 1, 56),
        "mode": "exit",
        "enemy_count": 30,
    },
    {
        "path": "levels/level_data/e1m3.json",
        "exit_position": (32, 1, 28),
        "mode": "exit",
        "enemy_count": 30,
        "enemy_classes": [Imp, Demon],
    },
    {
        "path": "levels/level_data/e1m4.json",
        "exit_position": (28, 1, 44),
        "mode": "exit",
        "enemy_count": 40,
        "enemy_classes": [Imp, Demon],
        "reward_weapon": Shotgun,
    },
    {
        "path": "levels/level_data/e1m5.json",
        "exit_position": (144, 1, 60),
        "mode": "exit",
        "enemy_count": 1,
        "enemy_classes": [MiniBoss],
    },
    {
        "path": "levels/level_data/e1m52.json",
        "mode": "exit",
        "exit_position": None,
        "enemy_count": 0,
    },
]

current_level_entities = []
exit_trigger = None
current_enemies = []
player = None
weapon = None
owned_weapons = []
hud = None
minimap = None
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

    entities, start_pos = load_level(level["path"])
    current_level_entities = entities
    player.position = start_pos

    if minimap:
        minimap.load(level["path"], level.get("exit_position"))

    if not is_last and level.get("exit_position"):
        exit_trigger = ExitTrigger(
            on_trigger=lambda: complete_stage(),
            player=player,
            position=level["exit_position"],
        )

    if level["enemy_count"] > 0:
        enemy_classes = level.get("enemy_classes", [Imp])
        spawn_enemies(
            get_random_open_positions(level["path"], count=level["enemy_count"]),
            enemy_classes=enemy_classes,
        )
    else:
        spawn_enemies([])


def spawn_enemies(positions, enemy_classes=None):
    global current_enemies

    if enemy_classes is None:
        enemy_classes = [Imp]

    for e in current_enemies:
        destroy(e)
    current_enemies = []

    for pos in positions:
        enemy_class = random.choice(enemy_classes)
        enemy = enemy_class(position=pos)
        enemy.target = player
        enemy.on_death = handle_enemy_death
        current_enemies.append(enemy)


def handle_enemy_death(position):

    roll = random.random()

    if roll < AMMO_DROP_CHANCE:
        target_weapon = random.choice(owned_weapons)
        pickup = AmmoPickup(
            position=position,
            amount=getattr(target_weapon, "pickup_ammo", 12),
            weapon=target_weapon,
        )
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

    reward = LEVELS[current_level_index].get("reward_weapon")
    if reward and give_weapon(reward):
        hud.notice = f"NEW WEAPON: {type(weapon).__name__.upper()}"


def advance_to_next_stage():
    global current_level_index

    reset_weapons()
    hud.notice = ""

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

def equip_weapon(index):
    global weapon
    if index < 0 or index >= len(owned_weapons):
        return
    if owned_weapons[index] is weapon:
        return
    weapon.unequip()
    weapon = owned_weapons[index]
    weapon.equip()
    hud.weapon = weapon


def give_weapon(weapon_class):
    if any(isinstance(w, weapon_class) for w in owned_weapons):
        return False
    owned_weapons.append(weapon_class(player=player))
    equip_weapon(len(owned_weapons) - 1)
    return True


def cycle_weapon(step):
    if len(owned_weapons) < 2:
        return
    if player.health <= 0 or player.stage_cleared:
        return
    equip_weapon((owned_weapons.index(weapon) + step) % len(owned_weapons))


def reset_weapons():
    global weapon, owned_weapons
    pistol = owned_weapons[0]
    for w in owned_weapons[1:]:
        destroy(w)
    owned_weapons = [pistol]
    pistol.ammo = pistol.max_ammo
    pistol.equip()
    weapon = pistol
    hud.weapon = pistol


def grant_rewards_before(index):
    # Used by the number-key level jump, so jumping to e1m5 still gives you the shotgun
    for level in LEVELS[:index]:
        reward = level.get("reward_weapon")
        if reward:
            give_weapon(reward)


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
    hud.notice = ""
    grant_rewards_before(index)
    load_current_level()
    print(f"Jumped to level {index + 1}: {LEVELS[index]['path']}")


def teleport_to_exit():
    level = LEVELS[current_level_index]
    exit_pos = level.get("exit_position")

    if exit_pos is None:
        print(f"Level {current_level_index + 1} has no exit position set")
        return

    offset_distance = 6
    ex, ey, ez = exit_pos
    player.position = (ex - offset_distance, ey, ez)
    print(f"Teleported near exit at {player.position} (exit itself at {exit_pos})")


def return_to_menu():
    global current_level_entities, exit_trigger, current_enemies, active_pickups, player, weapon, hud, minimap, owned_weapons


    for e in current_level_entities:
        destroy(e)
    current_level_entities = []

    for e in current_enemies:
        destroy(e)
    current_enemies = []

    for p in active_pickups:
        destroy(p)
    active_pickups = []

    for w in owned_weapons:
        destroy(w)
    owned_weapons = []
    weapon = None

    if exit_trigger:
        destroy(exit_trigger)
        exit_trigger = None

    if hud:
        destroy(hud)
        hud = None

    if minimap:
        destroy(minimap)
        minimap = None

    if player:
        destroy(player)
        player = None

    mouse.locked = False
    menu.enabled = True


def start_game():
    global player, weapon, hud, owned_weapons, minimap, current_level_index

    current_level_index = 0
    player = Player()
    player.gravity = 0.5
    weapon = Pistol(player=player)
    owned_weapons = [weapon]
    hud = HUD(player, weapon)
    minimap = Minimap(player, get_enemies=lambda: current_enemies)

    load_current_level()

    mouse.locked = True


menu = MainMenu(on_start=start_game)
mouse.locked = False


def input(key):
    if weapon is None:
        return
    if key == "left mouse down":
        if player.health > 0 and not player.stage_cleared:
            weapon.fire()
    if key == "r":
        if player.health <= 0:
            weapon.ammo = 15
            restart_game()
    if key == "q" or key == "scroll up":
        cycle_weapon(1)
    if key == "scroll down":
        cycle_weapon(-1)
    if key == "space":
        if player.stage_cleared:
            if player.has_next_level:
                advance_to_next_stage()
            else:
                return_to_menu()
    if key == "shift":
        player.start_sprint()
    if key == "shift up":
        player.stop_sprint()

    if key.isdigit():
        jump_to_level(int(key) - 1)

    if key == "e":
        teleport_to_exit()


app.run()
