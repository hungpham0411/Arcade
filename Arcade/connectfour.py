import pygame
import button
import os
import sys
import math
from state import State
from connectfour_players import ConnectFourAIPlayer

SQUARE_SIZE = 80

STRONG_BLUE = (0, 0, 102)
BLUE = (50, 150, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = YELLOW = (255, 255, 0)
BOARD_WIDTH = 560
BOARD_HEIGHT = 560
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100

class ConnectFour(State):
    def __init__(self, game, player_color, max_depth_AI):
        State.__init__(self, game)
        self.players = []
        self.grid = []
        self.turn = -1
        self.max_depth_AI = max_depth_AI
        self.player_color = player_color
        self.game.connectfour_player_color = player_color
        self.game.connectfour_max_depth_AI = max_depth_AI
        
        if self.player_color == RED:
            self.AI_player = ConnectFourAIPlayer(YELLOW, self)
        else:
            self.AI_player = ConnectFourAIPlayer(RED, self)
            
        self.game_over = False
        self.result = None
        self.initialize()
        self.load_assets()
        
    # Initialize the grid
    def initialize(self):
        for i in range(6):
            row = []
            for j in range(7):
                row.append(-1)
            self.grid.append(row)
        self.turn = RED
        
    def set_position(self, column, player):
        row = 5
        while self.grid[row][column] != -1:
            row -= 1
        self.grid[row][column] = player
        self.result = self.check_for_winner()
            
    def check_for_winner(self):
        win = self.check_horizontal_win()
        if win is None:
            win = self.check_vertical_win()
        if win is None:
            win = self.check_neg_diagonal_win()
        if win is None:
            win = self.check_pos_diagonal_win()
        return win 
    
    def check_horizontal_win(self):
        win = False
        state = self.grid
        for row in range(6):
            for column in range(4):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row][column + 1]) and (
                        state[row][column] == state[row][column + 2]) and (
                            state[row][column] == state[row][column + 3]) 
                if win:
                    self.game_over = True
                    return state[row][column]
        return None
    
    def check_vertical_win(self):
        win = False
        state = self.grid
        for column in range(7):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column]) and (
                        state[row][column] == state[row + 2][column]) and (
                            state[row][column] == state[row + 3][column])
                if win:
                    self.game_over = True
                    return state[row][column]
        return None
    
    def check_neg_diagonal_win(self):
        win = False
        state = self.grid
        for column in range(4):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column + 1]) and (
                        state[row][column] == state[row + 2][column + 2]) and (
                            state[row][column] == state[row + 3][column + 3])
                    if win:
                        self.game_over = True
                        return state[row][column]
        return None
    
    def check_pos_diagonal_win(self):
        win = False
        state = self.grid
        for column in range(3, 7):
            for row in range(3):
                if state[row][column] != -1:
                    win = (state[row][column] == state[row + 1][column - 1]) and (
                        state[row][column] == state[row + 2][column - 2]) and (
                            state[row][column] == state[row + 3][column - 3])
                if win:
                    self.game_over = True
                    return state[row][column]
        return None
                
    def check_for_draw(self):
        for row in range(6):
            for column in range(7):
                if self.grid[row][column] == -1:
                    return False
        self.game_over = True
        return True
    
    def next_player(self):
        if self.turn == RED:
            self.turn = YELLOW
        else:
            self.turn = RED

    def get_turn(self):
        return self.turn
    
    def get_grid(self):
        return self.grid
    
    # Place the move
    def place_token(self, move):
        self.set_position(move, self.get_turn())
        self.next_player()
    
    # Draw the connectfour grid
    def draw_grid(self):
        for row in range(6):
            for column in range(7):
                square = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE, 
                                     self.game.screen_height//2 - BOARD_HEIGHT//2 + row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.game.screen, BLUE, square)
                pygame.draw.circle(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE + SQUARE_SIZE//2, 
                                                             self.game.screen_height//2 - BOARD_HEIGHT//2 + row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE//2), 35)
        vertical_border_left = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 - 6, self.game.screen_height//2 - BOARD_HEIGHT//2 + SQUARE_SIZE, 6, BOARD_HEIGHT - SQUARE_SIZE + 6)
        vertical_border_right = pygame.Rect(self.game.screen_width//2 + BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2 + SQUARE_SIZE, 6, BOARD_HEIGHT - SQUARE_SIZE + 6)
        horizontal_border_top = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 - 6, self.game.screen_height//2 - BOARD_HEIGHT//2  + SQUARE_SIZE - 6, BOARD_WIDTH + 12, 6)
        horizontal_border_bottom = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 + BOARD_HEIGHT//2, BOARD_WIDTH, 6)
        
        pygame.draw.rect(self.game.screen, BLUE, vertical_border_left)
        pygame.draw.rect(self.game.screen, BLUE, vertical_border_right)
        pygame.draw.rect(self.game.screen, BLUE, horizontal_border_top)
        pygame.draw.rect(self.game.screen, BLUE, horizontal_border_bottom)
    
    # Draw the pieces
    def draw_pieces(self):
        for row in range(6):
            for column in range(7):
                if self.grid[row][column] == RED:
                    pygame.draw.circle(self.game.screen, RED, (self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE + SQUARE_SIZE//2, 
                                                               self.game.screen_height//2 - BOARD_HEIGHT//2 + row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE//2), 35)
                elif self.grid[row][column] == YELLOW:
                    pygame.draw.circle(self.game.screen, YELLOW, (self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE + SQUARE_SIZE//2, 
                                                                  self.game.screen_height//2 - BOARD_HEIGHT//2 + row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE//2), 35)    
    
    # Draw the connectfour board on the game window
    def draw_board(self):
        self.draw_grid()
        self.draw_pieces()
        
        pygame.display.update()
        
    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.connectfour_background,(self.game.screen_width, self.game.screen_height)), (0,0)) 
        
        # Buttons
        red_button = button.Button(self.game.screen_width - BUTTON_WIDTH*3 - 30, 10, 
                                 "Red", self.get_font(15), BLACK, STRONG_BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        yellow_button = button.Button(self.game.screen_width - BUTTON_WIDTH*2 - 20, 10, 
                                 "Yellow", self.get_font(15), BLACK, STRONG_BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        back_button = button.Button(self.game.screen_width - BUTTON_WIDTH - 10, 10, 
                                 "Back", self.get_font(17), BLACK, STRONG_BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Option for the human player to go first (as RED)
        if red_button.interact_button() == True:
            self.game.state_stack.pop()
            new_state = ConnectFour(self.game, RED, self.max_depth_AI)
            new_state.enter_state()
        
        # Option for the human player to go second (as YELLOW)
        if yellow_button.interact_button() == True:
            self.game.state_stack.pop()
            new_state = ConnectFour(self.game, YELLOW, self.max_depth_AI)
            new_state.enter_state() 
        
        # Back button to return to the connectfour difficulty screen
        if back_button.interact_button() == True:
            self.exit_state()   # Exit the current state which will move to the previous state
            pygame.time.wait(300)
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Track the piece and synchronize it with the player's mouse position
            if event.type == pygame.MOUSEMOTION:
                if self.turn == self.player_color and not self.game.connectfour_game_over:
                    pos = pygame.mouse.get_pos()
                    in_width_boundary = (self.game.screen_width//2 - BOARD_WIDTH//2 < pos[0] < self.game.screen_width//2 + BOARD_WIDTH//2)
                    in_height_boundary = (self.game.screen_height//2 - BOARD_HEIGHT//2 < pos[1] < self.game.screen_height//2 + BOARD_HEIGHT//2)
                    if in_width_boundary and in_height_boundary:
                        column = (pos[0] - (self.game.screen_width//2 - BOARD_WIDTH//2)) // SQUARE_SIZE
                        start = self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE + SQUARE_SIZE//2
                        pygame.draw.circle(self.game.screen, self.player_color, (start, self.game.screen_height//2 - BOARD_HEIGHT//2 + SQUARE_SIZE//2 - 6), 35)
                self.draw_board()
            
            # Player moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.turn == self.player_color and not self.game.connectfour_game_over:
                    # Position of player's move 
                    pos = pygame.mouse.get_pos()
                    
                    # Check if the moves are in the board or outside of the board
                    in_width_boundary = (self.game.screen_width//2 - BOARD_WIDTH//2 <= pos[0] <= self.game.screen_width//2 + BOARD_WIDTH//2)
                    in_height_boundary = (self.game.screen_height//2 - BOARD_HEIGHT//2 <= pos[1] <= self.game.screen_height//2 + BOARD_HEIGHT//2)
                    if in_width_boundary and in_height_boundary:
                        move = (pos[0] - (self.game.screen_width//2 - BOARD_WIDTH//2)) // SQUARE_SIZE
                        self.place_token(move)
                    else:
                        pass
    
                    self.draw_board()
                    
                    # Game over message when the game is over
                    if self.game_over:
                        if self.result == self.player_color:
                            text = "Player wins!!!"
                            winner_color = self.player_color
                        elif self.result == self.AI_player.color:
                            text = "Computer wins!!!"
                            winner_color = self.AI_player.color
                        else:
                            text = "Draw!!!"
                            winner_color = WHITE
                        myfont = self.get_font(25)
                        textbox = myfont.render(text, 1, winner_color)
                        self.draw_board()
                        self.game.screen.blit(textbox, (self.game.screen_width//2 - textbox.get_width()//2, SQUARE_SIZE - 10))
                        pygame.display.update()
                        self.game.connectfour_game_over = True  
                    
        # Computer moves
        if self.turn == self.AI_player.color and not self.game.connectfour_game_over:                
            move = self.AI_player.get_move()
            self.place_token(move)
            
            self.draw_board()
                    
            # Game over message when the game is over
            if self.game_over:
                if self.result == self.player_color:
                    text = "Player wins!!!"
                    winner_color = self.player_color
                elif self.result == self.AI_player.color:
                    text = "Computer wins!!!"
                    winner_color = self.AI_player.color
                else:
                    text = "Draw!!!"
                    winner_color = WHITE
                myfont = self.get_font(25)
                textbox = myfont.render(text, 1, winner_color)
                self.draw_board()
                self.game.screen.blit(textbox, (self.game.screen_width//2 - textbox.get_width()//2, SQUARE_SIZE - 10))
                pygame.display.update()
                self.game.connectfour_game_over = True

    def load_assets(self):
        self.connectfour_background = pygame.image.load(os.path.join('Assets', 'cyberpunk_background4.png'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)