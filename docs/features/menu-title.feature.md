# EPIC: Title Menu

## Overview

When the game starts, the player is greeted with a title screen before entering the world. This screen sets the visual identity of the game and provides the player with clear options: start playing, access settings, or exit the application. The title screen uses the game's name prominently displayed in a blocky, Minecraft-inspired font, layered over a softly blurred screenshot of the game world as a background.

## Business Value

A title menu gives the game a polished, professional first impression. It signals to the player that the experience is intentional and well-crafted, rather than dropping them directly into the world with no context. It also provides a natural place for future options such as settings, world selection, or multiplayer.

## User Stories

### US-01: Display title screen on startup

**As a** player,
**I want** to see a title screen when I launch the game,
**so that** I know the game has loaded and I can choose what to do next.

**Acceptance Criteria:**

```gherkin
Feature: Title screen display on startup

  Scenario: Title screen appears when the game starts
    Given the player launches the game with "uv run start"
    When the application window opens
    Then the title screen is displayed
    And the game world is not loaded yet
    And the mouse cursor is visible and unlocked

  Scenario: Title text is visible
    Given the title screen is displayed
    Then the text "MINECRAFT-PY" is shown in a large blocky font
    And the title is positioned in the upper portion of the screen
```

---

### US-02: Blurred background image

**As a** player,
**I want** the title screen to show a blurred game screenshot as the background,
**so that** the menu feels immersive and visually connected to the game world.

**Acceptance Criteria:**

```gherkin
Feature: Title screen background

  Scenario: Background image is displayed with blur
    Given the title screen is displayed
    Then the background shows the image from "docs/images/title-bg.png"
    And the background image is slightly blurred
    And the background covers the entire screen
```

---

### US-03: Play button starts the game

**As a** player,
**I want** to click a "Play" button on the title screen,
**so that** the world is generated and I can start exploring.

**Acceptance Criteria:**

```gherkin
Feature: Play button

  Scenario: Play button is visible on the title screen
    Given the title screen is displayed
    Then a "Play" button is visible below the title
    And the button has a Minecraft-style appearance with a stone-gray color

  Scenario: Clicking Play loads the world
    Given the title screen is displayed
    When the player clicks the "Play" button
    Then the title screen is hidden
    And the game world is generated and displayed
    And the player controller is active
    And the mouse cursor is locked for gameplay
    And the hotbar is visible

  Scenario: Play button highlights on hover
    Given the title screen is displayed
    When the player hovers over the "Play" button
    Then the button changes to a lighter highlighted color
```

---

### US-04: Settings button is present but disabled

**As a** player,
**I want** to see a "Settings" button on the title screen,
**so that** I know configuration options will be available in the future.

**Acceptance Criteria:**

```gherkin
Feature: Settings button

  Scenario: Settings button is visible but disabled
    Given the title screen is displayed
    Then a "Settings" button is visible below the "Play" button
    And the "Settings" button appears dimmed or grayed out
    And clicking the "Settings" button has no effect
```

---

### US-05: Exit button closes the application

**As a** player,
**I want** to click an "Exit" button on the title screen,
**so that** I can close the game without entering the world.

**Acceptance Criteria:**

```gherkin
Feature: Exit button

  Scenario: Exit button is visible on the title screen
    Given the title screen is displayed
    Then an "Exit" button is visible below the "Settings" button
    And the button has a Minecraft-style appearance

  Scenario: Clicking Exit closes the game
    Given the title screen is displayed
    When the player clicks the "Exit" button
    Then the application closes
```

---

### US-06: Title screen does not interfere with gameplay

**As a** player,
**I want** the title screen to fully disappear after I click Play,
**so that** nothing from the menu interferes with my gameplay experience.

**Acceptance Criteria:**

```gherkin
Feature: Title screen cleanup

  Scenario: Title screen elements are removed after Play
    Given the player has clicked the "Play" button
    When the game world is loaded
    Then no title screen elements are visible
    And the pause menu still works with ESC
    And block placement and destruction work normally
    And creative flight mode works normally
```
