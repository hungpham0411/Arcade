import pygame
import button
import os
import sys
import numpy as np
from tictactoe_players import TicTacToeAIPlayer, TicTacToeHumanPlayer
from state import State

BLUE = (0, 0, 102)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_SIDE = 450
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100
PLAYER1 = 'X'
PLAYER2 = 'O'

class Tictactoe(State):
    def __init__(self, game, symbol_for_player, max_depth_AI):
        State.__init__(self, game)
        self.players = []
        self.grid = []
        self.turn = -1
        self.max_depth_AI = max_depth_AI
        self.game.tictactoe_symbol_for_player = symbol_for_player
        self.game.tictactoe_max_depth_AI = max_depth_AI
        
        # Set the human player according the symbol_for_player attribute
        if symbol_for_player == 'X': # If the symbol is 'X', the human player go first
            player1 = TicTacToeHumanPlayer('X')
            player2 = TicTacToeAIPlayer('O', self)
            if len(self.players) > 0:
                self.players[0] = player1
                self.players[1] = player2
            else: 
                self.players.append(player1)
                self.players.append(player2)
        else:   # If not, the human player go second ('O')
            player1 = TicTacToeAIPlayer('X', self)
            player2 = TicTacToeHumanPlayer('O')
            if len(self.players) > 0:
                self.players[0] = player1
                self.players[1] = player2
            else: 
                self.players.append(player1)
                self.players.append(player2)
        
        self.initialize()
        self.load_assets()
        
    # Initialize the grid
    def initialize(self):
        self.grid = [[None, None, None], [None, None, None], [None, None, None]]
        self.turn = 'X'
    
    def set_position(self, pos, player):
        pos -= 1
        row = pos // 3
        col = pos % 3
        # Play the sound effect when making a move
        if player == 'X':
            self.X_sound.play()
        else:
            self.O_sound.play()
        self.grid[row][col] = player
            
    def check_for_winner(self):
        state = self.grid
        for row in range(3):
            if state[row][0] is not None and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                return state[row][0]
        for col in range(3):
            if state[0][col] is not None and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                return state[0][col]
        if state[0][0] is not None and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
            return state[0][0]
        if state[2][0] is not None and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
            return state[2][0]

        return self.check_for_draw()  
    
    def check_for_draw(self):
        all_filled = True
        for row in range(3):
            for col in range(3):
                if self.grid[row][col] is None:
                    all_filled = False
        return all_filled
    
    def next_player(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def get_turn(self):
        return self.turn

    def get_grid(self):
        return self.grid
    
    # Place the move
    def place_token(self, move):
        self.set_position(move, self.get_turn())
        self.next_player()
    
    def get_player(self, p):
        if p == 'X':
            return self.players[0]
        return self.players[1]
    
    # Draw the tic-tac-toe grid
    def draw_grid(self):
        # Tic-tac-toe visual board
        visual_board = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, BOARD_SIDE, BOARD_SIDE)
        pygame.draw.rect(self.game.screen, BLACK, visual_board)
        
        # Vertical border
        vertical_border_left = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, 6, BOARD_SIDE)
        vertical_border_right = pygame.Rect(self.game.screen_width//2 + BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, 6, BOARD_SIDE)
        
        # Horizontal border
        horizontal_border_top = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, BOARD_SIDE, 6)
        horizontal_border_bottom = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 + BOARD_SIDE/2, BOARD_SIDE + 10, 6)

        pygame.draw.rect(self.game.screen, WHITE, vertical_border_left)
        pygame.draw.rect(self.game.screen, WHITE, vertical_border_right)
        pygame.draw.rect(self.game.screen, WHITE, horizontal_border_top)
        pygame.draw.rect(self.game.screen, WHITE, horizontal_border_bottom)
        
        # Lines inside the board
        for i in range(1,3):
            # horizontal lines
            pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3), 
                             (self.game.screen_width//2 + BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3), 6) 
            # vertical lines
            pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3, self.game.screen_height//2 - BOARD_SIDE/2), 
                             (self.game.screen_width//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3, self.game.screen_height//2 + BOARD_SIDE/2), 6)
    
    # Draw the markers for 'X' and 'O'
    def draw_markers(self):
        for row in range(3):
            for column in range(3):
                if self.grid[row][column] == PLAYER1:     # For 'X'
                    pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 35, self.game.screen_height//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 35), 
                                     (self.game.screen_width//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 115, self.game.screen_height//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 115), 15)
                    pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 115, self.game.screen_height//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 35), 
                                     (self.game.screen_width//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 35, self.game.screen_height//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 115), 15)
                elif self.grid[row][column] == PLAYER2:   # For 'O'
                    pygame.draw.circle(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 80, self.game.screen_height//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 75), 50, 15)
                    
    # Draw the tic-tac-toe board on the game window
    def draw_board(self):
        self.draw_grid()
        self.draw_markers()
        
        pygame.display.update()
        
    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.tictactoe_background,(self.game.screen_width, self.game.screen_height)), (0,0)) 
        
        # Buttons
        X_button = button.Button(self.game.screen_width - BUTTON_WIDTH*3 - 30, 10, 
                                 "X", self.get_font(30), BLACK, BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        O_button = button.Button(self.game.screen_width - BUTTON_WIDTH*2 - 20, 10, 
                                 "O", self.get_font(30), BLACK, BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        back_button = button.Button(self.game.screen_width - BUTTON_WIDTH - 10, 10, 
                                 "Back", self.get_font(17), BLACK, BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Option for the human player to go first (as 'X')
        if X_button.interact_button() == True:
            self.game.state_stack.pop()
            new_state = Tictactoe(self.game, 'X', self.max_depth_AI)
            new_state.enter_state()
        
        # Option for the human player to go second (as 'O')
        if O_button.interact_button() == True:
            pygame.time.wait(50)
            self.game.state_stack.pop()
            new_state = Tictactoe(self.game, 'O', self.max_depth_AI)
            new_state.enter_state() 
        
        # Back button to return to the tictactoe difficulty screen
        if back_button.interact_button() == True:
            pygame.mixer.music.unload()  # Unload the game background music when go back to the Game Hub
            pygame.mixer.music.load(os.path.join('Assets', 'menu_music.mp3'))   # Load the Game Hub background music
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1) # Repeat the song indefinitely
            self.exit_state()   # Exit the current state which will move to the previous state
            pygame.time.wait(300)
        
        self.draw_board()
    
    def get_events(self):
        myfont = self.get_font(25)
        player_char = self.get_turn()
        player = self.get_player(player_char)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Check if the player playing is the human player
                if player.is_automated() == False and not self.game.tictactoe_game_over:
                    # Position of the human's move
                    pos = pygame.mouse.get_pos()
                    cell_x = pos[0] // 150 - 3 # The column of the move
                    cell_y = pos[1] // 150 - 1 # The row of the move
                    
                    # Check if the moves are in the board or outside of the board
                    if 0 <= cell_x <= 2 and 0 <= cell_y <= 2:
                        if self.grid[cell_y][cell_x] is not None:
                            pass
                        else:
                            move = cell_y * 3 + (cell_x + 1)
                            self.place_token(move)
                            self.draw_board()
                    else:
                        pass
                    result = self.check_for_winner()
                    
                    #Check if the human player win
                    if result == player_char:
                        if result == PLAYER1:
                            # Make the sound effect when the game is over
                            self.gameover_sound.play()
                            label = myfont.render("Player wins!!!", 1, WHITE)
                            self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                            pygame.display.update()
                            self.game.tictactoe_game_over = True
                        else:
                            # Make the sound effect when the game is over
                            self.gameover_sound.play()
                            label = myfont.render("Computer wins!!!", 1, WHITE)
                            self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                            pygame.display.update()
                            self.game.tictactoe_game_over = True
                            
                    #Check for draw
                    elif result == True:
                        # Make the sound effect when the game is over
                        self.gameover_sound.play()
                        label = myfont.render("Draw!!!", 1, WHITE)
                        self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                        pygame.display.update()
                        self.game.tictactoe_game_over = True
                    
        #Check if the player playing is the AI
        if player.is_automated() == True and not self.game.tictactoe_game_over:       
            pygame.time.wait(500)         
            move = player.get_move()
            self.place_token(move)
            self.draw_board()
            result = self.check_for_winner()
            
            #Check if the AI player win
            if result == player_char:
                if result == PLAYER1:
                    # Make the sound effect when the game is over
                    self.gameover_sound.play()
                    label = myfont.render("Player wins!!!", 1, WHITE)
                    self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                    pygame.display.update()
                    self.game.tictactoe_game_over = True
                else:
                    # Make the sound effect when the game is over
                    self.gameover_sound.play()
                    label = myfont.render("Computer wins!!!", 1, WHITE)
                    self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                    pygame.display.update()
                    self.game.tictactoe_game_over = True
                    
            #Check for draw
            elif result == True: 
                # Make the sound effect when the game is over
                self.gameover_sound.play()
                label = myfont.render("Draw!!!", 1, WHITE)
                self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                pygame.display.update()
                self.game.tictactoe_game_over = True  

    def load_assets(self):
        self.tictactoe_background = pygame.image.load(os.path.join('Assets', 'cyberpunk_background.jpg'))
        
        # Sound effects
        self.X_sound = pygame.mixer.Sound(os.path.join('Assets', 'tictactoe_X_sound.wav'))
        self.O_sound = pygame.mixer.Sound(os.path.join('Assets', 'tictactoe_O_sound.wav'))
        self.gameover_sound = pygame.mixer.Sound(os.path.join('Assets', 'gameover_sound.wav'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)