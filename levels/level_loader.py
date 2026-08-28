import json
from ursina import Entity, color


def load_level(path):
    # Load the JSON level
    with open(path) as f:
        data = json.load(f)

    # Get level information
    grid = data['grid']
    cell_size = data.get('cell_size', 4)
    entities = []

    width = len(grid[0])
    depth = len(grid)

    # Floor spans the whole grid
    floor = Entity(
        model='plane',
        scale=(width * cell_size, 1, depth * cell_size),
        position=(width * cell_size / 2, 0, depth * cell_size / 2),
        color=color.gray,
        texture='white_cube',
        texture_scale=(width, depth),
        collider='box'
    )
    entities.append(floor)

    # Walls per grid cell
    for z, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '1':
                wall = Entity(
                    model='cube',
                    scale=(cell_size, 4, cell_size),
                    position=(x * cell_size, 2, z * cell_size),
                    color=color.white,
                    collider='box'
                )
                entities.append(wall)

    # Convert player start from grid coordinates
    # to actual Ursina world coordinates
    start_x, start_z = data['player_start']
    player_start_pos = (
        start_x * cell_size,
        1,
        start_z * cell_size
    )

    return entities, player_start_pos
