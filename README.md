# minecraft-py

A Minecraft-inspired 3D voxel game built with Python and the [Ursina](https://www.ursinaengine.org/) game engine. Start from a Minecraft-style title screen, explore procedurally generated terrain, place and destroy blocks, and switch between survival and creative flight modes.

![Demo](docs/images/demo.png)

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

## Run

```bash
uv run start
```

## Controls

| Key            | Action                     |
| -------------- | -------------------------- |
| `W A S D`      | Move                       |
| `Space`        | Jump                       |
| `Double Space` | Toggle creative mode (fly) |
| `Shift`        | Descend (creative mode)    |
| `Left Click`   | Place block                |
| `Right Click`  | Destroy block              |
| `1` – `9`      | Select hotbar slot         |
| `Scroll Wheel` | Cycle hotbar slots         |
| `Esc`          | Pause / Resume             |

## Features

- Minecraft-style title screen on startup with Play, Settings, and Exit buttons
- Procedural terrain generation using Perlin noise
- 9 block types: grass, dirt, stone, snow, ice, lava, brick, gravel, cobblestone
- Isometric block preview in the hotbar
- Face-culling optimization — only exposed block faces are rendered as entities
- Neighbor exposure system — when a block is removed, hidden adjacent blocks are automatically revealed
- Creative mode (fly) with double-tap Space
- Pause menu with Resume and Quit to Title options

## Project Structure

```sh
src/
├── main.py         # Entry point, terrain generation, input handling
├── block.py        # Block entity definition and texture registry
├── world_chunk.py  # Neighbor directions constant (NEIGHBORS)
├── hotbar.py       # Hotbar UI with slot selection and block preview
├── pause_menu.py   # ESC pause menu with Resume / Quit to Title
├── title_menu.py   # Startup title screen with Minecraft-style UI
└── assets/
    └── fonts/
        └── Monocraft.otf   # Minecraft-style font (OFL license)
docs/
├── features/
│   └── menu-title.feature.md   # EPIC with user stories for title menu
└── images/
    ├── demo.png        # Gameplay screenshot
    └── title-bg.png    # Title screen background
```

## Architecture

### Title screen

`TitleMenu` is shown at startup before gameplay begins. It renders a blurred background image, the game title in Monocraft font, and three buttons: Play, Settings (disabled), and Exit. Clicking Play tears down the menu and initializes the game world. Clicking "Quit to Title" from the pause menu destroys all world entities and returns to the title screen, freeing memory.

### Face culling

All block data is stored in a flat `world_blocks` dict before any entities are created. Only blocks with at least one air neighbor are spawned as Ursina entities. This reduces the entity count by ~80% compared to spawning every block.

### Hotbar

`Hotbar` renders nine slots at the bottom of the screen. Each slot displays a cropped section of the block texture (x: 318, y: 300, 300 × 300 px) on a quad entity. The selected slot is highlighted with a white border, and `Hotbar.select(index)` updates colors and border visibility without rebuilding any entities.

### Pause menu

`PauseMenu` is always enabled as an Ursina `Entity` so its `input()` method fires with `ignore_paused=True`. Only the visual `menu_parent` container toggles visibility, keeping ESC functional both in-game and while paused. "Quit to Title" destroys all gameplay entities and resets all state before reopening the title screen.

## Branch protection

| Branch    | Rule                                            |
| --------- | ----------------------------------------------- |
| `main`    | PR required · 1 approval · all checks must pass |
| `develop` | PR required · 1 approval · all checks must pass |

Direct pushes to `main` or `develop` are blocked. Force pushes and branch deletion are disabled.

## License

MIT
