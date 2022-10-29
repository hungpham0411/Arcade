import pygame
import button
import os
import sys
from state import State
from tictactoe import Tictactoe

LIGHT_BLUE = (26, 26, 179)
NEON = (1, 255, 244)
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70

class Gamehub(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.gamehub_background,(self.game.screen_width, self.game.screen_height)), (0,0))

        # Buttons
        tictactoe_button = button.Button(self.game.screen_width//4 - BUTTON_WIDTH//2, self.game.screen_height//2, 
                                         "Tic Tac Toe", self.get_font(35), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        connectfour_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2, 
                                           "Connect Four", self.get_font(35), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        checkers_button = button.Button(3*(self.game.screen_width//4) - BUTTON_WIDTH//2, self.game.screen_height//2, 
                                        "Checkers", self.get_font(35), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        pong_button = button.Button(self.game.screen_width//4 - BUTTON_WIDTH//2, self.game.screen_height//2 + 100, 
                                    "Pong", self.get_font(35), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        battleship_button = button.Button(self.game.screen_width//2 - BUTTON_WIDTH//2, self.game.screen_height//2 + 100, 
                                          "Battleship", self.get_font(35), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        back_button = button.Button(3*(self.game.screen_width//4) - BUTTON_WIDTH//2, self.game.screen_height//2 + 100, 
                                    "Back", self.get_font(35), LIGHT_BLUE, NEON, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Check if the button is clicked, and what happens when it is clicked
        if tictactoe_button.draw_button(self.game.screen) == True:
            new_state = Tictactoe(self.game, 'X') # Create the Tictactoe state
            new_state.enter_state()
            self.game.screen.fill((0,0,0))
            pygame.display.update()
            pygame.time.wait(300)
            
        if connectfour_button.draw_button(self.game.screen) == True:
            pass
        
        if checkers_button.draw_button(self.game.screen) == True:
            pass
        
        if pong_button.draw_button(self.game.screen) == True:
            pass
        
        if battleship_button.draw_button(self.game.screen) == True:
            pass
        
        if back_button.draw_button(self.game.screen) == True:
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()
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
        self.gamehub_background = pygame.image.load(os.path.join('Assets', 'retro_background1.jpg'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font2.ttf'), size)
            


