# type: ignore

from ursina import Entity, load_texture

block_textures = {
    "grass": load_texture("assets/textures/groundEarth.png"),
    "dirt": load_texture("assets/textures/groundMud.png"),
    "stone": load_texture("assets/textures/wallStone.png"),
    "bedrock": load_texture("assets/textures/stone07.png"),
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
