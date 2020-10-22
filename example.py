import tetris
import time
import keyboard
import pygame

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


# Initialize the game engine
pygame.init()

# Constants

# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

pygame.init()
pygame.display.set_caption("Tetris")


SQUARE_SIZE = 50
BOARD_WIDTH = 10
BOARD_HEIGHT = 15

game = tetris.Game(BOARD_WIDTH, BOARD_HEIGHT)
display_size = [SQUARE_SIZE * BOARD_WIDTH, SQUARE_SIZE * BOARD_HEIGHT]

# Set up the drawing window
screen = pygame.display.set_mode(display_size)

start_time = time.time()
i = 0
while not game.is_game_over():

    for event in pygame.event.get():
        # Handle window closing
        if event.type == pygame.QUIT:
            game.set_game_over(True)

        # Handle button presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # For debugging, only update gamestate when pressing 'q'
                game.tick()
                game.print()

    # Fill the background with white
    screen.fill(pygame.Color('white'))

    # Draw the board
    for i, row in enumerate(game.board.matrix):
        for j, square in enumerate(row):
            if square:
                pygame.draw.rect(screen, BLUE, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw to screen
    pygame.display.flip()

pygame.quit()
game.print()
print('\nGame over, your final score was', game.score)

input("Press enter to continue")



#     if time.time() > start_time + i:
#         i += 1
#         game.tick()
#         game.print()


