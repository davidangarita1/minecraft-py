# type: ignore

from ursina import Entity, load_texture

block_textures = {
    "grass":      load_texture("assets/textures/groundEarth.png"),
    "dirt":       load_texture("assets/textures/groundMud.png"),
    "stone":      load_texture("assets/textures/wallStone.png"),
    "bedrock":    load_texture("assets/textures/stone07.png"),
    "snow":       load_texture("assets/textures/groundSnow.png"),
    "ice":        load_texture("assets/textures/ice01.png"),
    "lava":       load_texture("assets/textures/lava01.png"),
    "brick":      load_texture("assets/textures/wallBrick01.png"),
    "gravel":     load_texture("assets/textures/stone04.png"),
    "cobblestone":load_texture("assets/textures/Stone01.png"),
}


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
        self.block_type = block_type
