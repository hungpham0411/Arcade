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
    def __init__(self, game, symbol_for_player):
        State.__init__(self, game)
        self.load_assets()
        self.players = []
        self.grid = None
        self.turn = -1
        if symbol_for_player == 'X':
            player1 = TicTacToeHumanPlayer('X')
            player2 = TicTacToeAIPlayer('O', self)
            if len(self.players) > 0:
                self.players[0] = player1
                self.players[1] = player2
            else: 
                self.players.append(player1)
                self.players.append(player2)
        else:
            player1 = TicTacToeAIPlayer('X', self)
            player2 = TicTacToeHumanPlayer('O')
            if len(self.players) > 0:
                self.players[0] = player1
                self.players[1] = player2
            else: 
                self.players.append(player1)
                self.players.append(player2)
        self.initialize()
        self.player_win = 0
        self.computer_win = 0
        self.draw = 0

    def initialize(self):
        self.grid = [[None, None, None], [None, None, None], [None, None, None]]
        self.turn = 'X'
    
    def set_position(self, pos, player):
        pos -= 1
        row = pos // 3
        col = pos % 3
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

        return self.check_for_draw()  # No winner
    
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
    
    def place_token(self, move):
        self.set_position(move, self.get_turn())
        self.next_player()
    
    def get_player(self, p):
        if p == 'X':
            return self.players[0]
        return self.players[1]
    
    # Draw the tic-tac-toe board on the game window
    def draw_board(self, board):
        # Tic-tac-toe logic board
        logic_board = np.transpose(board)
        
        # Tic-tac-toe visual board
        visual_board = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, BOARD_SIDE, BOARD_SIDE)
        pygame.draw.rect(self.game.screen, BLACK, visual_board)
        
        # Vertical border
        line1 = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, 6, BOARD_SIDE)
        line2 = pygame.Rect(self.game.screen_width//2 + BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, 6, BOARD_SIDE)
        
        # Horizontal border
        line3 = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2, BOARD_SIDE, 6)
        line4 = pygame.Rect(self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 + BOARD_SIDE/2, BOARD_SIDE + 10, 6)

        pygame.draw.rect(self.game.screen, WHITE, line1)
        pygame.draw.rect(self.game.screen, WHITE, line2)
        pygame.draw.rect(self.game.screen, WHITE, line3)
        pygame.draw.rect(self.game.screen, WHITE, line4)
        
        # Draw the lines inside the board
        for i in range(1,3):
            pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3), 
                             (self.game.screen_width//2 + BOARD_SIDE/2, self.game.screen_height//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3), 6) 
            pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3, self.game.screen_height//2 - BOARD_SIDE/2), 
                             (self.game.screen_width//2 - BOARD_SIDE/2 + i * BOARD_SIDE/3, self.game.screen_height//2 + BOARD_SIDE/2), 6)
        
        # Draw the markers for 'X' and 'O'
        for row in range(3):
            for column in range(3):
                if logic_board[row][column] == PLAYER1:
                    pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 35, self.game.screen_height//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 35), 
                                     (self.game.screen_width//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 115, self.game.screen_height//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 115), 15)
                    pygame.draw.line(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 115, self.game.screen_height//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 35), 
                                     (self.game.screen_width//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 35, self.game.screen_height//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 115), 15)
                elif logic_board[row][column] == PLAYER2:
                    pygame.draw.circle(self.game.screen, WHITE, (self.game.screen_width//2 - BOARD_SIDE/2 + row * BOARD_SIDE/3 + 80, self.game.screen_height//2 - BOARD_SIDE/2 + column * BOARD_SIDE/3 + 75), 50, 15)
        
        # Score board
        #player = self.get_font(17)
        #label = player.render("Player", 1, WHITE)
        #player_score = self.get_font(25)
        #label1 = player_score.render(str(self.player_win), 1, WHITE)
        #self.game.screen.blit(label, (0, 10))
        #self.game.screen.blit(label1, (40, 30))
        
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
        
        if X_button.draw_button(self.game.screen) == True:
            self.game.state_stack.pop()
            new_state = Tictactoe(self.game, 'X')
            new_state.enter_state()
            
        if O_button.draw_button(self.game.screen) == True:
            self.game.state_stack.pop()
            new_state = Tictactoe(self.game, 'O')
            new_state.enter_state() 
        
        if back_button.draw_button(self.game.screen) == True:
            new_state = self.prev_state
            self.game.state_stack.pop()
            new_state.enter_state()
            pygame.time.wait(300)
        
        self.draw_board(self.get_grid())
    
    def get_events(self):
        myfont = self.get_font(30)
        self.draw_board(self.get_grid())
        self.game.game_over = False
        player_char = self.get_turn()
        player = self.get_player(player_char)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Check if the player playing is the human player
                if player.is_automated() == False:
                    # Position of the human's move
                    pos = pygame.mouse.get_pos()
                    cell_x = pos[0] // 150 - 3 # The column of the move
                    cell_y = pos[1] // 150 - 1 # The row of the move
                    if cell_y > 2 or cell_x > 2:
                        pass
                    else:
                        if self.grid[cell_y][cell_x] is not None:
                            pass
                        else:
                            self.grid[cell_y][cell_x] = player_char
                            self.next_player()
                    result = self.check_for_winner()
                    #Check if the human win
                    if result == player_char:
                        if result == PLAYER1:
                            label = myfont.render("Player 1 wins", 1, WHITE)
                            self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                            #self.player_win += 1
                            self.game.game_over = True
                        else:
                            label = myfont.render("Player 2 wins", 1, WHITE)
                            self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                            #self.player_win += 1
                            self.game.game_over = True
                    #Check for draw
                    elif result == True:
                        label = myfont.render("Draw!!", 1, WHITE)
                        self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                        #self.draw += 1
                        self.game.game_over = True
                            
                    self.draw_board(self.get_grid())
                    
        #Check if the player playing is the AI
        if player.is_automated() == True and not self.game.game_over:                
            move = player.get_move()
            self.place_token(move)
            result = self.check_for_winner()
            #Check if the AI win
            if result == player_char:
                if result == PLAYER1:
                    label = myfont.render("Player 1 wins", 1, WHITE)
                    self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                    #self.computer_win += 1
                    self.game.game_over = True
                else:
                    label = myfont.render("Player 2 wins", 1, WHITE)
                    self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                    #self.player_win += 1
                    self.game.game_over = True
            #Check for draw
            elif result == True: 
                label = myfont.render("Draw!!", 1, WHITE)
                self.game.screen.blit(label, (self.game.screen_width//2 - BOARD_SIDE + 30, 40))
                #self.draw += 1
                self.game.game_over = True  
                      
            self.draw_board(self.get_grid())

    def load_assets(self):
        self.tictactoe_background = pygame.image.load(os.path.join('Assets', 'cyberpunk_background.jpg'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)