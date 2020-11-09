import tetris
import agent
import keyboard
from copy import deepcopy

game = tetris.Game()
game.print()

while not game.is_game_over():
    board = game.get_board()
    piece = game.get_piece()
    possible_piece_placements = game.get_possible_piece_placements()
    for p in possible_piece_placements:
        print(p)
    possible_next_states = []
    for piece_placement in possible_piece_placements:
        possible_next_states.append((board, piece, piece_placement))
    next_state_id = agent.get_next_state(possible_next_states)
    (next_position_x, next_position_y), next_rotation = possible_next_states[next_state_id][2]
    game.rotate_piece(next_rotation)
    game.set_piece_position(next_position_x, next_position_y)
    game.print()
    game.tick()