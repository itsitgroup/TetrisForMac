# Tetris for Mac with Apple Silicon - User Guide

## Introduction

Welcome to Tetris for Mac with Apple Silicon! This game is a modern implementation of the classic Tetris game, optimized specifically for Mac computers with Apple Silicon (M-series) chips. The game features smooth gameplay, beautiful graphics, and takes full advantage of the performance capabilities of your M-series Mac.

## System Requirements

- macOS 11.0 (Big Sur) or later
- Mac with Apple Silicon (M1, M1 Pro, M1 Max, M1 Ultra, M2, or newer)
- 50MB of free disk space
- Keyboard for controls

## Installation

1. Extract the `TetrisForMac-AppleSilicon.zip` file
2. Drag the `TetrisForMac.app` to your Applications folder
3. Right-click on the app and select "Open" (required only the first time you run the app)
4. Enjoy playing!

## Game Controls

- **Left Arrow**: Move piece left
- **Right Arrow**: Move piece right
- **Down Arrow**: Soft drop (move piece down faster)
- **Up Arrow**: Rotate piece clockwise
- **Space**: Hard drop (instantly drop piece to bottom)
- **P**: Pause/Resume game
- **M**: Mute/Unmute sound
- **B**: Change block style
- **R**: Restart game (when game over)

## Game Features

### Gameplay
- Classic Tetris gameplay with modern enhancements
- Ghost piece preview shows where your piece will land
- Next piece preview
- Four different block styles (classic, rounded, gradient, and 3D)

### Scoring System
- Points for clearing lines (more points for multiple lines at once)
- Bonus points for hard drops
- Combo system for clearing lines in succession
- T-spin detection and bonus points
- Back-to-back Tetris bonus

### Graphics and Effects
- Smooth animations and particle effects
- Line clear animations
- Level up animations
- Background star effects

### Apple Silicon Optimizations
- Metal-based rendering for improved performance
- Memory optimizations for ARM architecture
- Optimized input handling
- Proper macOS application bundle

## Game Mechanics

### Levels
The game starts at level 1 and increases by one level for every 10 lines cleared. As the level increases, pieces fall faster, making the game more challenging.

### Rotation System
The game uses a modern rotation system with wall kicks, allowing pieces to rotate even when next to walls or other blocks by automatically shifting the piece if possible.

### Scoring Details
- Single line: 100 × level
- Double line: 300 × level
- Triple line: 500 × level
- Tetris (four lines): 800 × level
- T-spin bonus: 400 × lines cleared × level
- Back-to-back Tetris: 400 × level
- Combo bonus: 50 × combo count × level
- Hard drop: 1 point per cell dropped

## Troubleshooting

### Game Won't Start
- Make sure you're running macOS 11.0 (Big Sur) or later
- Right-click the app and select "Open" to bypass Gatekeeper on first run
- Check that you have sufficient disk space

### Performance Issues
- Close other applications that might be using significant system resources
- Try changing the block style to "classic" for better performance
- Make sure your system is not in low power mode

### Sound Issues
- Check if the game is muted (press M to toggle)
- Verify your system volume is turned up
- Ensure your Mac's sound output device is properly configured

## Credits

This game was created as a modern implementation of Tetris, optimized specifically for Apple Silicon Macs. The game uses Pygame for rendering and includes custom optimizations for M-series chips.

## Contact

If you encounter any issues or have suggestions for improvements, please contact us at support@tetrisformac.example.com.

Enjoy the game!
