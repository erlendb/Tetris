import numpy
import random
import time
from copy import deepcopy

class Position():
    def __init__(self, x = -1, y = -1):
        self.x = x
        self.y = y

class Piece():
    def __init__(self, matrix):
        self.matrix = matrix
        
        self.rotated_matrices = []
        self.rotated_matrices.append(matrix)
        self.rotated_matrices.append(numpy.rot90(self.rotated_matrices[0], k = 1, axes = (1, 0)))
        self.rotated_matrices.append(numpy.rot90(self.rotated_matrices[1], k = 1, axes = (1, 0)))
        self.rotated_matrices.append(numpy.rot90(self.rotated_matrices[2], k = 1, axes = (1, 0)))
        
        self.rotation = 0
        self.position = Position()
    
    def rotate(self, rotation):
        self.rotation = (self.rotation + rotation) % 4
        self.matrix = self.rotated_matrices[rotation]
    
    def move_horizontally(self, movement):
        self.position.x += movement
    
    def move_vertically(self, movement):
        self.position.y += movement

class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[0 for i in range(width)] for j in range(height)]
    
    def add_piece(self, piece):
        for board_i in range(piece.position.y, min(self.height, piece.position.y + len(piece.matrix))):
            piece_i = board_i - piece.position.y
            for board_j in range(piece.position.x, piece.position.x + len(piece.matrix[0])):
                piece_j = board_j - piece.position.x
                if piece.matrix[piece_i][piece_j] == 1:
                    self.matrix[board_i][board_j] = 1
    
    def pop_line(line):
        self.matrix.pop(line)
        self.matrix.append([0 for i in range(width)])
        
class Game():
    def __init__(self):
        self.board = Board(10, 10)

        self.pieces = []
        self.pieces.append(Piece([[1, 1, 1, 1]]))
        self.pieces.append(Piece([[1, 0, 0], [1, 1, 1]]))
        self.pieces.append(Piece([[0, 0, 1], [1, 1, 1]]))
        self.pieces.append(Piece([[1, 1],    [1, 1]]))
        self.pieces.append(Piece([[0, 1, 1], [1, 1, 0]]))
        self.pieces.append(Piece([[0, 1, 0], [1, 1, 1]]))
        self.pieces.append(Piece([[1, 1, 0], [0, 1, 1]]))

        self.piece = random.choice(self.pieces)
        self.piece.position.x = int(self.board.width/2 - len(self.piece.matrix[0])/2)
        self.piece.position.y = self.board.height - 1
        
        self.tick_count = 0
        self.round_count = 0
        
    def print(self):
        print('Round count: ', self.round_count)
        print('Tick count: ', self.tick_count)
        
        board_to_print = deepcopy(self.board)
        board_to_print.add_piece(self.piece)
        for i in reversed(range(0, len(board_to_print.matrix))):
            print('|', end = '')
            for j in range(0, len(board_to_print.matrix[0])):
                if board_to_print.matrix[i][j] > 0:
                    print('X', end = '')
                else:
                    print(' ', end = '')
            print('|')
    
    def can_piece_go_further(self):
        new_piece_height = self.piece.position.y - 1
        for board_i in range(new_piece_height, new_piece_height + len(self.piece.matrix)):
            piece_i = board_i - new_piece_height
            for board_j in range(self.piece.position.x, self.piece.position.x + len(self.piece.matrix[0])):
                piece_j = board_j - self.piece.position.x
                if (self.piece.matrix[piece_i][piece_j] == 1 and self.board.matrix[board_i][board_j] == 1) or (new_piece_height < 0):
                    return False
        return True
    
    def is_piece_position_allowed(self, x, y, rotation):
        piece = deepcopy(self.piece)
        piece.position.x = x
        piece.position.y = y
        piece.rotate(rotation)
        
        for board_i in range(piece.position.y, piece.position.y + len(self.piece.matrix)):
            piece_i = board_i - piece.position.y
            for board_j in range(piece.position.x, piece.position.x + len(piece.matrix[0])):
                piece_j = board_j - piece.position.x
                if (piece.matrix[piece_i][piece_j] == 1 and self.board.matrix[board_i][board_j] == 1):
                    return False
                elif piece.position.y < 0:
                    return False
                elif piece.position.x < 0 or piece.position.x + len(piece.matrix[0]) >= self.board.width:
                    return False
        return True
    
    def is_game_over(self):
        for i in reversed(range(0, self.board.height)):
            for j in range(self.board.width):
                if self.board.matrix[i][j] > 0:
                    break
            if j == self.board.width - 1:
                return False
        return True
    
    def rotate_piece(self, rotation):
        # check overflow
        self.piece.rotate(rotation)
        
    def rotate_piece_clockwise(self):
        self.rotate_piece(1)

    def move_piece_down(self):
        if self.piece.position.y > 0:
            self.piece.move_vertically(-1)

    def move_piece_horizontally(self, movement):
        new_x = self.piece.position.x + movement
        if (new_x >= 0 and new_x + len(self.piece.matrix[0]) < self.board.width):
            self.piece.move_horizontally(movement)

    def move_piece_left(self):
        self.move_piece_horizontally(-1)

    def move_piece_right(self):
        self.move_piece_horizontally(1)
    
    def tick(self):
        if self.can_piece_go_further():
            self.piece.move_vertically(-1)
            self.tick_count += 1
        else:
            self.board.add_piece(self.piece)
            
            # pop line if full
            
            self.piece = random.choice(self.pieces)
            self.piece.position.y = self.board.height - 1
            self.piece.position.x = int(self.board.width/2 - len(self.piece.matrix[0])/2)
            
            self.tick_count = 0
            self.round_count += 1