import tetris
from datetime import datetime

class Environment():
    def __init__(self, number_of_games = 1):
        self.game = tetris.Game()
        self.number_of_games = number_of_games
        self.game_iterator = 0
        self.game_score = 0
    
    def tick(self):
        self.game.tick()
        self.game_score += self.get_reward()
    
    def reset_game(self):
        self.game = tetris.Game()
        self.game_iterator += 1
        self.game_score = 0
        
    def place_piece(self, placement):
        (next_position_x, next_position_y), next_rotation = placement
        self.game.rotate_piece(next_rotation)
        self.game.set_piece_position(next_position_x, next_position_y)
    
    def get_reward(self):
        popped_lines = self.game.get_popped_lines()
        reward = 1 + popped_lines**2
        if self.game.is_game_over():
            reward = -10
        return reward
    
    def log_write(self, model_name, extra_information, epsilon):
        log_file = 'logs/' +  model_name + '.txt'
        with open(log_file, 'a') as log:
            if self.game_iterator == 0:
                log.write(f"Model name: {model_name}\n")
                log.write(f"Extra information: {extra_information}\n")
                log.write(f"Timestamp: {datetime.now()}\n")
                log.write(f"Game Rounds Score Epsilon\n")
            log.write(f"{self.game_iterator} {self.game.get_round_count()} {self.game_score} {epsilon}\n")
