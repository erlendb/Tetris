import numpy
import random
import time
from copy import deepcopy

def _rotate_clockwise(matrix):
    return numpy.rot90(matrix, k = 1, axes = (1, 0))

class Piece():
    def __init__(self, matrix):
        self.matrix = matrix
        self.rotation = 0
    
    # Rotate the piece matrix 'rotation' times clockwise.
    def rotate(self, rotation):
        rotation = rotation % 4
        if rotation < 0:
            rotation += 4
        for i in range(rotation):
            self.matrix = _rotate_clockwise(self.matrix)
            self.rotation += 1

class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[0 for i in range(width)] for j in range(height)]
    
    def erase_line(line):
        self.matrix.pop(line)
        
class Game():
    def _get_board_matrix_with_piece(self):
        matrix = deepcopy(self.board.matrix)
        for _i in range(self.piece.height, self.piece.height + len(self.piece.matrix)):
            i = _i - self.piece.height
            for _j in range(self.piece.position, self.piece.position + len(self.piece.matrix[i])):
                j = _j - self.piece.position
                if self.piece.matrix[i][j] == 1:
                    matrix[_i][j] = 1
        return matrix
        
    def _print(self):
        matrix = self._get_board_matrix_with_piece()
        for i in reversed(range(0, len(matrix))):
            print('| ', end = '')
            for j in range(0, len(matrix[0])):
                if matrix[i][j] > 0:
                    print('X', end = '')
                else:
                    print(' ', end = '')
            print(' |')
    
    def __init__(self):
        self.board = Board(10, 20)
        
        self.pieces = []
        self.pieces.append(Piece([[1, 1, 1, 1]]))
        self.pieces.append(Piece([[1, 0, 0], [1, 1, 1]]))
        self.pieces.append(Piece([[0, 0, 1], [1, 1, 1]]))
        self.pieces.append(Piece([[1, 1],    [1, 1]]))
        self.pieces.append(Piece([[0, 1, 1], [1, 1, 0]]))
        self.pieces.append(Piece([[0, 1, 0],  [1, 1, 1]]))
        self.pieces.append(Piece([[1, 1, 0], [0, 1, 1]]))
        
    def play(self):
        self.piece = self.pieces[0]
        self.piece.position = int(self.board.width/2)
        self.piece.height = self.board.height
        
        i = 0
        start_time = time.time()
        while (True):
            if time.time() > start_time + i:
                i += 1
                
                self.piece.height -= 1
                
                print()
                print(i)
                self._print()
            
            # Check for crash
                #self.next_piece = random.choice(self.pieces)
                #self.current_piece_height = self.board.height
            
            