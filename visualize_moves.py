import tetris
import keyboard
import time

### Change these settings before running main.py
load_moves_log = '1605965316.591669test-etter-halvferdig-runde4-moves.txt'
start_at_game = 0
time_limit_round = 1 # Seconds between each piece placement. -1 if you want to tick with pressing the space button
time_limit_game = 2 # Seconds from game over to new game. -1 if you want to go to next game by pressing the space button
###

data_starts_at_line = 4

moves_file = 'logs/' + load_moves_log
file = open(moves_file, 'r')
lines = file.readlines()
file.close()

data = []
for index, line in enumerate(lines):
    if index < data_starts_at_line - 1 + start_at_game:
        continue
    data.append(line.split())

#print(data)

games = []

for i, game in enumerate(data):
        
    moves = []
    for j, move in enumerate(game):
        if j == 0:
            continue
        moves.append(move.split(','))
    games.append(moves)

#print(games)

go_further_flag = False
prev_time = time.time()

def should_go_further(time_limit=-1):
    global go_further_flag
    global prev_time
    
    if time_limit != -1:
        while not time.time() - prev_time > time_limit:
            pass
        prev_time = time.time()
        return True
    
    prev_time = time.time()
    if not go_further_flag:
        return False
    go_further_flag = False
    return True

def key_press_handler(event):
    global go_further_flag
    if event.name == 'space':
        go_further_flag = True
keyboard.on_press(key_press_handler)

i = 0
while not i > len(games):
    game = tetris.Game()
    game.board.better_visualization = True
    j = 0
    while j < len(games[i]):
        while not should_go_further(time_limit=time_limit_round):
            pass
        print()
        print('Game number: ', start_at_game + i)
        print('Move number: ', j)
        move = games[i][j]
        piece_type = int(move[0])
        y = int(move[2])
        x = int(move[1])
        rotation = int(move[3])
        
        next_piece_type = 0
        if j + 1 < len(games[i]):
            next_piece_type = int(games[i][j+1][0])
        
        game.piece = game.pieces[piece_type]
        game.set_next_piece_id(next_piece_type)
        game.piece.set_rotation(rotation)
        game.piece.set_position(x, y)
        
        game.print()
        game.tick()
        j += 1
    i += 1
    while not should_go_further(time_limit=time_limit_game):
        pass
