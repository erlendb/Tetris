import environment
import agent
from tetris import Piece, get_board_with_piece_matrix
import sys

logstr = ''
if len(sys.argv) > 1:
    logstr = str(sys.argv[1])

env = environment.Environment(number_of_games = 100)
agt = agent.Agent(num_training_games = 100)
for i in range(env.number_of_games):
    #env.game.print() #debugger
    print(env.game_iterator) #debugger
    while not env.game.is_game_over():
        board = env.game.board
        piece_matrix = env.game.get_piece()
        piece = Piece(piece_matrix)
        
        possible_piece_placements = env.game.get_possible_piece_placements()
        #for p in possible_piece_placements: #debugger
        #    print(p) #debugger
        possible_next_states = []
        for piece_placement in possible_piece_placements:
            (x, y), rotation = piece_placement
            piece.set_rotation(rotation)
            piece.set_position(x, y)
            state = get_board_with_piece_matrix(board, piece)
            possible_next_states.append(state)
        next_state_id = agt.get_next_state(possible_next_states)
        env.place_piece(possible_piece_placements[next_state_id])
        env.tick()
        #env.game.print() #debugger
        reward = env.get_reward()
        agt.add_to_memory(possible_next_states[next_state_id], reward, env.game.is_game_over())
    env.log_write(logstr, agt.epsilon)
    env.reset_game()

    agt.train()
