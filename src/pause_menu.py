# type: ignore

from ursina import (
    Button,
    Entity,
    Text,
    application,
    camera,
    color,
    mouse,
)


class PauseMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=camera.ui,
            ignore_paused=True,
            z=-10,
        )
        self.is_open = False
        self.menu_parent = Entity(parent=self, enabled=False)

        Entity(
            parent=self.menu_parent,
            model='quad',
            color=color.rgba(0, 0, 0, 0.7),
            scale=(2, 2),
            z=1,
        )

        Text(
            parent=self.menu_parent,
            text='Game Paused',
            origin=(0, 0),
            y=0.15,
            scale=3,
            color=color.white,
        )

        Button(
            parent=self.menu_parent,
            text='Resume',
            scale=(0.3, 0.07),
            y=0.0,
            color=color.rgba(0.2, 0.2, 0.2, 0.8),
            highlight_color=color.rgba(0.3, 0.5, 0.3, 0.85),
            pressed_color=color.rgba(0.25, 0.4, 0.25, 0.85),
            on_click=self.resume,
            ignore_paused=True,
        )

        Button(
            parent=self.menu_parent,
            text='Exit',
            scale=(0.3, 0.07),
            y=-0.1,
            color=color.rgba(0.2, 0.2, 0.2, 0.8),
            highlight_color=color.rgba(0.5, 0.25, 0.25, 0.85),
            pressed_color=color.rgba(0.4, 0.15, 0.15, 0.85),
            on_click=application.quit,
            ignore_paused=True,
        )

        for key, value in kwargs.items():
            setattr(self, key, value)

    def toggle(self):
        if self.is_open:
            self.resume()
        else:
            self.pause()

    def pause(self):
        self.is_open = True
        self.menu_parent.enabled = True
        application.paused = True
        mouse.locked = False

    def resume(self):
        self.is_open = False
        self.menu_parent.enabled = False
        application.paused = False
        mouse.locked = True

    def input(self, key):
        if key == 'escape':
            self.toggle()
