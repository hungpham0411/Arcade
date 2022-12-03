import pygame
import button
import os
import sys
from state import State
from pong import Pong

LIGHT_BLUE = (26, 26, 179)
NEON = (1, 255, 244)
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70

class Pong_Difficulty_Screen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.pong_difficulty_screen_background,(self.game.screen_width, self.game.screen_height)), (0,0)) 
        
        # Buttons
        normal_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2, 
                                    "NORMAL", self.get_font(40), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        hard_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 100, 
                                    "HARD", self.get_font(40), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        back_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 200, 
                                    "BACK", self.get_font(40), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Choose the Normal mode
        if normal_button.interact_button() == True:
            new_state = Pong(self.game, 'normal') # Create the Pong state with normal AI
            new_state.enter_state()
            pygame.time.wait(300)

        # Choose the Hard mode
        if hard_button.interact_button() == True:
            new_state = Pong(self.game, 'hard') # Create the Pong state with hard AI 
            new_state.enter_state()
            pygame.time.wait(300)

        # Back button to return to the game hub screen
        if back_button.interact_button() == True:
            self.exit_state()   # Exit the current state which will move to the previous state
            pygame.time.wait(300)

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
        self.pong_difficulty_screen_background = pygame.image.load(os.path.join('Assets', 'cyberpunk_background3.jpg'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font2.ttf'), size)