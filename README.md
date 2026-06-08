# Chess
A passion project to remove the dust (and maybe add more shine) to my software engineering abilities.

The main focuses are good architecture and TDD.

Run `python3 -m src.myproject` to play.

## Remaining Development Tasks
- [ ] Checkmate
- [ ] Stalemate
- [ ] Castling
- [ ] En Passant
- [ ] Promotion
- [ ] Will move put king in check?
    - [x] Is piece in check?
    - [ ] Simulate board move
- [ ] Testing

## Structure
```
.
├── README.md
├── src
│   └── myproject
│       ├── __init__.py
│       ├── __main__.py
│       ├── game.py
│       ├── pieces.py
│       ├── player.py
│       ├── rules.py
│       └── utils
│           ├── __init__.py
│           └── board_utils.py
└── tests
    ├── fakes
    │   └── fake_game.py
    ├── test_moves.py
    └── testutils
        └── exceptions.py

```

### game.py
Contains the `Game` class which is responsible for handling the gameplay loop.

### pieces.py
Contains the `ChessPiece` class and its subclasses.

Each chess piece holds the following information:
- Its position on the board
- It's owner
- It's moveset (represented by `ChessMove`)

### move.py
Contains the `ChessMove` class which is responsible for representing moves that chess pieces can make, alongside their requirements (e.g. a pawn must be taking a piece to move diagonally).

### player.py
Contains the `Player` class and its subclasses which is responsible for representing the player and their pieces.

### rules.py
Contains the `Rules` class which is responsible for enforcing rules that require knowledge of the board state (e.g. a bishop can move any distance diagonally until it's blocked by another piece or the board edge).

### utils/
Contains common resources that are used across multiple classes.
