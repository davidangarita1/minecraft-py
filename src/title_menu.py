# type: ignore

from pathlib import Path

from ursina import (
    Button,
    Entity,
    Text,
    application,
    camera,
    color,
    load_texture,
    mouse,
)

_FONT = "Monocraft.otf"

_TITLE_TEXT = "MINECRAFT-PY"
_TITLE_SCALE = 5
_TITLE_Y = 0.28

_BUTTON_WIDTH = 0.5
_BUTTON_HEIGHT = 0.065
_BUTTON_SPACING = 0.085

_PLAY_Y = 0.02
_SETTINGS_Y = _PLAY_Y - _BUTTON_SPACING
_EXIT_Y = _SETTINGS_Y - _BUTTON_SPACING

_BUTTON_COLOR = color.rgba(0.33, 0.33, 0.33, 0.85)
_BUTTON_HIGHLIGHT = color.rgba(0.47, 0.47, 0.72, 0.9)
_BUTTON_PRESSED = color.rgba(0.37, 0.37, 0.57, 0.9)
_BUTTON_DISABLED_COLOR = color.rgba(0.2, 0.2, 0.2, 0.6)
_BUTTON_DISABLED_TEXT = color.rgba(0.5, 0.5, 0.5, 0.7)
_BUTTON_TEXT_SCALE = 0.85

_TITLE_SHADOW_OFFSET = 0.003
_TITLE_SHADOW_COLOR = color.rgba(0.15, 0.15, 0.15, 0.7)

_BACKGROUND_BLUR_COLOR = color.rgba(0, 0, 0, 0.35)


class TitleMenu(Entity):
    def __init__(self, on_play, **kwargs):
        super().__init__(parent=camera.ui, z=-20)
        self._on_play = on_play
        self._build_background()
        self._build_title()
        self._build_buttons()
        mouse.locked = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _build_background(self):
        source_directory = Path(__file__).parent
        background_folder = source_directory.parent / "docs" / "images"
        background_texture = load_texture("title-bg.png", folder=background_folder)

        Entity(
            parent=self,
            model="quad",
            texture=background_texture,
            scale=(2, 1),
            z=1,
        )

        Entity(
            parent=self,
            model="quad",
            color=_BACKGROUND_BLUR_COLOR,
            scale=(2, 1),
            z=0.9,
        )

    def _build_title(self):
        Text(
            parent=self,
            text=_TITLE_TEXT,
            font=_FONT,
            origin=(0, 0),
            y=_TITLE_Y + _TITLE_SHADOW_OFFSET,
            x=_TITLE_SHADOW_OFFSET,
            scale=_TITLE_SCALE,
            color=_TITLE_SHADOW_COLOR,
            z=0.5,
        )

        Text(
            parent=self,
            text=_TITLE_TEXT,
            font=_FONT,
            origin=(0, 0),
            y=_TITLE_Y,
            scale=_TITLE_SCALE,
            color=color.white,
            z=0.4,
        )

    def _build_buttons(self):
        self._build_play_button()
        self._build_settings_button()
        self._build_exit_button()

    def _build_play_button(self):
        play_button = Button(
            parent=self,
            text="Play",
            scale=(_BUTTON_WIDTH, _BUTTON_HEIGHT),
            y=_PLAY_Y,
            color=_BUTTON_COLOR,
            highlight_color=_BUTTON_HIGHLIGHT,
            pressed_color=_BUTTON_PRESSED,
            on_click=self._start_game,
            text_size=_BUTTON_TEXT_SCALE,
        )
        play_button.text_entity.font = _FONT

    def _build_settings_button(self):
        settings_button = Button(
            parent=self,
            text="Settings",
            scale=(_BUTTON_WIDTH, _BUTTON_HEIGHT),
            y=_SETTINGS_Y,
            color=_BUTTON_DISABLED_COLOR,
            highlight_color=_BUTTON_DISABLED_COLOR,
            pressed_color=_BUTTON_DISABLED_COLOR,
            text_size=_BUTTON_TEXT_SCALE,
        )
        settings_button.text_entity.font = _FONT
        settings_button.text_entity.color = _BUTTON_DISABLED_TEXT

    def _build_exit_button(self):
        exit_button = Button(
            parent=self,
            text="Exit",
            scale=(_BUTTON_WIDTH, _BUTTON_HEIGHT),
            y=_EXIT_Y,
            color=_BUTTON_COLOR,
            highlight_color=_BUTTON_HIGHLIGHT,
            pressed_color=_BUTTON_PRESSED,
            on_click=application.quit,
            text_size=_BUTTON_TEXT_SCALE,
        )
        exit_button.text_entity.font = _FONT

    def _start_game(self):
        self.enabled = False
        self._on_play()
