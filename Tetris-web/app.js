/// Game data
var game_data_starts_at_line = 5;

var lines = data1_game.split('\n');
var game_info = []
for (var i = game_data_starts_at_line; i < lines.length; i++) {
  var data = lines[i].split(' ');
  var rounds = data[1];
  var score = data[2];
  var epsilon = data[3];
  var cl = data[4];
  game_info.push([rounds, score, epsilon, cl]);
}
///

/// Moves
var moves_data_starts_at_line = 4;

var lines = data1_moves.split('\n');
var games = [];
for (var i = moves_data_starts_at_line; i < lines.length; i++) {
  var data = lines[i].split(' ');
  var moves = [];
  for (var j = 1; j < data.length; j++) {
    var move = data[j].split(',');
    var piece_id = parseInt(move[0]);
    var x = parseInt(move[1]);
    var y = parseInt(move[2]);
    var rotation = parseInt(move[3]);
    
    moves.push([piece_id, x, y, rotation]);
  }
  games.push(moves);
}
///

var game_iterator = 0;
var new_game_iterator = -1;
var sleep_time = 500;

async function run() {
  while (game_iterator < games.length) {
    show_game_number(game_iterator);
    show_game_info(game_iterator);
    round_iterator = 0;
    game = new Game();
    while (round_iterator < games[game_iterator].length - 1 && new_game_iterator == -1) {
      show_round_number(round_iterator);
      var move = games[game_iterator][round_iterator];
      var piece_id = move[0];
      var x = move[1];
      var y = move[2];
      var rotation = move[3];
      game.set_piece(piece_id);
      game.piece.set_rotation(rotation);
      game.piece.set_position(x, y);
      game.add_piece();

      $('#boardContainer').html(game.get_html());
      game.pop_full_lines();
      await sleep(sleep_time/2);
      $('#boardContainer').html(game.get_html());
      await sleep(sleep_time/2);
      
      round_iterator++;
    }
    if (new_game_iterator == -1) {
      game_iterator++;
    } else {
      game_iterator = new_game_iterator;
      new_game_iterator = -1;
    }
    if (game_iterator >= games.length || game_iterator < 0) {
      game_iterator = 0;
    }
  }
}

$('#setGameSubmit').click(function(e) {
  var game_number = parseInt($('[name="setGame"]').val())
  if (game_number >= 0 && game_number <= 9999) {
    set_game(game_number);
  } else {
    $('[name="setGame"]').val(game_iterator);
  }
});

$('#setSleepSubmit').click(function(e) {
  var sleep = parseInt($('[name="setSleep"]').val())
  set_sleep_time(sleep);
});

function set_game(game) {
  new_game_iterator = game;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function show_game_number(game_number) {
  $('#gameNumber').html(game_number);
}

function show_game_info(game_number) {
  var rounds = game_info[game_number][0];
  var score = game_info[game_number][1];
  var epsilon = game_info[game_number][2];
  var cl = game_info[game_number][3];
  $('#rounds').html(rounds);
  $('#score').html(score);
  $('#epsilon').html(epsilon);
  $('#cl').html(cl);
}

function show_round_number(round_number) {
  $('#roundNumber').html(round_number);
}

function set_sleep_time(time) {
  sleep_time = time;
}

run();