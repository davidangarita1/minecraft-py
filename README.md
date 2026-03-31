# minecraft-py

A Minecraft-inspired 3D voxel game built with Python and the [Ursina](https://www.ursinaengine.org/) game engine.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

## Run

```bash
uv run python src/main.py
```

## Controls

| Key | Action |
|-----|--------|
| `W A S D` | Move |
| `Space` | Jump |
| `Double Space` | Toggle creative mode (fly) |
| `Shift` | Descend (creative mode) |
| `Left Click` | Place block |
| `Right Click` | Destroy block |
| `1` / `2` | Select block texture |
| `Esc` | Pause / Resume |

## Features

- Procedural terrain generation using Perlin noise
- Block types: grass, dirt, stone, bedrock
- Face-culling optimization — only exposed block faces are rendered as entities
- Neighbor exposure system — when a block is removed, hidden adjacent blocks are automatically revealed
- Creative mode (fly) with double-tap Space
- Pause menu with Resume and Exit options
- First-person controller with gravity and jump

## Project Structure

```
src/
├── main.py         # Entry point, terrain generation, input handling
├── block.py        # Block entity definition and texture registry
├── chunk.py        # Neighbor directions constant (NEIGHBORS)
└── pause_menu.py   # ESC pause menu with Resume / Exit
```

## Architecture

### Face culling
All block data is stored in a flat `world_blocks` dict before any entities are created. Only blocks with at least one air neighbor are spawned as Ursina entities. This reduces the entity count by ~80% compared to spawning every block.

### Pause menu
`PauseMenu` is always enabled as an Ursina `Entity` so its `input()` method fires with `ignore_paused=True`. Only the visual `menu_parent` container toggles visibility, keeping ESC functional both in-game and while paused.
