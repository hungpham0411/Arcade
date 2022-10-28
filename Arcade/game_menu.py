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
        self.game.screen.blit(pygame.transform.scale(self.background,(self.game.screen_width, self.game.screen_height)), (0,0))
        self.game.screen.blit(self.title, (self.game.screen_width//2 - self.title.get_width()//2, 100))
            
        # Buttons
        start_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2, 
                                    "START", self.get_font(40), PURPLE, GREEN, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        settings_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 100, 
                                    "SETTINGS", self.get_font(40), PURPLE, GREEN, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        exit_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 200, 
                                    "EXIT", self.get_font(40), PURPLE, GREEN, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Check if the button is clicked, and what happens when it is clicked
        if start_button.draw_button(self.game.screen) == True:
            new_state = Gamehub(self.game) # Create the Gamehub state
            new_state.enter_state()
            self.game.screen.fill((0,0,0))
            pygame.display.update()
            pygame.time.wait(300)
        if settings_button.draw_button(self.game.screen) == True:
            pass
        if exit_button.draw_button(self.game.screen) == True:
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
        self.background = pygame.image.load(os.path.join('Assets', 'retro_background.jpg'))
        self.title = pygame.image.load(os.path.join('Assets', 'title.png'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font2.ttf'), size)


