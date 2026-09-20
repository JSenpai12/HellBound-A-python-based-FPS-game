# check_demon_textures.py
from ursina import *

app = Ursina()

from entities.demon import Demon
d = Demon()

for pose, frames in d.walk_rotation_frames.items():
    for n, tex in frames.items():
        if tex is None:
            print(f"MISSING walk {pose}{n}")
for i, tex in enumerate(d.die_frames):
    if tex is None:
        print(f"MISSING die frame {i}")

print("texture check done")
