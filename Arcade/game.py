import pygame
from game_menu import GameMenu
import tictactoe

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
        
        self.game_over = False
        self.max_depth_AI = 0

    # The main game loop
    def game_loop(self):
        while self.playing:
            # If the game is over, restart the game
            if self.game_over == True:
                self.state_stack.pop()
                new_state = tictactoe.Tictactoe(self, 'X', self.max_depth_AI)
                pygame.display.update()
                pygame.time.delay(2000)
                new_state.enter_state()
                self.game_over = False
            self.render()
            self.get_events()
            self.clock.tick(FPS)    # Set the maximum frames per second for all windows
        pygame.quit()
                
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