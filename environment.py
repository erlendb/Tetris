import tetris
from datetime import datetime

class Environment():
    def __init__(self, number_of_games = 1):
        self.game = tetris.Game()
        self.number_of_games = number_of_games
        self.game_iterator = 0
        self.game_cleared_lines = 0
        self.game_score = 0

    def tick(self):
        self.game.tick()
        self.game_cleared_lines += self.game.get_popped_lines()
        self.game_score += self.get_reward()

    def reset_game(self):
        self.game = tetris.Game()
        self.game_iterator += 1
        self.game_cleared_lines = 0
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
                log.write(f"Game Rounds Score Epsilon ClearedLines\n")
            log.write(f"{self.game_iterator} {self.game.get_round_count()} {self.game_score} {epsilon} {self.game_cleared_lines}\n")


    def get_board_features(self, board_matrix):
        height = 0
        lines_cleared = 0
        holes = 0
        for row in range(len(board_matrix)):
            if any(board_matrix[row]):  # If at least one block in row
                height = row
            if all(board_matrix[row]):  # If row is full (will be cleared)
                lines_cleared += 1
            for col in range(len(board_matrix[row])):
                if row == len(board_matrix)-1:
                    break
                if not board_matrix[row][col] and board_matrix[row + 1][col]:
                    holes += 1

        return height, lines_cleared, holes

