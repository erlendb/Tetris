import tetris
import time
import keyboard
import time
timestamp = str(time.time())

moves_file_name = 'test1'

moves = []

def save_moves():
    global moves
    global moves_file_name
    log_file = 'logs/moves-' + moves_file_name + '.txt'
    with open(log_file, 'a') as log:
        for move in moves:
            piece_type = move[0]
            x = move[1]
            y = move[2]
            rotation = move[3]
            log.write(f"{piece_type},{x},{y},{rotation} ")
        log.write("\n")

def key_press_handler(event):
    global moves
    if event.name == 'left':
        game.move_piece_horizontally(-1)
    elif event.name == 'right':
        game.move_piece_horizontally(1)
    elif event.name == 'up':
        game.rotate_piece(1)
    elif event.name == 'down':
        game.move_piece_down()
    elif event.name == 'space':
        game.move_piece_down_until_not_allowed()
        moves.append([game.piece.type, game.piece.position.x, game.piece.position.y, game.piece.rotation])
        game.tick()
    game.print()
keyboard.on_press(key_press_handler)

game = tetris.Game()

while not game.is_game_over():
    pass

save_moves()

game.print()
print('\nGame over, your final score was', game.get_score())

input("Press enter key to continue")
