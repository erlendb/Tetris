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
        self.rotated_matrices.append(numpy.rot90(matrix, k = 1, axes = (1, 0)))
        self.rotated_matrices.append(numpy.rot90(matrix, k = 2, axes = (1, 0)))
        self.rotated_matrices.append(numpy.rot90(matrix, k = 3, axes = (1, 0)))
        
        self.rotation = 0
        self.position = Position()
    
    def rotate(self, rotation):
        self.rotation = (self.rotation + rotation) % 4
        while self.rotation < 0:
            self.rotation += 4
        self.matrix = self.rotated_matrices[self.rotation]
    
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
            piece_i = -1 - (board_i - piece.position.y)
            for board_j in range(piece.position.x, piece.position.x + len(piece.matrix[0])):
                piece_j = (board_j - piece.position.x)
                if piece.matrix[piece_i][piece_j] == 1:
                    self.matrix[board_i][board_j] = 1
    
    def pop_line(self, line):
        self.matrix.pop(line)
        self.matrix.append([0 for i in range(self.width)])
        
class Game():
    def __init__(self, board_width = 10, board_height = 20, pieces = None):
        if pieces is None:
            self.pieces = []
            self.pieces.append(Piece([[1, 1, 1, 1]]))
            self.pieces.append(Piece([[1, 0, 0], [1, 1, 1]]))
            self.pieces.append(Piece([[0, 0, 1], [1, 1, 1]]))
            self.pieces.append(Piece([[1, 1],    [1, 1]]))
            self.pieces.append(Piece([[0, 1, 1], [1, 1, 0]]))
            self.pieces.append(Piece([[0, 1, 0], [1, 1, 1]]))
            self.pieces.append(Piece([[1, 1, 0], [0, 1, 1]]))
        else:
            self.pieces = []
            for i in range(0, len(pieces)):
                self.pieces.append(Piece(pieces[i]))
                
        self.board = Board(board_width, board_height)
        
        self.set_piece(random.randrange(len(self.pieces)))
        self.reset_piece_position()
        self.set_next_piece_id(random.randrange(len(self.pieces)))
        
        self.tick_count = 0
        self.round_count = 0
        
    def print(self):
        print('\n\nRound count: ', self.round_count)
        print('Tick count: ', self.tick_count)
        
        print('\nNext piece:')
        next_piece = self.pieces[self.next_piece_id]
        for i in range(0, len(next_piece.matrix)):
            for j in range(0, len(next_piece.matrix[0])):
                if next_piece.matrix[i][j] == 1:
                    print('X', end = '')
                else:
                    print(' ', end = '')
            print()
        print()
        
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
    
    def is_piece_position_allowed(self, x = None, y = None, rotation = None):
        piece = deepcopy(self.piece)
        if x is not None:
            piece.position.x = x
        if y is not None:
            piece.position.y = y
        if rotation is not None:
            piece.rotate(rotation)
        
        for board_i in range(piece.position.y, min(self.board.height, piece.position.y + len(piece.matrix))):
            piece_i = -1 - (board_i - piece.position.y)
            for board_j in range(piece.position.x, piece.position.x + len(piece.matrix[0])):
                piece_j = board_j - piece.position.x
                if piece.position.y < 0:
                    return False
                elif piece.position.x < 0 or piece.position.x + len(piece.matrix[0]) - 1 >= self.board.width:
                    return False
                elif (piece.matrix[piece_i][piece_j] == 1 and self.board.matrix[board_i][board_j] == 1):
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
    
    def pop_full_lines(self):
        for i in range(self.board.height):
            line_is_full = True
            for j in range(self.board.width):
                if self.board.matrix[i][j] == 0:
                    line_is_full = False
                    break
            if line_is_full:
                self.board.pop_line(i)
            
    def tick(self):
        if self.is_piece_position_allowed(y = self.piece.position.y - 1):
            self.move_piece_down()
            self.tick_count += 1
        else:
            self.board.add_piece(self.piece)
            
            self.pop_full_lines()
            
            self.set_piece(self.next_piece_id)
            self.reset_piece_position()
            self.set_next_piece_id(random.randint(0, len(self.pieces)))
            
            self.tick_count = 0
            self.round_count += 1
    
    def get_tick_count(self):
        return self.tick_count
    
    def get_round_count(self):
        return self.round_count
    
    def get_board(self):
        return self.board.matrix
    
    def get_piece(self):
        return self.piece.matrix
    
    def get_board_with_piece(self):
        # merge them and return matrix
        pass
    
    def get_piece_position(self):
        return self.piece.position.x, self.piece.position.y
    
    def set_piece_position(self, x, y):
        if self.is_piece_position_allowed(x = x, y = y):
            self.piece.position.x = x
            self.piece.position.y = y
    
    def set_piece(self, piece_id):
        if piece_id >= 0 and piece_id < len(self.pieces):
            self.piece = deepcopy(self.pieces[piece_id])
    
    def set_next_piece_id(self, piece_id):
        if piece_id >= 0 and piece_id < len(self.pieces):
            self.next_piece_id = piece_id
    
    def reset_piece_position(self):
        self.set_piece_position(x = int(self.board.width/2 - len(self.piece.matrix[0])/2), y = self.board.height - 1)
    
    def rotate_piece(self, rotation):
        if self.is_piece_position_allowed(rotation = rotation):
            self.piece.rotate(rotation)
        
    def rotate_piece_clockwise(self):
        self.rotate_piece(1)

    def move_piece_down(self):
        if self.is_piece_position_allowed(y = self.piece.position.y - 1):
            self.piece.move_vertically(-1)
        
    def move_piece_down_until_not_allowed(self):
        while self.is_piece_position_allowed(y = self.piece.position.y - 1):
            self.piece.move_vertically(-1)

    def move_piece_horizontally(self, movement):
        if self.is_piece_position_allowed(x = self.piece.position.x + movement):
            self.piece.move_horizontally(movement)

    def move_piece_left(self):
        self.move_piece_horizontally(-1)

    def move_piece_right(self):
        self.move_piece_horizontally(1)