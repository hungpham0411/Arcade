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

    def game_loop(self):
        while self.playing:
            if self.game_over == True:
                self.state_stack.pop()
                new_state = tictactoe.Tictactoe(self, 'X')
                pygame.display.update()
                pygame.time.delay(2000)
                new_state.enter_state()
                self.game_over = False
            self.render()
            self.get_events()
            self.clock.tick(FPS)
        pygame.quit()
                
    def render(self):
        # Render current state to the screen
        self.state_stack[-1].render()
            
    def get_events(self):
        self.state_stack[-1].get_events()

        #def draw_text(self, surface, text, color, x, y):
            #text_surface = self.font.render(text, True, color)
            #text_rect = text_surface.get_rect()
            #text_rect.center = (x, y)
            #surface.blit(text_surface, text_rect)

    # Load the states
    def load_states(self):
        self.title_screen = GameMenu(self)
        self.state_stack.append(self.title_screen)

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()