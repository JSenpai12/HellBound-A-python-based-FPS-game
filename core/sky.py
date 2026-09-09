# core/sky.py
from ursina import Sky, load_texture


class GameSky(Sky):
    """Loads a custom sky texture instead of Ursina's default procedural sky."""
    def __init__(self, texture_name='SKY1.png'):
        texture = load_texture(f'assets/textures/sky/{texture_name}')
        super().__init__(texture=texture)
