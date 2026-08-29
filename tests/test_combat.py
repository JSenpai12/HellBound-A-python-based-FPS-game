from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Ground
Entity(
    model='plane',
    scale=30,
    texture='white_cube',
    collider='box'
)

# 1-unit cube
Entity(
    model='cube',
    scale=1,
    position=(2, 0.5, 5),
    color=color.red
)

# 2-unit cube
Entity(
    model='cube',
    scale=2,
    position=(5, 1, 5),
    color=color.green
)

# 4-unit cube
Entity(
    model='cube',
    scale=4,
    position=(10, 2, 5),
    color=color.blue
)

# Player
player = FirstPersonController()
player.position = (0, 1, 0)

app.run()
