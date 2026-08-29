from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from levels.level_loader import load_level
from entities.weapons.pistol import Pistol
from entities.enemies.imp import Imp
from entities.player import Player
from ui.hud import HUD

app = Ursina()


entities, start_pos = load_level('levels/level_data/e1m1.json')


# Player
player = Player()
player.position = start_pos
player.gravity = 0.5

weapon = Pistol()
enemy = Imp(position=(24, 1, 16))
enemy.target = player
hud = HUD(player, weapon)

def input(key):
    if key == 'left mouse down':
        weapon.fire()

app.run()
