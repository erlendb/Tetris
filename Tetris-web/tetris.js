var pieces = [];
var pieces_rotated = [];
pieces.push([[1, 1, 1, 1]]);
pieces_rotated.push([
  [[1, 1, 1, 1]],
  [[1], [1], [1], [1]],
  [[1, 1, 1, 1]],
  [[1], [1], [1], [1]]
]);
pieces.push([[1, 0, 0], [1, 1, 1]]);
pieces_rotated.push([
  [[1, 0, 0], [1, 1, 1]],
  [[1, 1], [1, 0], [1, 0]],
  [[1, 1, 1], [0, 0, 1]],
  [[0, 1], [0, 1], [1, 1]]
]);
pieces.push([[0, 0, 1], [1, 1, 1]]);
pieces_rotated.push([
  [[0, 0, 1], [1, 1, 1]],
  [[1, 0], [1, 0], [1, 1]],
  [[1, 1, 1], [1, 0, 0]],
  [[1, 1], [0, 1], [0, 1]]
]);
pieces.push([[1, 1], [1, 1]]);
pieces_rotated.push([
  [[1, 1], [1, 1]],
  [[1, 1], [1, 1]],
  [[1, 1], [1, 1]],
  [[1, 1], [1, 1]]
]);
pieces.push([[0, 1, 1], [1, 1, 0]]);
pieces_rotated.push([
  [[0, 1, 1], [1, 1, 0]],
  [[1, 0], [1, 1], [0, 1]],
  [[0, 1, 1], [1, 1, 0]],
  [[1, 0], [1, 1], [0, 1]]
]);
pieces.push([[0, 1, 0], [1, 1, 1]]);
pieces_rotated.push([
  [[0, 1, 0], [1, 1, 1]],
  [[1, 0], [1, 1], [1, 0]],
  [[1, 1, 1], [0, 1, 0]],
  [[0, 1], [1, 1], [0, 1]]
]);
pieces.push([[1, 1, 0], [0, 1, 1]]);
pieces_rotated.push([
  [[1, 1, 0], [0, 1, 1]],
  [[0, 1], [1, 1], [1, 0]],
  [[1, 1, 0], [0, 1, 1]],
  [[0, 1], [1, 1], [1, 0]]
]);


class Position {
  constructor(x = -1, y = -1) {
    this.x = x;
    this.y = y;
  }
}

class Piece {
  constructor(matrix, type, rotated_matrices) {
    this.matrix = matrix;
    this.type = type;
    this.rotated_matrices = rotated_matrices;
    
    this.rotation = 0;
    this.position = new Position(-1, -1);
  }
  
  set_rotation(rotation) {
    this.rotation = rotation % 4;
    while (this.rotation < 0) {
      this.rotation += 4;
    }
    this.matrix = this.rotated_matrices[this.rotation];
  }
  
  set_position(x, y) {
    this.position.x = x;
    this.position.y = y;
  }
}

class Board {
  constructor(width, height) {
    this.width = width;
    this.height = height;
    this.matrix = new Array(this.height);
    for (var i = 0; i < this.height; i++) {
      this.matrix[i] = new Array(this.width).fill(0);
    }
  }
  
  make_binary() {
    for (var j = 0; j < this.width; j++) {
      for (var i = 0; i < this.height; i++) {
        if (this.matrix[i][j] > 0) {
          this.matrix[i][j] = 1;
        }
      }
    }
  }
  
  add_piece(piece) {
    this.make_binary();
        
    for (var board_i = piece.position.y; board_i < Math.min(this.height, piece.position.y + piece.matrix.length); board_i++) {
      var piece_i = piece.matrix.length - 1 - (board_i - piece.position.y);//-1 - (board_i - piece.position.y);
      for (var board_j = piece.position.x; board_j < piece.position.x + piece.matrix[0].length; board_j++) {
        var piece_j = (board_j - piece.position.x);
        if (piece.matrix[piece_i][piece_j] > 0) {
          this.matrix[board_i][board_j] = 2;
        }
      }
    }
  }
  
  pop_line(line) {
    this.matrix.splice(line, 1);
    this.matrix.push(new Array(this.width).fill(0));
  }
}

class Game {
  constructor(board_width = 10, board_height = 20) {
    this.pieces = []
    for (var i = 0; i < pieces.length; i++) {
      this.pieces.push(new Piece(pieces[i], i, pieces_rotated[i]));
    }
    
    this.board = new Board(board_width, board_height);
  }
  
  pop_full_lines() {
    for (var i = this.board.height - 1; i >= 0; i--) {
      var line_is_full = true;
      for (var j = 0; j < this.board.width; j++) {
        if (this.board.matrix[i][j] == 0) {
          var line_is_full = false;
          break;
        }
      }
      if (line_is_full) {
        this.board.pop_line(i);
      }
    }
  }
  
  set_piece(piece_id) {
    this.piece = new Piece(pieces[piece_id], piece_id, pieces_rotated[piece_id]);
  }
  
  set_next_piece(piece_id) {
    this.next_piece = new Piece(pieces[piece_id], piece_id, pieces_rotated[piece_id]);
  }
  /*
  tick() {
    //this.board.add_piece(this.piece);
    //this.pop_full_lines();
  }*/
  
  add_piece() {
    this.board.add_piece(this.piece);
  }
  
  get_html() {
    var html = '';
    html += '<div class="board">';
    for (var i = this.board.matrix.length - 1; i >= 0; i--) {
      html += '<div class="line">';
      for (var j = 0; j < this.board.matrix[0].length; j++) {
        html += '<div class="pixel" value=';
        html += this.board.matrix[i][j];
        html += '>';
        html += '</div>';
      }
      html += '</div>';
    }
    html += '</div>';
    return html;
  }
}