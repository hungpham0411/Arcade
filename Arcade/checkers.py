import pygame
import button
import os
import sys
from state import State
from checkers_board import CheckersBoard
from checkers_players import CheckersAIPlayer

SQUARE_SIZE = 80                

BOARD_WIDTH = 640
BOARD_HEIGHT = 640
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STRONG_BLUE = (0, 0, 102)
BLUE = (50, 150, 200)
RED = (250, 50, 100)
GREEN = (0, 255, 0)
YELLOW = (102,102,0)

class Checkers(State):
    def __init__(self, game, max_depth_AI):
        State.__init__(self, game)
        self.max_depth_AI = max_depth_AI
        self.game.checkers_max_depth_AI = max_depth_AI
        self.AI_player = CheckersAIPlayer(BLUE, self)
        self.board = CheckersBoard()
        self.load_assets()
        
    def get_board(self):
        return self.board
    
    # Draw the Checkers grid
    def draw_grid(self, left = 0, top = 0):    
        for i in range(64):
            x = i % 8 
            y = i // 8 
            square = pygame.Rect(left + x * SQUARE_SIZE, top + y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(self.game.screen, WHITE, square)
            if y % 2 == 1:
                if x % 2 == 1:
                    pygame.draw.rect(self.game.screen, BLACK, square)
            elif y % 2 == 0:
                if x % 2 == 0:
                    pygame.draw.rect(self.game.screen, BLACK, square)
                    
        vertical_border_left = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 - 6, self.game.screen_height//2 - BOARD_HEIGHT//2, 6, BOARD_HEIGHT + 6)
        vertical_border_right = pygame.Rect(self.game.screen_width//2 + BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, 6, BOARD_HEIGHT + 6)
        horizontal_border_top = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, BOARD_WIDTH, 6)
        horizontal_border_bottom = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 + BOARD_HEIGHT//2, BOARD_WIDTH, 6)
        
        pygame.draw.rect(self.game.screen, RED, vertical_border_left)
        pygame.draw.rect(self.game.screen, RED, vertical_border_right)
        pygame.draw.rect(self.game.screen, RED, horizontal_border_top)
        pygame.draw.rect(self.game.screen, RED, horizontal_border_bottom)
    
    # Draw the Checkers pieces
    def draw_pieces(self):
        for row in range(8):
            for column in range(8):
                piece = self.board.grid[row][column]
                if piece != '-' and piece != -1:
                    if piece.color == RED:
                        x = self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE + 40
                        y = self.game.screen_height//2 - BOARD_HEIGHT//2 + row * SQUARE_SIZE + 40
                        pygame.draw.circle(self.game.screen, RED, (x, y), 30)
                        
                        # If piece is a king piece
                        if piece.king:  
                            crown = pygame.transform.scale(self.crown_image, (44,25))
                            self.game.screen.blit(crown, (x - crown.get_width()//2, y - crown.get_height()//2))
                            
                    elif piece.color == BLUE:
                        x = self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE + 40
                        y = self.game.screen_height//2 - BOARD_HEIGHT//2 + row * SQUARE_SIZE + 40
                        pygame.draw.circle(self.game.screen, BLUE, (x, y), 30)
                        
                        # If piece is a king piece
                        if piece.king:  
                            crown = pygame.transform.scale(self.crown_image, (44,25))
                            self.game.screen.blit(crown, (x - crown.get_width()//2, y - crown.get_height()//2))
    
    # Draw valid moves for the selected piece
    def draw_valid_moves(self, moves):
        for move in moves:
            row, column = move
            valid_move = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 + column * SQUARE_SIZE, 40 + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(self.game.screen, GREEN, valid_move)
    
    # Draw the highlight color for the selected piece
    def draw_selected_move(self, move):
        if move == None:
            return
        selected_move = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 + move.column * SQUARE_SIZE, 40 + move.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.game.screen, YELLOW, selected_move)
        self.draw_pieces()
        
    # Draw the Checkers board on the game window
    def draw_board(self):
        self.draw_grid(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2)
        self.draw_pieces()
        if not self.board.game_over:
            self.draw_selected_move(self.board.selected)
            self.draw_valid_moves(self.board.valid_moves)
        
        pygame.display.update()
        
    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.checkers_background,(self.game.screen_width, self.game.screen_height)), (0,0)) 
        
        # Buttons
        back_button = button.Button(self.game.screen_width - BUTTON_WIDTH - 10, 10, 
                                 "Back", self.get_font(17), BLACK, STRONG_BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        #rules_button = button.Button(self.game.screen_width - BUTTON_WIDTH - 10, 10, 
                                 #"Rules", self.get_font(17), BLACK, BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Back button to return to the pong difficulty screen
        if back_button.interact_button() == True:
            self.exit_state()   # Exit the current state which will move to the previous state
            pygame.time.wait(300)
            
        #if rules_button.interact_button(self.game.screen) == True:
        
        self.draw_board()
            
    def get_events(self):
        self.game.checkers_game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Player moves
                if not self.game.checkers_game_over and self.board.turn == RED:
                    # Position of player's move
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // SQUARE_SIZE - 4 
                    y = (pos[1]-40) // SQUARE_SIZE 
                    if x > 7 or y > 7:  # If the moves is out of the checkers board, pass
                        pass 
                    else:
                        self.board.select(y, x, self.checkers_sound)  
                        self.draw_board()
                        
                        if self.board.game_over:
                            # Make the sound effect when the game is over
                            self.gameover_sound.play()
                            myfont = self.get_font(25)
                            winner, winner_color = self.board.result
                            text = winner + " wins!!!"
                            textbox = myfont.render(text, 1, winner_color)
                            self.game.screen.blit(textbox, (20, 20))
                            pygame.display.update()
                            self.game.checkers_game_over = True
        
        # Computer moves
        if not self.game.checkers_game_over and self.board.turn == BLUE:
            if self.max_depth_AI > 4:
                pygame.time.wait(200)
            else:
                pygame.time.wait(500)
            opponent = RED
            piece, move, skipped = self.AI_player.get_move()
            row, column = move
            self.board.move_piece(piece, row, column)
            if skipped is not None:
                self.board.remove_piece(skipped)
            
            # Check if there is any red piece or blue piece left on the board + 
            # check if player has any valid move to place on the board
            if self.board.red_left <= 0 or self.board.blue_left <= 0 or len(self.board.get_all_valid_moves(opponent)) == 0:
                self.board.game_over = True
                self.board.result = ("Player", RED) if self.board.turn == RED else ("Computer", BLUE)
            
            # Check if the current player has any valid move to place on the board
            elif len(self.board.get_all_valid_moves(self.board.turn)) == 0:
                self.board.game_over = True
                self.board.result = ("Player", RED)
                
            self.board.next_player()
            self.draw_board()
            self.checkers_sound.play()  # Play the sound effect when move a checkers piece
            # Game over message when the game is over
            if self.board.game_over:
                # Make the sound effect when the game is over
                self.gameover_sound.play()
                myfont = self.get_font(25)
                winner, winner_color = self.board.result
                text = winner + " wins!!!"
                textbox = myfont.render(text, 1, winner_color)
                self.game.screen.blit(textbox, (20, 20))
                pygame.display.update()
                self.game.checkers_game_over = True
        
    def load_assets(self):
        self.checkers_background = pygame.image.load(os.path.join('Assets', 'retro_background2.jpg'))
        self.crown_image = pygame.image.load(os.path.join('Assets', 'checkers_crown.png'))
        
        # Sound effects
        self.checkers_sound = pygame.mixer.Sound(os.path.join('Assets', 'checkers_sound.mp3'))
        self.gameover_sound = pygame.mixer.Sound(os.path.join('Assets', "gameover_sound.wav"))
        
    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)