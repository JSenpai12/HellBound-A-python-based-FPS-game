from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from levels.level_loader import load_level
from entities.weapons.pistol import Pistol

app = Ursina()


entities, start_pos = load_level('levels/level_data/e1m1.json')


# Player
player = FirstPersonController()
player.position = start_pos
player.gravity = 0.5

weapon = Pistol()

def input(key):
    if key == 'left mouse down':
        weapon.fire()

app.run()
