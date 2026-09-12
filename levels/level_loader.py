import json, random
from ursina import Entity
from core.sky import GameSky


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

    # Sky (optional per-level texture, falls back to a default)
    sky_texture = data.get('sky', 'SKY1.png')
    sky = GameSky(sky_texture)
    entities.append(sky)

    # Floor spans the whole grid
    floor = Entity(
        model='plane',
        scale=(width * cell_size, 1, depth * cell_size),
        position=(width * cell_size / 2, 0, depth * cell_size / 2),
        texture='assets/textures/floors/FLOOR4_8.png',
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
                    texture='assets/textures/walls/WALL40_1.png',
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



def get_random_open_positions(path, count, min_distance_from_start=6):
    with open(path) as f:
        data = json.load(f)

    grid = data['grid']
    cell_size = data.get('cell_size', 4)
    start_x, start_z = data['player_start']

    open_cells = []
    for z, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '0':
                dist = abs(x - start_x) + abs(z - start_z)
                if dist >= min_distance_from_start:
                    open_cells.append((x, z))

    chosen = random.sample(open_cells, min(count, len(open_cells)))
    return [(x * cell_size, 1, z * cell_size) for x, z in chosen]
