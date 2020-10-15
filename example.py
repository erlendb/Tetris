import tetris
import time
import keyboard

def key_press_handler(event):
    if event.name == 'left':
        game.move_piece_left()
    elif event.name == 'right':
        game.move_piece_right()
    elif event.name == 'up':
        game.rotate_piece_clockwise()
    elif event.name == 'down':
        game.move_piece_down()
    elif event.name == 'space':
        game.move_piece_down_until_not_allowed()
keyboard.on_press(key_press_handler)

game = tetris.Game()

start_time = time.time()
i = 0
while not game.is_game_over():
    if time.time() > start_time + i:
        i += 1
        game.tick()
        game.print()

game.print()
print('Game over')