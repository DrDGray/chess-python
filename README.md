# Chess

## How to Play
`python3 run.py`

## Structure

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
Contains the `Player` class and its subclasses which is resonsible for representing the player and their pieces.

### rules.py
Contains the `Rules` class which is responsible for enforcing rules that require knowledge of the board state (e.g. a bishop can move any distance diagonally until it's blocked by another piece or the board edge).

### _helper.py
Contains common resources that are used across multiple classes.

## Remaining Development Tasks
- [ ] Checkmate
- [ ] Stalemate
- [ ] Castling
- [ ] En Passant
- [ ] Promotion
- [ ] Will move put king in check?
