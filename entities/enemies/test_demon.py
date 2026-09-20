from pathlib import Path
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Point Ursina at the project root so 'assets/textures/...' resolves
application.asset_folder = Path(__file__).resolve().parents[2]

from entities.enemies.demon import Demon

# Flat ground to stand and walk on
Entity(
    model='plane',
    scale=60,
    texture='white_cube',
    texture_scale=(60, 60),
    collider='box',
)

player = FirstPersonController(position=(0, 1, -10))
demon = Demon(position=(0, 2, 10))

# Quick texture check: prints any frame that failed to load
for pose, frames in demon.walk_rotation_frames.items():
    for n, tex in frames.items():
        if tex is None:
            print(f"MISSING walk frame {pose}{n}")
for i, tex in enumerate(demon.die_frames):
    if tex is None:
        print(f"MISSING die frame {i}")


def input(key):
    if key == 'escape':
        application.quit()
    # Add a debug key for your death method once you know its name, e.g.:
    if key == 'k':
        demon.die()


app.run()
