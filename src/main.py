# type: ignore

import random
import time

from perlin_noise import PerlinNoise
from ursina import (
    DirectionalLight,
    Entity,
    Sky,
    Text,
    Ursina,
    Vec3,
    camera,
    color,
    destroy,
    held_keys,
    load_texture,
    mouse,
    scene,
)
from ursina.prefabs.first_person_controller import FirstPersonController

from block import Block
from chunk import NEIGHBORS
from pause_menu import PauseMenu

app = Ursina(title="Minecraft-py")
mouse.update_step = 4

TERRAIN_WIDTH = 30
TERRAIN_DEPTH = 30
HEIGHT_SCALE = 8
MIN_HEIGHT = -10

textures = ["grass", "stone"]
selected_texture = textures[0]
creative_mode = False
last_space_press = 0
world_blocks = {}
block_entities = {}


def build_world_data():
    noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000))

    for z in range(TERRAIN_DEPTH):
        for x in range(TERRAIN_WIDTH):
            surface_y = round(
                noise([x / TERRAIN_WIDTH, z / TERRAIN_DEPTH]) * HEIGHT_SCALE
            )
            world_blocks[(x, surface_y, z)] = "grass"
            for y in range(surface_y - 1, MIN_HEIGHT, -1):
                if y == MIN_HEIGHT + 1:
                    world_blocks[(x, y, z)] = "bedrock"
                else:
                    world_blocks[(x, y, z)] = "dirt" if y >= surface_y - 3 else "stone"


def create_visible_blocks():
    for (x, y, z), block_type in world_blocks.items():
        if is_exposed(x, y, z):
            block = Block((x, y, z), block_type, scene)
            block_entities[(x, y, z)] = block


def is_exposed(x, y, z):
    for dx, dy, dz in NEIGHBORS:
        if (x + dx, y + dy, z + dz) not in world_blocks:
            return True
    return False


def expose_neighbors(x, y, z):
    for dx, dy, dz in NEIGHBORS:
        nx, ny, nz = x + dx, y + dy, z + dz
        if (nx, ny, nz) in world_blocks and (nx, ny, nz) not in block_entities:
            if is_exposed(nx, ny, nz):
                block = Block((nx, ny, nz), world_blocks[(nx, ny, nz)], scene)
                block_entities[(nx, ny, nz)] = block


def generate_terrain():
    build_world_data()
    create_visible_blocks()


player = FirstPersonController()
initial_position = (TERRAIN_WIDTH // 2, HEIGHT_SCALE + 5, TERRAIN_DEPTH // 2)
player.position = initial_position

pause_menu = PauseMenu()

texture_display = Entity(
    parent=camera.ui,
    model="quad",
    texture=load_texture(f"textures/{selected_texture}.png"),
    scale=(0.1, 0.1),
    position=(-0.83, 0.44),
)

highlight_border = Entity(
    parent=camera.ui,
    model="quad",
    color=color.white33,
    scale=(0.09, 0.09),
    position=(0, -0.45),
    enabled=True,
    z=-0.5,
)

texture_options_ui = []
spacing = 0.13
start_x = -((len(textures) - 1) * spacing) / 2
for i, texture_name in enumerate(textures):
    x = start_x + i * spacing
    icon = Entity(
        parent=camera.ui,
        model="quad",
        texture=load_texture(f"textures/{texture_name}.png"),
        scale=(0.08, 0.08),
        position=(x, -0.45),
    )
    number_label = Text(
        text=str(i + 1),
        parent=camera.ui,
        origin=(0, 0),
        position=(x, -0.53),
        scale=1.5,
        color=color.white,
    )
    texture_options_ui.append((icon, number_label))

highlight_border.position = texture_options_ui[0][0].position


def input(key):
    global selected_texture, creative_mode, last_space_press

    if key == 'space':
        now = time.time()
        if now - last_space_press < 0.3:
            creative_mode = not creative_mode
            if creative_mode:
                player.gravity = 0
                player.jump_height = 0
            else:
                player.gravity = 1
                player.jump_height = 2
            last_space_press = 0
        else:
            last_space_press = now

    if key.isdigit():
        index = int(key) - 1
        if 0 <= index < len(textures):
            selected_texture = textures[index]
            texture_display.texture = selected_texture
            highlight_border.position = texture_options_ui[index][0].position

    hovered = mouse.hovered_entity
    if hovered and isinstance(hovered, Block):
        if key == 'left mouse down':
            new_pos = hovered.position + mouse.normal
            pos_key = (int(new_pos.x), int(new_pos.y), int(new_pos.z))
            if pos_key not in world_blocks:
                world_blocks[pos_key] = selected_texture
                block = Block(new_pos, selected_texture, scene)
                block_entities[pos_key] = block

        if key == 'right mouse down':
            if hovered.block_type != 'bedrock':
                pos = hovered.position
                pos_key = (int(pos.x), int(pos.y), int(pos.z))
                world_blocks.pop(pos_key, None)
                block_entities.pop(pos_key, None)
                destroy(hovered)
                expose_neighbors(*pos_key)


def update():
    if player.y < -30:
        player.position = initial_position
        player.velocity = Vec3(0, 0, 0)

    if creative_mode:
        speed = 10 * time.dt
        direction = Vec3(
            int(held_keys['d']) - int(held_keys['a']),
            int(held_keys['space']) - int(held_keys['shift']),
            int(held_keys['w']) - int(held_keys['s']),
        )
        player.position += camera.forward * direction.z * speed
        player.position += camera.right * direction.x * speed
        player.position += Vec3(0, 1, 0) * direction.y * speed


DirectionalLight().look_at(Vec3(1, -1, -1))
generate_terrain()
Sky(texture="sky.png")
app.run()
