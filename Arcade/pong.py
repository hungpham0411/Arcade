import pygame
import button
import os
import sys
from state import State

BLUE = (0, 0, 102)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_WIDTH = 800
BOARD_HEIGHT = 500
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100

PADDLEINSET = 50
PADDLEWIDTH = 10
PADDLEHEIGHT = 60
BALLSIZE = 10

class Pong(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.load_assets()

        #self.player_win = 0
        #self.computer_win = 0
        #self.draw = 0

    # Draw the Pong board on the game window
    def draw_board(self):
        # Pong visual board
        visual_board = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH/2, self.game.screen_height//2 - BOARD_HEIGHT/2, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.game.screen, BLACK, visual_board)
        
        # Divide line
        divide_line = pygame.Rect(self.game.screen_width//2 + 2.5, self.game.screen_height//2 - BOARD_HEIGHT/2, 5, BOARD_HEIGHT)
        pygame.draw.rect(self.game.screen, WHITE, divide_line)
        
        # Vertical borders
        vertical_line_left = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH/2, self.game.screen_height//2 - BOARD_HEIGHT/2, 6, BOARD_HEIGHT)
        vertical_line_right = pygame.Rect(self.game.screen_width//2 + BOARD_WIDTH/2, self.game.screen_height//2 - BOARD_HEIGHT/2, 6, BOARD_HEIGHT)
        
        # Horizontal borders
        horizontal_line_up = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH/2, self.game.screen_height//2 - BOARD_HEIGHT/2, BOARD_WIDTH, 6)
        horizontal_line_down = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH/2, self.game.screen_height//2 + BOARD_HEIGHT/2, BOARD_WIDTH + 10, 6)
        
        pygame.draw.rect(self.game.screen, WHITE, vertical_line_left)
        pygame.draw.rect(self.game.screen, WHITE, vertical_line_right)
        pygame.draw.rect(self.game.screen, WHITE, horizontal_line_up)
        pygame.draw.rect(self.game.screen, WHITE, horizontal_line_down)
        
        # Paddles
        paddle_left = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH/2 + 50, self.game.screen_height//2 - BOARD_HEIGHT/2 + 50, PADDLEWIDTH, PADDLEHEIGHT)
        paddle_right = pygame.Rect(self.game.screen_width//2 + BOARD_WIDTH/2 - 50, self.game.screen_height//2 - BOARD_HEIGHT/2 + 50, PADDLEWIDTH, PADDLEHEIGHT)
        
        pygame.draw.rect(self.game.screen, WHITE, paddle_left)
        pygame.draw.rect(self.game.screen, WHITE, paddle_right)
        
        # Ball
        pygame.draw.circle(self.game.screen, WHITE, (self.game.screen_width//2 + 5, self.game.screen_height//2), 10)
        
        pygame.display.update()
        
    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.pong_background,(self.game.screen_width, self.game.screen_height)), (0,0))
    
        # Buttons
        back_button = button.Button(self.game.screen_width - BUTTON_WIDTH - 10, 10, 
                                 "Back", self.get_font(17), BLACK, BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Back button to return to the pong difficulty screen
        if back_button.interact_button(self.game.screen) == True:
            self.exit_state()   # Exit the current state which will move to the previous state
            pygame.time.wait(300)
            
        self.draw_board()
            
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
        self.pong_background = pygame.image.load(os.path.join('Assets', 'cyberpunk_background3.jpg'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)