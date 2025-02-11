# Chess-python

# Chess-python

A Python chess game with graphical interface built using PyQt5.

## Project Overview
- Complete chess implementation with GUI
- Object-oriented design with clean code structure
- Move validation and game state management
- Visual feedback for moves and game states

## Features
- Full chess game logic implementation
- Legal move validation for all pieces
- Check and checkmate detection
- Piece movement visualization
- Interactive board with piece highlighting
- Game state tracking

## Implementation Details
### Core Components:
- **Board Management**: [`ChessBoard`](scripts/board.py) handles game board visualization
- **Piece Logic**: [`ChessPiece`](scripts/piece.py) implements piece behaviors
- **Move Validation**: [`MoveRules`](scripts/rules.py) ensures legal moves
- **Game State**: [`GameState`](scripts/game_state.py) tracks game progress

### Project Structure
```
chess-python/
├── images/           # Chess piece images
├── scripts/
│   ├── board.py      # Board implementation
│   ├── constants.py  # Game constants
│   ├── piece.py      # Chess pieces
│   ├── rules.py      # Move validation
│   ├── square.py     # Board squares
│   └── game_state.py # Game state
└── main.py          # Entry point
```

## Setup & Running
1. Requirements:
   - Python 3.x
   - PyQt5

2. Installation:
```bash
pip install PyQt5
```

3. Run the game:
```bash
python main.py
```

## Development Status
### Implemented:
- Basic piece movements
- Legal move validation
- Check detection
- Board visualization
- Turn system

### TODO:
- [ ] Castling moves
- [ ] En passant
- [ ] Pawn promotion
- [ ] Stalemate detection
- [ ] Move history
- [ ] Save/Load games

## License
Released under the Unlicense - see LICENSE file for details.

## Contributing
Contributions welcome! Please feel free to submit pull requests.