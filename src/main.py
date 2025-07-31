# type: ignore

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

            for y in range(surface_y - 1, -16, -1):
                if y >= surface_y - 3:
                    tex = texture_map[textures[4]]
                else:
                    tex = texture_map[textures[2]]

                Entity(
                    model="cube",
                    texture=tex,
                    position=(x, y, z),
                    parent=ground_parent,
                    origin_y=0.5,
                    collider=None,
                )

    ground_parent.combine()


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
    global selected_texture
    if key.isdigit():
        index = int(key) - 1
        if 0 <= index < len(textures):
            selected_texture = textures[index]
            texture_display.texture = load_texture(f"textures/{selected_texture}")
            highlight_border.position = texture_options_ui[index][0].position


def input(key):
    if key == "escape":
        application.quit()
        return

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


DirectionalLight().look_at(Vec3(1, -1, -1))
generate_terrain()
Sky(texture="sky.png")
app.run()
