import pygame
from pygame.locals import *
from cpu import findBestMove

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))

# 
board = [
    [ '_', '_', '_' ],
    [ '_', '_', '_' ],_
    [ '_', '_', '_' ]
]

game = True
while game:

    for event in pygame.event.get():
        if event.type == pygame.quit:
            game = False

    pygame.display.update()

pygame.quit()