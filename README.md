# Tetris

This thing is supposed to be some sort of framework for playing Tetris. The idea is to use this framwork together with machine learning methods. Machine learning methods can be implemented so that they interact directly with the Tetris framework.

* *tetris.py* contains the Tetris framework, as explained in the Reference section.
* *example.py* contains a simple implementation of a terminal Tetris game, using the framework. Run with `sudo python3 example.py`. `sudo` is needed due to the use of the `keyboard` module.
* graphic_example contains a graphical implementation based on pyGame. Run with `sudo python3 example.py` as in example.py.
    * To install pygame on python 3.8, use `python3 -m pip install pygame==2.0.0.dev10`

## Reference

### Piece matrices

Pieces are represented as two dimensional lists. E.g. the square piece and the "L" piece is represented as follows:
```python
# square
[
  [1, 1],
  [1, 1]
]

# L
[
  [1, 0],
  [1, 0],
  [1, 1]
]
```

### Piece movement
Vertical and horizontal movement:

```
Move left                         | Original |   Move right
game.move_piece_horizontally(-1)  | piece    |   game.move_piece_horizontally(1)
game.move_piece_left()            | position |   game.move_piece_right()

                              Move down
                              game.move_piece_down()

                              Move down as far as allowed
                              game.move_piece_down_until_not_allowed()
```

Piece rotation:
```
Rotate counter-clockwise |  Original rotation: | Rotate clockwise
game.rotate_piece(-1)    |                     | game.rotate_piece(1)
                         |                     | game.rotate_piece_clockwise()
                         |         X           |
                  X      |         X           |     XXX
                XXX      |         XX          |     X
```
The piece will always be positioned on the board based on its left bottom pixel.

### The board
The board is represented as a two dimensional list. Below is an example of a game board as the user will see it:
```
y-axis

5 |          |
4 |          |
3 |    X     |
2 |    X     |
1 | X  X  X  |
0 |XXX_X__XXX|
   0123456789  x-axis
```

This board is represented by the following matrix:
```python
[
  [1, 1, 1, 0, 1, 0, 0, 1, 1, 1],
  [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
```

As you can see from the figure and the matrix, the bottom left corner of the game board is the `[0][0]` element of the matrix.

### The `Game` class

#### `pieces`
A list of all pieces available for the player.

Note that errors might occur if you try to modify or call the methods of the pieces in the `pieces` list directly.

#### `piece`
The current piece. This is the piece the player is about to place on the board. Instance of the `Piece` class

Note that errors might occur if you try to modify or call the methods of the `piece` directly.

#### `next_piece_id`
The id of the piece that will become current in the next round.

#### `board`
An instance of the `Board` class.

Note that errors might occur if you try to modify or call the methods of the `board` directly.

#### `tick_count`
The number of ticks performed this round.

#### `round_count`
The number of rounds since the game started. The round count is increased each time a piece is permanently added to the board.

#### `score`
The score achieved so far in the game.

#### `line_clear_scores`

A dictionary defining how much score the player will get when clearing a number of lines from the board. The dictionary is on the form `number of lines cleared: score`.
By default:
```python
{
  0: 0,
  1: 100,
  2: 300,
  3: 500,
  4: 800
}
```

#### `__init__( [board_width, board_height, pieces] )`
Initiates the game.

* `board_width` (optional): the with of the game board
* `board_height` (optional): the height of the game board
* `pieces` (optional): list of pieces that will be available for the player.

If not specified, the board width and board height will be set to the default values og the `Board` class. The pieces list will default to the 7 standard Tetris pieces.

#### `print()`
Print the game in its current state, together with available information. Useful for debugging or for simple Tetris implementations.

#### `is_piece_position_allowed( [x, y, rotation] )`
Checks if the current piece is allowed in the game board at position `x, y` rotated `rotation` times clockwise.

Returns `False` if the piece crashes with already filled spots on the board, or if the piece will be positioned fully or partly outside of the board.

#### `is_game_over()`
Returns `True` if there are no empty lines left on the board.

#### `pop_full_lines()`
Pops all the full lines of the board. Adds empty line on the top of the board for each line popped. Returns the number of lines that was popped.

#### `tick()`
Takes the game one step further. This means lowering the piece one step on the board if possible. If not possible, the piece is permanently added to the board at its current position, then full lines are popped, and the current piece and the next piece is updated.

#### `get_tick_count()`
Returns the current tick count. The tick count is reset each new round.

#### `get_round_count()`
Returns the current round count. The round count is increased each time a piece is permanently added to the board.

#### `get_board()`
Returns the board matrix, without the piece yet to be added permanently.

#### `get_piece()`
Returns the matrix of the current piece.

#### `get_board_with_piece()`
Returns a merged matrix of the board matrix and the matrix of the current piece at its current position.

#### `get_piece_position()`
Returns the position `x, y` of the current piece

#### `get_score()`
Get the current score.

#### `set_piece_position(x, y)`
Set a new position of the current piece, given that the provided position is allowed.

#### `set_piece(piece_id)`
Change the current piece, given that the `piece_id` exists in the `pieces` list.

#### `set_next_piece_id(piece_id)`
Change the next piece, given that the `piece_id` exists in the `pieces` list.

#### `reset_piece_position()`
Reset the position of the current piece according to the board dimensions. The piece will be moved to the top center of the board.

#### `rotate_piece(rotation)`
Rotate the current piece `rotation` times clockwise, given that the new piece position and orientation is allowed. `rotation` can be any integer.

#### `rotate_piece_clockwise()`
Rotate the current piece one time clockwise, given that the ned piece position and orientation is allowed

#### `move_piece_down()`
Move the current piece one step down on the board, without performing a tick, given that the new position is allowed.

#### `move_piece_down_until_not_allowed()`
Move the current piece as far down on the board as possible, without performing a tick.

#### `move_piece_horizontally(movement)`
Move the current piece `movement` steps horizontally, given that the new position is allowed.

#### `move_piece_left()`
Move the current piece one step left, given that the new position is allowed.

#### `move_piece_right()`
Move the current piece one step right, given that the new position is allowed.
