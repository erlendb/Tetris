import tetris
from datetime import datetime

class Environment():
    def __init__(self, number_of_games = 1):
        self.game = tetris.Game()
        self.log_file = 'log.txt'
        self.number_of_games = number_of_games
        self.game_iterator = 0
        self.game_score = 0
    
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
        return 1 + popped_lines**2
        # if game over return -10
    
    def log_write(self):
        with open(self.log_file, 'a') as log:
            if self.game_iterator == 0:
                log.write(f"\nTimestamp: {datetime.now()}\n")
            log.write(f"Game number {self.game_iterator}, Rounds: {self.game.get_round_count()}, Score: {self.game_score}\n")
