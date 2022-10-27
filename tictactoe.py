import pygame
from pygame.locals import *
from cpu import findBestMove

pygame.init()

screen_width = 1191
screen_height = 670

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

retro_background = pygame.image.load("C:/Users/Connor/Desktop/Skool/Fall 2022/Software Engineering/team-4-arcade-project-cs-490/retroback.jpg").convert()
screen.blit(retro_background, (0,0))

# '_' = available move
# 'X' = player
# 'O' = opponent
# to get cpu move, call cpu.findBestMove(board)
# will return bestMove(row, column)
board = [
    [ '_', '_', '_' ],
    [ '_', '_', '_' ],
    [ '_', '_', '_' ]
]

game = True
while game:
    
    for event in pygame.event.get():
        if event.type == pygame.quit:
            game = False

    pygame.display.update()

pygame.quit()