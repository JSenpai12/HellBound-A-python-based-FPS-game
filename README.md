# Hellbound

A Doom-inspired 2.5D FPS game built with **Python and Ursina**.

The project uses a 3D environment with 2D billboard sprites for enemies, weapons, and items, inspired by the visual style of the original *Doom* (1993).

> 🚧 **Project Status: In Progress**
>
> Hellbound is currently under development. Features, gameplay systems, levels, and assets are still being added.

## About

**Hellbound** is a learning project focused on building a simple Doom-style FPS from scratch using Python and the Ursina Engine.

Instead of using fully 3D models for everything, the game uses 2D sprites inside a 3D environment to create a classic 2.5D appearance.

## Current Features

* First-person player movement
* Player collision
* Grid-based levels using JSON
* Automatically generated walls and floors
* Pistol
* Shooting system
* Basic enemy system
* Imp enemy
* Enemy health and damage
* Enemy death
* Enemy AI with idle/chase/attack state machine
* Collision-aware enemy movement (won't walk through walls)
* Player health system with damage handling
* Enemy attacks (cooldown-based) that damage the player

## Technologies

* **Python**
* **Ursina Engine**
* **JSON** — level data
* **Freedoom** — sprites and textures

## Project Structure

```text
Hellbound/
├── main.py
├── settings.py
├── requirements.txt
├── README.md
│
├── assets/
│   ├── textures/
│   ├── audio/
│   └── fonts/
│
├── core/
│   ├── game.py
│   ├── input_handler.py
│   ├── camera_controller.py
│   └── game_state.py
│
├── entities/
│   ├── player.py
│   ├── enemy_base.py
│   ├── enemies/
│   ├── weapons/
│   ├── pickups/
│   └── projectiles.py
│
├── levels/
│   ├── level_loader.py
│   ├── level_data/
│   └── level_objects.py
│
├── ui/
│   ├── hud.py
│   ├── main_menu.py
│   ├── pause_menu.py
│   └── minimap.py
│
├── systems/
│   ├── combat_system.py
│   ├── ai_system.py
│   ├── audio_manager.py
│   ├── save_system.py
│   └── collision_manager.py
│
└── utils/
    ├── math_utils.py
    └── constants.py
```

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/hellbound.git
cd hellbound
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Linux/macOS:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Game

```bash
python main.py
```

## Controls

| Key            | Action      |
| -------------- | ----------- |
| **W A S D**    | Move        |
| **Mouse**      | Look around |
| **Left Click** | Shoot       |

## Level System

Levels are stored as JSON files inside:

```text
levels/level_data/
```

The level uses a simple grid system:

```text
1 = Wall
0 = Floor
```

Example:

```text
111111
100001
101101
100001
111111
```

The game reads the grid and automatically creates the 3D walls and floor.

## Enemies

Enemies use a basic enemy system.

The current enemy is the **Imp**, which uses a 2D sprite inside the 3D environment.

Enemies currently have:

* Health
* Damage handling
* Death
* Collision
* Billboard sprites

## Assets

The project is intended to use assets from [Freedoom](https://freedoom.github.io/), a free and open replacement for the original Doom game assets.

The project does not use the original copyrighted Doom assets.

## Development

Hellbound is a **work in progress**.

The project is being developed step by step, starting with the basic player, level, weapon, and enemy systems before expanding into more advanced gameplay features.

More features, enemies, weapons, levels, sounds, and gameplay systems will be added as development continues.

## License

This project is intended for educational and personal development purposes.

Freedoom assets are distributed under their respective free/open licenses. Please refer to the [Freedoom project](https://freedoom.github.io/) for asset licensing information.

