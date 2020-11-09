import random

def get_next_state(possible_next_states):
    best_next_state = random.randint(0, len(possible_next_states)-1)
    return best_next_state