import tetris
import time
import keyboard

def key_press_handler(event):
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
print('\nGame over, your final score was', game.get_score())

input("Press enter key to continue")
