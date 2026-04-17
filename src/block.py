# type: ignore

from ursina import Entity, load_texture

TEXTURE_PATHS = {
    "grass": "assets/textures/groundEarth.png",
    "dirt": "assets/textures/groundMud.png",
    "stone": "assets/textures/wallStone.png",
    "bedrock": "assets/textures/stone07.png",
    "snow": "assets/textures/groundSnow.png",
    "ice": "assets/textures/ice01.png",
    "lava": "assets/textures/lava01.png",
    "brick": "assets/textures/wallBrick01.png",
    "gravel": "assets/textures/stone04.png",
    "cobblestone": "assets/textures/Stone01.png",
}

block_textures = {}


def load_block_textures():
    for name, path in TEXTURE_PATHS.items():
        block_textures[name] = load_texture(path)


class Block(Entity):
    def __init__(self, position, block_type, parent):
        super().__init__(
            model="assets/models/block_model",
            texture=block_textures.get(block_type),
            position=position,
            parent=parent,
            origin_y=0.5,
            collider="box",
        )
        self.block_type = block_type
