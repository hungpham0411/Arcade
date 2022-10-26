import pygame
from pygame.locals import *
from cpu import findBestMove

pygame.init()

screen_width = 600
screen_height = 600
screen_color = (0,150,255)

screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(screen_color)
pygame.display.set_caption('Tic Tac Toe')

main_rec_color = (255,255,255)
pygame.draw.rect(screen, main_rec_color, pygame.Rect(100,100,400,400))

##title_rec_color = (255,255,255)
##pygame.draw.rect(screen, title_rec_color, pygame.Rect(100,10,400,50))

font = pygame.font.Font('freesansbold.ttf', 32)
title = font.render('Tic Tac Toe', True, (0,0,0), (255,255,255))
title_rect = title.get_rect()
title_rect.center = (300,50)

screen.blit(title, title_rect)

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