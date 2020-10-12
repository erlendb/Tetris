import tetris
import time
import keyboard

game = tetris.Game()
start_time = time.time()
i = 0

def key_press_handler(event):
    if event.name == 'left':
        game.move_piece_left()
    elif event.name == 'right':
        game.move_piece_right()
    elif event.name == 'up':
        game.rotate_piece_clockwise()
keyboard.on_press(key_press_handler)

while not game.is_game_over():
    if time.time() > start_time + i:
        i += 1
        game.tick()
        game.print()