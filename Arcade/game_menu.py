import pygame
import button
import os
import sys
from state import State
from gamehub import Gamehub

PURPLE = (204, 26, 255)
GREEN = (5, 187, 170)
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70

class GameMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.game_menu_background,(self.game.screen_width, self.game.screen_height)), (0,0))
        self.game.screen.blit(self.title, (self.game.screen_width//2 - self.title.get_width()//2, 100))
            
        # Buttons
        start_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2, 
                                    "START", self.get_font(40), PURPLE, GREEN, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        settings_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 100, 
                                    "SETTINGS", self.get_font(40), PURPLE, GREEN, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        exit_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 200, 
                                    "EXIT", self.get_font(40), PURPLE, GREEN, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Choose Start
        if start_button.interact_button() == True:
            self.game.screen.fill((0,0,0))
            new_state = Gamehub(self.game) # Create the Gamehub state
            new_state.enter_state()
            pygame.display.update()
            pygame.time.wait(300)

        # Choose Settings
        if settings_button.interact_button() == True:
            pass

        # Exit button to exit the game
        if exit_button.interact_button() == True:
            pygame.quit()
            sys.exit()

        pygame.display.update()
            
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def load_assets(self):
        self.game_menu_background = pygame.image.load(os.path.join('Assets', 'retro_background.jpg'))
        self.title = pygame.image.load(os.path.join('Assets', 'title.png'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font2.ttf'), size)


