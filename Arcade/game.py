import pygame
from game_menu import GameMenu
import tictactoe
import pong
import battleship
import checkers

FPS = 60

class Game():
    def __init__(self):
        pygame.init()
        #Screen resolution
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running, self.playing = True, True
        
        # Contain the states and load them
        self.state_stack = [] 
        self.load_states()
        
        pygame.display.set_caption('Arcade')
        self.clock = pygame.time.Clock()
        
        # Tic-tac-toe
        self.tictactoe_game_over = False
        self.tictactoe_max_depth_AI = 0

        # Pong
        self.pong_game_over = False
        self.pong_mode = None
        
        # Battleship
        self.battleship_game_over = False
        self.battleship_mode = None
        
        # Checkers
        self.checkers_game_over = False
        self.checkers_max_depth_AI = None
        
    # The main game loop
    def game_loop(self):
        while self.playing:
            # If the Tictactoe game is over, restart the Tictactoe game
            if self.tictactoe_game_over == True:
                pygame.time.delay(3000)
                self.state_stack.pop()
                new_state = tictactoe.Tictactoe(self, 'X', self.tictactoe_max_depth_AI)
                new_state.enter_state()
                self.tictactoe_game_over = False
                
            # If the Pong game is over, restart the Pong game
            if self.pong_game_over == True:
                pygame.time.delay(3000)
                self.state_stack.pop()
                new_state = pong.Pong(self, self.pong_mode)
                new_state.enter_state()
                self.pong_game_over = False
            
            # If the Battleship game is over, restart the Battleship game
            if self.battleship_game_over == True:
                pygame.time.delay(3000)
                self.state_stack.pop()
                new_state = battleship.Battleship(self, self.battleship_mode)
                new_state.enter_state()
                self.battleship_game_over = False
            
            # If the Checkers game is over, restart the Checkers game
            if self.checkers_game_over == True:
                pygame.time.delay(3000)
                self.state_stack.pop()
                new_state = checkers.Checkers(self, self.checkers_max_depth_AI)
                new_state.enter_state()
                self.checkers_game_over = False
                
            self.render()    
            self.get_events()    
            self.clock.tick(FPS)    # Set the maximum frames per second for all windows
                
    def render(self):
        # Render current state to the screen
        self.state_stack[-1].render()
            
    def get_events(self):
        # Call the events of the current state
        self.state_stack[-1].get_events()

    # Load the states
    def load_states(self):
        self.title_screen = GameMenu(self)
        self.state_stack.append(self.title_screen)

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()