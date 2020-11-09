import random

class Agent():
    def get_next_state(self, possible_next_states):
        best_next_state = random.randint(0, len(possible_next_states)-1)
        return best_next_state
        
    def add_to_memory(self, reward):
        pass