# type: ignore

from ursina import Entity, Text, camera, color

TOTAL_SLOTS = 9

_SLOT_SIZE = 0.068
_ICON_SIZE = 0.056
_STEP = 0.080
_Y = -0.42
_DARK = color.rgba(0.12, 0.12, 0.12, 0.88)
_SELECTED = color.rgba(0.28, 0.28, 0.28, 0.92)


class Hotbar(Entity):
    def __init__(self, slot_types):
        super().__init__(parent=camera.ui)
        self.slot_types = slot_types
        self.selected_index = 0
        self._borders = []
        self._bgs = []
        self._build()

    def _build(self):
        total_span = (TOTAL_SLOTS - 1) * _STEP

        Entity(
            parent=self,
            model="quad",
            color=color.rgba(0, 0, 0, 0.6),
            scale=(total_span + _SLOT_SIZE + 0.024, _SLOT_SIZE + 0.024),
            position=(0, _Y),
            z=0.3,
        )

        for i in range(TOTAL_SLOTS):
            x = -total_span / 2 + i * _STEP

            border = Entity(
                parent=self,
                model="quad",
                color=color.white,
                scale=(_SLOT_SIZE + 0.009, _SLOT_SIZE + 0.009),
                position=(x, _Y),
                z=0.2,
                enabled=(i == 0),
            )

            bg = Entity(
                parent=self,
                model="quad",
                color=_SELECTED if i == 0 else _DARK,
                scale=(_SLOT_SIZE, _SLOT_SIZE),
                position=(x, _Y),
                z=0.1,
            )

            if i < len(self.slot_types):
                _, tex = self.slot_types[i]
                Entity(
                    parent=self,
                    model="quad",
                    texture=tex,
                    scale=(_ICON_SIZE, _ICON_SIZE),
                    position=(x, _Y),
                    z=0.05,
                )

            Text(
                parent=self,
                text=str(i + 1),
                origin=(0.5, -0.5),
                position=(x + _SLOT_SIZE * 0.46, _Y - _SLOT_SIZE * 0.44),
                scale=0.6,
                color=color.rgba(0.85, 0.85, 0.85, 0.9),
                z=0,
            )

            self._borders.append(border)
            self._bgs.append(bg)

    @property
    def selected_type(self):
        if self.selected_index < len(self.slot_types):
            return self.slot_types[self.selected_index][0]
        return None

    def select(self, index):
        if not (0 <= index < TOTAL_SLOTS):
            return
        self._borders[self.selected_index].enabled = False
        self._bgs[self.selected_index].color = _DARK
        self.selected_index = index
        self._borders[index].enabled = True
        self._bgs[index].color = _SELECTED
