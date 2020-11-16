import environment
import agent

env = environment.Environment(number_of_games = 10)
agt = agent.Agent()
for i in range(env.number_of_games):
    #env.game.print() #debugger
    print(env.game_iterator) #debugger
    while not env.game.is_game_over():
        board = env.game.get_board()
        piece = env.game.get_piece()
        possible_piece_placements = env.game.get_possible_piece_placements()
        #for p in possible_piece_placements: #debugger
        #    print(p) #debugger
        possible_next_states = []
        for piece_placement in possible_piece_placements:
            possible_next_states.append((board, piece, piece_placement))
        next_state_id = agt.get_next_state(possible_next_states)
        env.place_piece(possible_next_states[next_state_id][2])
        env.game.tick()
        env.game.print() #debugger
        reward = env.get_reward()
        agt.add_to_memory(possible_next_states[next_state_id], reward, env.game.is_game_over())
    env.log_write()
    env.reset_game()

    agt.train()
