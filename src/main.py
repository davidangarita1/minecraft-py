# type: ignore

import time

from perlin_noise import PerlinNoise
from ursina import (
    Button,
    DirectionalLight,
    Entity,
    Sky,
    Text,
    Ursina,
    Vec3,
    application,
    camera,
    color,
    destroy,
    load_texture,
    mouse,
    scene,
    held_keys,
)
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title="Minecraft-py")

# Terrain config
noise = PerlinNoise(octaves=4, seed=2025)
terrain_width = 20
terrain_depth = 20
height_scale = 8
textures = ["grass.png", "glass.png", "stone.png", "iron_stone.png", "earth_bottom.png"]
texture_map = {name: load_texture(f"textures/{name}") for name in textures}
selected_texture = textures[0]
boxes = []
creative_mode = False
last_space_press = 0


def generate_terrain():
    ground_parent = Entity()

    for z in range(terrain_depth):
        for x in range(terrain_width):
            surface_y = round(
                noise([x / terrain_width, z / terrain_depth]) * height_scale
            )

            top_block = Button(
                model="cube",
                texture=texture_map[textures[0]],
                color=color.white,
                position=(x, surface_y, z),
                parent=scene,
                origin_y=0.5,
            )
            boxes.append(top_block)

            for y in range(surface_y - 1, -11, -1):
                if y >= surface_y - 3:
                    tex = texture_map[textures[4]]
                else:
                    tex = texture_map[textures[2]]

                boxes.append(
                    Button(
                        model="cube",
                        texture=tex,
                        color=color.white,
                        position=(x, y, z),
                        parent=ground_parent,
                        origin_y=0.5,
                    )
                )


texture_display = Entity(
    parent=camera.ui,
    model="quad",
    texture=load_texture(f"textures/{selected_texture}"),
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

# Texture Options
texture_options_ui = []
spacing = 0.13
start_x = -((len(textures) - 1) * spacing) / 2
for i, texture_name in enumerate(textures):
    x = start_x + i * spacing
    icon = Entity(
        parent=camera.ui,
        model="quad",
        texture=load_texture(f"textures/{texture_name}"),
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


def handle_texture_selection(key):
    if key.isdigit():
        index = int(key) - 1
        if 0 <= index < len(textures):
            selected_texture = textures[index]
            texture_display.texture = load_texture(f"textures/{selected_texture}")
            highlight_border.position = texture_options_ui[index][0].position


def input(key):
    global selected_texture, creative_mode, last_space_press

    if key == "escape":
        application.quit()
        return

    if key == "space":
        now = time.time()
        if now - last_space_press < 0.3:
            creative_mode = not creative_mode
            if creative_mode:
                player.gravity = 0
                player.jump_height = 0
                player.flying_speed = 10
            else:
                player.gravity = 1
                player.jump_height = 2
            last_space_press = 0
        else:
            last_space_press = now

    handle_texture_selection(key)

    for box in boxes:
        if box.hovered:
            if key == "left mouse down":
                new_cube = Button(
                    color=color.white,
                    model="cube",
                    position=box.position + mouse.normal,
                    texture=load_texture(f"textures/{selected_texture}"),
                    parent=scene,
                    origin_y=0.5,
                )
                boxes.append(new_cube)

            if key == "right mouse down":
                boxes.remove(box)
                destroy(box)


player = FirstPersonController()
initial_position = (terrain_width // 2, height_scale + 5, terrain_depth // 2)
player.position = initial_position


def update():
    if player.y < -30:
        player.position = initial_position
        player.velocity = Vec3(0, 0, 0)

    if creative_mode:
        speed = player.flying_speed * time.dt
        direction = Vec3(
            int(held_keys["d"]) - int(held_keys["a"]),
            int(held_keys["space"]) - int(held_keys["shift"]),
            int(held_keys["w"]) - int(held_keys["s"]),
        )
        player.position += camera.forward * direction.z * speed
        player.position += camera.right * direction.x * speed
        player.position += Vec3(0, 1, 0) * direction.y * speed


DirectionalLight().look_at(Vec3(1, -1, -1))
generate_terrain()
Sky(texture="sky.png")
app.run()
