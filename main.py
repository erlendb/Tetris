import environment
import agent
from tetris import Piece, get_board_with_piece_matrix
import time
timestamp = str(time.time())

### Change these settings before running main.py
model_name = timestamp + 'model1' # Name of the output log file and the output model files. NB: if model_name is the same as an existing model/log, the existing files will be overwritten!
log_extra_information = '' # Extra information to put in the log file
load_model_name = '' # Name of the model you want to load. Leave blank if you want to build a new model.
number_of_training_games = 2 # Games where the epsilon goes from 1 to 0.
number_of_games_total = number_of_training_games + 2 # If this is higher than number_of_training_games, then the last games will be run with epsilon 0 (always use the moves with the best reward)
###

agt = agent.Agent(num_training_games = number_of_training_games, saved_model_name = load_model_name)
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
        agt.add_to_memory(possible_next_states[next_state_id], reward, env.game.is_game_over())
    env.log_write(model_name = model_name, extra_information = log_extra_information, epsilon = agt.epsilon)
    env.reset_game()

    agt.train()
    
    if (i % 100) == 0:
        agt.save_model(model_name)

agt.save_model(model_name)
