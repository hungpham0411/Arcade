import pygame
import button
import os
import sys

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
PURPLE = (204, 26, 255)
GREEN = (5, 187, 170)
BACKGROUND = pygame.image.load(os.path.join('Assets', 'retro_background.jpg'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
GAMEHUB_BACKGROUND = pygame.image.load(os.path.join('Assets', 'retro_background1.jpg'))
GAMEHUB_BACKGROUND = pygame.transform.scale(GAMEHUB_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

TITLE = pygame.image.load(os.path.join('Assets', 'title.png'))
START_ICON = pygame.image.load(os.path.join('Assets', 'button_start.png'))
SETTINGS_ICON = pygame.image.load(os.path.join('Assets', 'button_settings.png'))
EXIT_ICON = pygame.image.load(os.path.join('Assets', 'button_exit.png'))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Arcade')

start_rect = pygame.Rect(SCREEN_WIDTH//2 - button.BUTTON_WIDTH//2, SCREEN_HEIGHT//2, button.BUTTON_WIDTH, button.BUTTON_HEIGHT)
settings_rect = pygame.Rect(SCREEN_WIDTH//2 - button.BUTTON_WIDTH//2, SCREEN_HEIGHT//2 + 100, button.BUTTON_WIDTH, button.BUTTON_HEIGHT)
exit_rect = pygame.Rect(SCREEN_WIDTH//2 - button.BUTTON_WIDTH//2, SCREEN_HEIGHT//2 + 200, button.BUTTON_WIDTH, button.BUTTON_HEIGHT)

clock = pygame.time.Clock()

def get_font(size):
    return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)

def draw_window():
    screen.blit(BACKGROUND, (0,0))
    screen.blit(TITLE, (SCREEN_WIDTH//2 - TITLE.get_width()//2, 100))

def start():
    screen.blit(GAMEHUB_BACKGROUND, (0,0))

    tictactoe_button = button.Button(SCREEN_WIDTH//2 - button.BUTTON_WIDTH//2, start_rect.y, "Tic Tac Toe", get_font(20), PURPLE, GREEN, screen)
    connectfour_button = button.Button(3*(SCREEN_WIDTH//4) - button.BUTTON_WIDTH//2, start_rect.y, "Connect Four", get_font(20), PURPLE, GREEN, screen)
    checkers_button = button.Button(SCREEN_WIDTH//4 - button.BUTTON_WIDTH//2, start_rect.y, "Checkers", get_font(20), PURPLE, GREEN, screen)
    pong_button = button.Button(SCREEN_WIDTH//4 - button.BUTTON_WIDTH//2, start_rect.y + 100, "Pong", get_font(20), PURPLE, GREEN, screen)
    battleship_button = button.Button(SCREEN_WIDTH//2 - button.BUTTON_WIDTH//2, start_rect.y + 100, "Back", get_font(20), PURPLE, GREEN, screen)

    if tictactoe_button.draw_button(screen) == True:
        pass
    if connectfour_button.draw_button(screen) == True:
        pass
    if checkers_button.draw_button(screen) == True:
        pass
    if pong_button.draw_button(screen) == True:
        pass
    if battleship_button.draw_button(screen) == True:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    pygame.display.update()

def settings():
    pass

def main():
    run = True
    while run:

        draw_window()

        #draw buttons
        start_button = button.Button(start_rect.x, start_rect.y, "START", get_font(25), PURPLE, GREEN, screen)
        settings_button = button.Button(settings_rect.x, settings_rect.y, "SETTINGS", get_font(25), PURPLE, GREEN, screen)
        exit_button = button.Button(exit_rect.x, exit_rect.y, "EXIT", get_font(25), PURPLE, GREEN, screen)

        #check if the buttons were clicked
        if start_button.draw_button(screen) == True:
            start()
        if settings_button.draw_button(screen) == True:
            pass
        if exit_button.draw_button(screen) == True:
            #run = False
            pygame.quit()
            sys.exit()
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(START_ICON.get_width())
            if event.type == pygame.QUIT:
                #run = False
                pygame.quit()
                sys.exit()
                
        clock.tick(FPS)
        pygame.display.update()

        

#main()
    

