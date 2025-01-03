# Enhanced Snake Game

An enhanced version of the classic Snake game built with Python and Pygame. This game features power-ups, sound effects, and modern gaming elements while maintaining the classic Snake gameplay mechanics.
## Demo 
![image](https://github.com/user-attachments/assets/362c0f43-6510-4e81-a541-6211e866a70b)

## Features

- 🎮 Classic snake gameplay with modern enhancements
- 🎵 Background music and sound effects
- ⚡ Multiple power-ups:
  - Speed boost
  - Speed reduction
  - Point multipliers
  - Invincibility mode
- 💫 Visual effects and animations
- 🏆 High score tracking
- ⏸️ Pause functionality
- 🎨 Custom background
- 📊 Score display

## Requirements

- Python 3.x
- Pygame
- tkinter (usually comes with Python)

## Installation

1. Make sure you have Python installed on your system
2. Install the required packages:
```bash
pip install pygame
```

3. Clone or download this repository
4. Ensure you have all the required asset files in your project directory:
   - ThemeSong.wav
   - snack.wav
   - lose.wav
   - Snakebackground.png

## How to Play

1. Run the game:
```bash
python SnakeGame.py
```

2. Game Controls:
   - Arrow keys to move the snake
   - SPACE to start game/return to menu
   - P to pause/unpause
   - Close window to quit

3. Gameplay Elements:
   - Green squares: Regular food
   - Gold squares: Power-ups
   - Red squares: Snake body

## Game Mechanics

- **Basic Movement**: Use arrow keys to guide the snake
- **Scoring**: 
  - +10 points for each food eaten
  - Bonus points from power-ups
- **Power-ups**:
  - Appear randomly after eating food
  - Last for 5 seconds
  - Different types of power-ups have different effects
- **Game Over**: Occurs when snake collides with itself (unless invincible)
- **Screen Wrapping**: Snake can move through walls and appear on the opposite side

## Technical Details

- Window Size: 800x600 pixels
- Grid Size: 20x20 cells
- Cell Size: 25 pixels
- Frame Rate: Variable based on snake speed
  - Normal Speed: 10 FPS
  - Speed Power-up: 15 FPS
  - Slow Power-up: 5 FPS

## Project Structure

```
SnakeGame/
│
├── SnakeGame.py          # Main game file
├── assets/
│   ├── ThemeSong.wav    # Background music
│   ├── snack.wav        # Food collection sound
│   ├── lose.wav         # Game over sound
│   └── Snakebackground.png  # Game background image
│
└── README.md            # Game documentation
```

## Classes

- `Game`: Main game controller
- `Snake`: Snake logic and movement
- `Cube`: Individual snake segments and food
- `PowerUp`: Power-up items and effects
- `SoundManager`: Audio handling

## Contributing

Feel free to fork this project and submit pull requests. You can also open issues for bugs or feature suggestions.

## Credits

This is an enhanced version of the classic Snake game, implementing modern gaming features while maintaining the original gameplay concept.

## License

This project is open source and available under the MIT License.
