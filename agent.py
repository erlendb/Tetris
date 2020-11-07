import random

def get_action(state, possible_next_states):
    best_next_state = random.randint(0, len(possible_next_states))
    return best_next_state