from ursina import Ursina, Button, color, Sky, scene, destroy, mouse, application, Entity, camera, Text
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title="Minecraft-py")
player = FirstPersonController()
Sky(texture="sky.png")

boxes = []

def generate_terrain(config):
    for i in range(config["axis"]["y"]):
        for j in range(config["axis"]["x"]):
            box = Button(
                color=color.white,  
                model="cube",
                position=(j, 0, i),
                texture=f"textures/{config["texture"]}",
                parent=scene,
                origin_y=0.5,
            )
            boxes.append(box)


textures = ["grass.png", "glass.png", "stone.png", "iron_stone.png", "earth_bottom.png"]
selected_texture = textures[0]

texture_display = Entity(
    parent=camera.ui,
    model='quad',
    texture=f'textures/{selected_texture}',
    scale=(0.1, 0.1),
    position=(-0.83, 0.44)
)



highlight_border = Entity(
    parent=camera.ui,
    model='quad',
    color=color.white33,
    scale=(0.09, 0.09),
    position=(0, -0.45),
    enabled=True,
    z=-0.5
)

# Texture Options
texture_options_ui = []
spacing = 0.13
start_x = -((len(textures) - 1) * spacing) / 2
for i, texture_name in enumerate(textures):
    x = start_x + i * spacing
    icon = Entity(
        parent=camera.ui,
        model='quad',
        texture=f'textures/{texture_name}',
        scale=(0.08, 0.08),
        position=(x, -0.45)
    )
    number_label = Text(
        text=str(i + 1),
        parent=camera.ui,
        origin=(0, 0),
        position=(x, -0.53),
        scale=1.5,
        color=color.white
    )
    texture_options_ui.append((icon, number_label))

highlight_border.position = texture_options_ui[0][0].position
def handle_texture_selection(key):
    global selected_texture
    if key.isdigit():
        index = int(key) - 1
        if 0 <= index < len(textures):
            selected_texture = textures[index]
            texture_display.texture = f'textures/{selected_texture}'
            highlight_border.position = texture_options_ui[index][0].position


def input(key):
    if key == 'escape':
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
                    texture=f"textures/{selected_texture}",
                    parent=scene,
                    origin_y=0.5,
                )
                boxes.append(new_cube)

            if key == "right mouse down":
                boxes.remove(box)
                destroy(box)


config = {
    "texture": "grass.png",
    "axis": {"y": 10, "x": 10}
}
generate_terrain(config)
app.run()