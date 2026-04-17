# Business Context

## Product Overview

Minecraft-py is a sandbox exploration game where players navigate a three-dimensional world made entirely of blocks. The world is generated automatically each time a new session starts, creating unique landscapes with hills, valleys, and layered terrain. Players interact with the environment by placing and removing blocks, giving them full creative freedom to reshape the world around them.

## Target Audience

Casual gamers, hobbyists, and educators looking for a lightweight, open-source sandbox experience that runs directly from a command line without complex installation steps.

## Core Value Proposition

A simple, self-contained block-building game that requires no account, no launcher, and no configuration — just one command to start playing.

## Key Capabilities

### Title Screen

When the game launches, players are greeted with a title screen that displays the game name in a large, stylized block font over a scenic background image. From here, players can start a new session by pressing Play, or close the application with Exit. A Settings button is also present for future use. The world is not created until the player chooses to begin, keeping startup fast and giving players a clear entry point into the experience.

### World Generation

Every game session produces a unique landscape. The terrain includes surface layers, underground layers, and a solid foundation at the bottom that cannot be removed. This ensures every playthrough feels different while maintaining a consistent structure.

### Block Interaction

Players can place new blocks onto existing surfaces and remove blocks from the world. Nine different block types are available (grass, dirt, stone, snow, ice, lava, brick, gravel, cobblestone), selectable from a toolbar displayed at the bottom of the screen.

### Movement Modes

Two movement modes are available:

- **Walking mode**: The player walks on the ground with gravity applied, and can jump over obstacles.
- **Creative flight mode**: The player can fly freely in any direction, including ascending and descending, to quickly traverse or build in the world. Activated by double-tapping the jump action.

### Toolbar

A nine-slot toolbar at the bottom of the screen shows the available block types. Players select a slot using number keys, and the currently selected block type is visually highlighted. Each slot displays a preview of the block's appearance.

### Pause Menu

The game can be paused at any time, presenting options to resume play or exit the application. The pause action remains responsive regardless of the game state.

## User Interactions Summary

| Action                | Result                                      |
| --------------------- | ------------------------------------------- |
| Launch the game        | View the title screen with Play, Settings, and Exit options |
| Click Play             | Start a new session and enter the world     |
| Click Exit (title)     | Close the application from the title screen |
| Move around            | Navigate the world on foot                  |
| Jump                   | Leap over single-block obstacles            |
| Toggle flight          | Switch between walking and free flight      |
| Place a block          | Add a block of the selected type to a surface |
| Remove a block         | Destroy an existing block from the world    |
| Select toolbar slot    | Choose which block type to place            |
| Pause / Resume         | Freeze or continue the game session         |
| Exit                   | Close the application                       |

## Performance Considerations

The game only renders blocks that are visible to the player — blocks fully surrounded by other blocks are hidden until an adjacent block is removed. This keeps the experience smooth even in larger worlds.

## Current Limitations

- The world size is fixed per session and does not expand as the player moves.
- There is no save or load functionality — the world is lost when the application closes.
- There is no multiplayer or networked play.
- There is no sound or music.
- The block type catalog is fixed at nine types.

## Future Opportunity Areas

- Persistent world saving and loading across sessions.
- Expandable worlds that grow as the player explores.
- Additional block types and decorative elements.
- Sound effects and ambient music.
- Multiplayer or shared world support.
- Mobile or web-based deployment.
