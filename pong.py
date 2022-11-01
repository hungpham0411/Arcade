# code sourced from pong pygame tutorial: https://ryanstutorials.net/pygame-tutorial/pygame-pong-simple.php

import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)
ELEMENTCOLOUR = (100, 100, 100)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pong!')

# Game Element Variables
PADDLEINSET = 20
PADDLEWIDTH = 10
PADDLEHEIGHT = 60
BALLSIZE = 10
 
# The main function that controls the game
def main () :
  looping = True
  
  leftPaddleY = 50
  rightPaddleY = 50
  ballX = WINDOW_WIDTH // 2
  ballY = WINDOW_HEIGHT // 2
  ballXMomentum = 1
  ballYMomentum = 1

  # The main game loop
  while looping :
    # Get inputs
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
    
    pressed = pygame.key.get_pressed()
    if (pressed[K_w]) :
      leftPaddleY -= 2
    elif (pressed[K_s]) :
      leftPaddleY += 2
    if (pressed[K_UP]) :
      leftPaddleY -= 2
    elif (pressed[K_DOWN]) :
      leftPaddleY += 2

    # Processing

    if leftPaddleY < 0 :
      leftPaddleY = 0
    if leftPaddleY > WINDOW_HEIGHT - PADDLEHEIGHT :
      leftPaddleY = WINDOW_HEIGHT - PADDLEHEIGHT
    if rightPaddleY < 0 :
      rightPaddleY = 0
    if rightPaddleY > WINDOW_HEIGHT - PADDLEHEIGHT :
      rightPaddleY = WINDOW_HEIGHT - PADDLEHEIGHT

    if ballY < BALLSIZE : # ball has hit the top
      ballYMomentum = 1
    if ballY > WINDOW_HEIGHT - BALLSIZE : # ball has hit the bottom
      ballYMomentum = -1

    if ballX <= BALLSIZE : # Left player loses
      ballX = WINDOW_WIDTH // 2
      ballY = WINDOW_HEIGHT // 2
      ballYMomentum = 1
      ballXMomentum = 1
    if ballX >= WINDOW_WIDTH - BALLSIZE : # Right player loses
      ballX = WINDOW_WIDTH // 2
      ballY = WINDOW_HEIGHT // 2
      ballYMomentum = 1
      ballXMomentum = -1

    if ballX <= PADDLEINSET + PADDLEWIDTH and ballX > PADDLEINSET : # work out if left paddle has hit the ball
      if leftPaddleY < ballY and leftPaddleY + PADDLEHEIGHT > ballY :
        ballXMomentum = 1
    if ballX >= WINDOW_WIDTH - PADDLEINSET - PADDLEWIDTH and ballX < WINDOW_WIDTH - PADDLEINSET : # work out if right paddle has hit the ball
      if rightPaddleY < ballY and rightPaddleY + PADDLEHEIGHT > ballY :
        ballXMomentum = -1

    leftPaddleRect = pygame.Rect(PADDLEINSET, leftPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
    rightPaddleRect = pygame.Rect(WINDOW_WIDTH - PADDLEINSET - PADDLEWIDTH, rightPaddleY, PADDLEWIDTH, PADDLEHEIGHT)
 
    ballX = ballX + ballXMomentum
    ballY = ballY + ballYMomentum

    # Render elements of the game

    WINDOW.fill(BACKGROUND)
    pygame.draw.line(WINDOW, ELEMENTCOLOUR, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 2)
    pygame.draw.rect(WINDOW, ELEMENTCOLOUR, leftPaddleRect)
    pygame.draw.rect(WINDOW, ELEMENTCOLOUR, rightPaddleRect)
    pygame.draw.circle(WINDOW, ELEMENTCOLOUR, (int(ballX), int(ballY)), BALLSIZE)
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()