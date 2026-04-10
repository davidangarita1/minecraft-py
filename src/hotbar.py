# type: ignore

from ursina import Entity, Text, camera, color

TOTAL_SLOTS     = 9

_SLOT_SIZE      = 0.068
_ICON_SIZE      = 0.056
_STEP           = 0.080
_Y              = -0.42
_BORDER_PADDING = 0.009
_BAR_PADDING    = 0.024
_BAR_ALPHA      = 0.6
_LABEL_SCALE    = 0.6
_LABEL_ALPHA    = 0.9
_LABEL_OFFSET_X = 0.46
_LABEL_OFFSET_Y = 0.44
_Z_BAR          = 0.3
_Z_BORDER       = 0.2
_Z_BG           = 0.1
_Z_ICON         = 0.05

_DARK           = color.rgba(0.12, 0.12, 0.12, 0.88)
_SELECTED       = color.rgba(0.28, 0.28, 0.28, 0.92)

_TEX_SIZE       = 1024
_CROP_X         = 318 / _TEX_SIZE
_CROP_Y         = 300 / _TEX_SIZE
_CROP_SCALE     = 300 / _TEX_SIZE


def _slot_icon(parent, texture, px, py, size, z):
    icon = Entity(
        parent=parent,
        model='quad',
        texture=texture,
        scale=(size, size),
        position=(px, py, z),
    )
    icon.texture_scale = (_CROP_SCALE, _CROP_SCALE)
    icon.texture_offset = (_CROP_X, _CROP_Y)


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
        self._build_background(total_span)
        for i in range(TOTAL_SLOTS):
            x = -total_span / 2 + i * _STEP
            self._build_slot(i, x)

    def _build_background(self, total_span):
        Entity(
            parent=self,
            model='quad',
            color=color.rgba(0, 0, 0, _BAR_ALPHA),
            scale=(total_span + _SLOT_SIZE + _BAR_PADDING, _SLOT_SIZE + _BAR_PADDING),
            position=(0, _Y),
            z=_Z_BAR,
        )

    def _build_slot(self, index, x):
        border = Entity(
            parent=self,
            model='quad',
            color=color.white,
            scale=(_SLOT_SIZE + _BORDER_PADDING, _SLOT_SIZE + _BORDER_PADDING),
            position=(x, _Y),
            z=_Z_BORDER,
            enabled=(index == 0),
        )
        bg = Entity(
            parent=self,
            model='quad',
            color=_SELECTED if index == 0 else _DARK,
            scale=(_SLOT_SIZE, _SLOT_SIZE),
            position=(x, _Y),
            z=_Z_BG,
        )
        if index < len(self.slot_types):
            _, tex = self.slot_types[index]
            _slot_icon(self, tex, x, _Y, _ICON_SIZE, _Z_ICON)
        self._build_label(index, x)
        self._borders.append(border)
        self._bgs.append(bg)

    def _build_label(self, index, x):
        Text(
            parent=self,
            text=str(index + 1),
            origin=(0.5, -0.5),
            position=(x + _SLOT_SIZE * _LABEL_OFFSET_X, _Y - _SLOT_SIZE * _LABEL_OFFSET_Y),
            scale=_LABEL_SCALE,
            color=color.rgba(0.85, 0.85, 0.85, _LABEL_ALPHA),
            z=0,
        )

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
