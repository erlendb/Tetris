import environment
import agent
from tetris import Piece, get_board_with_piece_matrix
import sys

###
logstr = ''
print_great_games = False
number_of_training_games = 4000
number_of_games_total = number_of_training_games + 500
load_model_name = '' # Leave blank ( '' ) if you want to build a new model
save_model_name = 'model3-natt'
###

highest_score = 0
agt = agent.Agent(num_training_games = number_of_training_games, saved_model_path = load_model_name)
env = environment.Environment(number_of_games = number_of_games_total)
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
        
        reward = env.get_reward()
        if print_great_games and env.game.is_game_over() and env.game_score > highest_score:
            highest_score = env.game_score
            env.game.print()
        
        agt.add_to_memory(possible_next_states[next_state_id], reward, env.game.is_game_over())
    env.log_write(logstr, agt.epsilon)
    env.reset_game()

    agt.train()

agt.save_model(save_model_name)
