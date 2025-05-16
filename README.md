# Jumping Ball Game

## Overview
A dynamic, endless jumping platformer game where players control a ball navigating through an ever-changing landscape of platforms.

## 🎮 Game Features

### Gameplay Mechanics
- Endless scrolling platformer
- Automatic jumping mechanism
- Procedurally generated platforms
- Dynamic difficulty progression

### Platform Varieties
- Standard platforms
- Moving platforms
- Disappearing platforms
- Dangerous platforms

### Sound Design
- Immersive background music
- Sound effects for:
  - Player jumps
  - Platform interactions
  - Game start/end events

### User Interface
- Intuitive main menu
- Game over screen with score display
- "Try Again" and "Main Menu" options

## 🕹️ Controls
- Automatic jumping
- No direct player input required
- Ball moves autonomously across platforms

## 🏆 Scoring
- Score increases with distance traveled
- Challenges become progressively harder

## 📦 Installation

### Requirements
- Python 3.8+
- Pygame
- PyInstaller (for creating executable)

### Running the Game
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python main.py`

### Creating Executable
```bash
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
```

## 🖼️ Screenshots

| Menu | Gameplay | How to Play |
|------|----------|-------------|
| ![Menu](docs/screenshots/menu.png) | ![Gameplay](docs/screenshots/game-play.png) | ![How to Play](docs/screenshots/how-to-play.png) |

| Custom Map Settings | Map Varieties | Settings |
|---------------------|---------------|----------|
| ![Custom Map Settings](docs/screenshots/custom-map-settings.png) | ![Maps](docs/screenshots/maps.png) | ![Settings](docs/screenshots/settings.png) |

## 🛠️ Customization
Adjust game parameters in `src/config/` files to modify:
- Platform generation
- Difficulty
- Sound settings

## 🤝 Contributing
Contributions are welcome! Please read the contributing guidelines. 