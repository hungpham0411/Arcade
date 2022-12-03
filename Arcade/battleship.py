import pygame
import button
import os
import sys
import random
from state import State
from battleship_players import Player

SQUARE_SIZE = 40                
HORIZONTAL_MARGIN = SQUARE_SIZE * 4      
VERTICAL_MARGIN = SQUARE_SIZE          
INDENT = 10

BOARD_WIDTH = 1000
BOARD_HEIGHT = 600
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 150)
STRONG_BLUE = (0, 0, 102)
BLUE = (50, 150, 200)
RED = (250, 50, 100)
ORANGE = (250, 140, 20)
COLORS = {"M": BLUE, "H": ORANGE, "S": RED}

class Battleship(State):
    def __init__(self, game, mode):
        State.__init__(self, game)
        self.mode = mode
        self.game.battleship_mode = mode
        
        self.human1 = True
        self.human2 = False
        self.player1 = Player()
        self.player2 = Player()
        self.player_turn = True
        self.computer_turn = True if not self.human1 else False
        
        self.miss_sound = pygame.mixer.Sound(os.path.join('Assets', 'battleship_miss_sound.mp3'))
        self.hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'battleship_hit_sound.mp3'))
        
        self.over = False
        self.result = None
        
        self.load_assets()
    
    def make_move(self, move):
        player = self.player1 if self.player_turn else self.player2
        opponent = self.player2 if self.player_turn else self.player1
        
        if player.search[move] != "U":
            return
        
        hit = False
        
        # If the move is on the opponent ships
        if move in opponent.indexes: 
            player.search[move] = "H"
            hit = True
            # Check if ship is sunk ("S")
            for ship in opponent.ships:
                sunk = True
                # Check if there is still any square of the ship that is not hit
                for index in ship.indexes: 
                    if player.search[index] == "U":
                        sunk = False
                        break
                if sunk:
                    for index in ship.indexes:
                        player.search[index] = "S"
        # If the move is not on the opponent ships
        else: 
            player.search[move] = "M"
            
        #check if game is over
        game_over = True
        for index in opponent.indexes:
            if player.search[index] == "U":
                game_over = False
                break
        self.over = game_over
        self.result = "Player" if self.player_turn else "Computer"
                
        #change active team
        #if not hit:        # If you want to play alternative turns, leave this comment
                            # if not (if you hit you can continue to make a move), uncomment this 
        self.player_turn = not self.player_turn
        
        #switch between human and computer turns
        if (self.human1 and not self.human2) or (not self.human1 and self.human2):
            self.computer_turn = not self.computer_turn
    
    # Make normal AI move
    def normal_ai(self):
        search = self.player1.search if self.player_turn else self.player2.search
        # List of unknown, "U" squares 
        unknown_squares = [i for i, square in enumerate(search) if square == "U"]
        # List of hit, "H" squares
        hit_squares = [i for i, square in enumerate(search) if square == "H"]
        
        # Search in neighborhood for hit squares
        u_squares_with_neighboring_hit_squares = [] 
        for u in unknown_squares:
            # Check if the "U" square has any adjacent hit square
            if u + 1 in hit_squares or u - 1 in hit_squares or u + 10 in hit_squares or u - 10 in hit_squares:
                u_squares_with_neighboring_hit_squares.append(u)
       
        # Pick "U" square that has an adjacent hit square
        if len(u_squares_with_neighboring_hit_squares) > 0:
            self.make_move(random.choice(u_squares_with_neighboring_hit_squares))
        else:
            self.make_random_move()
            
    # Make hard AI move
    def hard_ai(self):
        search = self.player1.search if self.player_turn else self.player2.search
        # List of unknown, "U" squares 
        unknown_squares = [i for i, square in enumerate(search) if square == "U"]
        # List of hit, "H" squares
        hit_squares = [i for i, square in enumerate(search) if square == "H"]
        
        # Search in neighborhood for hit squares
        u_squares_with_neighboring_hit_squares1 = [] 
        u_squares_with_neighboring_hit_squares2 = [] 
        for u in unknown_squares:
            # Check if the "U" square has any adjacent hit square
            if u + 1 in hit_squares or u - 1 in hit_squares or u + 10 in hit_squares or u - 10 in hit_squares:
                u_squares_with_neighboring_hit_squares1.append(u)
                # If the "U" square has any adjacent hit square, check if that "U" square also has any hit square 
                # that is 2 tiles away from it that could form a line of hit squares with the first adjacent hit square
                if u + 2 in hit_squares or u - 2 in hit_squares or u + 20 in hit_squares or u - 20 in hit_squares:
                    u_squares_with_neighboring_hit_squares2.append(u)
        
        # Pick "U" square that has a hit square which is 1 tile away (adjacent)
        # and a hit square which is two tiles away, (both of them in a line)
        if len(u_squares_with_neighboring_hit_squares2) > 0:
            self.make_move(random.choice(u_squares_with_neighboring_hit_squares2))
            return

        # Pick "U" square that has an adjacent hit square
        if len(u_squares_with_neighboring_hit_squares1) > 0:
            self.make_move(random.choice(u_squares_with_neighboring_hit_squares1))
        else:
            self.make_random_move()
            
    def make_random_move(self):
        search = self.player1.search if self.player_turn else self.player2.search
        # List of unknown, "U" squares 
        unknown_squares = [i for i, square in enumerate(search) if square == "U"]
        if len(unknown_squares) > 0:
            # Choose randomly from the list of unknown squares
            random_index = random.choice(unknown_squares)
            self.make_move(random_index)
            
    # Draw the grids
    def draw_grid(self, left = 0, top = 0):    
        for i in range(100):
            x = left + i % 10 * SQUARE_SIZE
            y = top + i // 10 * SQUARE_SIZE
            square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(self.game.screen, WHITE, square, width = 1)
    
    # Draw the markers (color circles for Miss, Hit, and Sunk)
    def draw_markers(self, player, left = 0, top = 0):
        for i in range(100):
            x = left + i % 10 * SQUARE_SIZE
            y = top + i // 10 * SQUARE_SIZE
            if player.search[i] == "U":
                pass
            else:
                x += SQUARE_SIZE // 2
                y += SQUARE_SIZE // 2
                pygame.draw.circle(self.game.screen, COLORS[player.search[i]], (x,y), radius = SQUARE_SIZE // 4)
    
    # Draw the ships onto the grid
    def draw_ships(self, player, left = 0, top = 0):
        for ship in player.ships:
            x = left + ship.column * SQUARE_SIZE + INDENT
            y = top + ship.row * SQUARE_SIZE + INDENT
        
            if ship.orientation == "h":
                width = ship.size * SQUARE_SIZE - 2 * INDENT
                height = SQUARE_SIZE - 2 * INDENT
            else:
                width = SQUARE_SIZE - 2 * INDENT
                height = ship.size * SQUARE_SIZE - 2 * INDENT
            rectangle = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.game.screen, GREEN, rectangle, border_radius = 15)
    
    # Draw the Player and Computer Text
    def draw_players_text(self):
        score_font = self.get_font(20)
        player_score_text = score_font.render("Player Board", 1, WHITE)
        computer_score_text = score_font.render("Computer Board", 1, WHITE)
        
        self.game.screen.blit(player_score_text, (self.game.screen_width//4 - player_score_text.get_width()//2 + 60, 100))
        self.game.screen.blit(computer_score_text, (3 * self.game.screen_width//4 - computer_score_text.get_width()//2 - 70, 100))
        
    # Draw the Battleship board on the game window
    def draw_board(self):
        background = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.game.screen, BLACK, background)
        
        # Draw the grid and ships for the player then draw the markers for CPU moves on the player board
        self.draw_grid(left = (self.game.screen_width//2 - BOARD_WIDTH//2 + 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
        self.draw_ships(self.player1, left = (self.game.screen_width//2 - BOARD_WIDTH//2 + 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
        self.draw_markers(self.player2, left = (self.game.screen_width//2 - BOARD_WIDTH//2 + 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
        
        # Draw the grid for the CPU then draw the markers for player moves on the CPU board
        self.draw_grid(left = (self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
        self.draw_markers(self.player1, left = (self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
        
        self.draw_players_text()
        
        pygame.display.update()
        
    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.battleship_background,(self.game.screen_width, self.game.screen_height)), (0,0)) 
        
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
                x, y = pygame.mouse.get_pos()
                if not self.game.battleship_game_over and self.player_turn:
                    move_board_left_vertical_border = self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50
                    move_board_right_vertical_border = self.game.screen_width//2 + BOARD_WIDTH//2 - 50
                    move_board_top_horizontal_border = self.game.screen_height//2 - BOARD_HEIGHT//2 + 100
                    move_board_bottom_horizontal_border = self.game.screen_height//2 + BOARD_HEIGHT//2 - 100
                    
                    # Make sure the player's move is on the grid (move board for player)
                    if move_board_left_vertical_border < x < move_board_right_vertical_border and move_board_top_horizontal_border < y < move_board_bottom_horizontal_border:
                        row = y // SQUARE_SIZE - 4
                        column = x // SQUARE_SIZE - 17
                        index = row * 10 + column
                        self.make_move(index)

                    self.draw_board()  
                    
                    # Game over message when the game is over
                    if self.over:
                        self.draw_ships(self.player2, left = (self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
                        self.draw_markers(self.player1, left = (self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
                        myfont = self.get_font(25)
                        text = self.result + " wins!!!"
                        textbox = myfont.render(text, 1, WHITE)
                        self.game.screen.blit(textbox, (self.game.screen_width//2 - textbox.get_width()//2, 40))
                        pygame.display.update()
                        self.game.battleship_game_over = True 
                        
        # Computer moves
        if not self.game.battleship_game_over and self.computer_turn:
            # Moves for normal AI
            if self.mode == "normal":
                self.normal_ai()
            # Moves for hard AI
            elif self.mode == "hard":
                self.hard_ai()
            pygame.time.wait(300)
                
            self.draw_board()
                
            # Game over message when the game is over
            if self.over:
                self.draw_ships(self.player2, left = (self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
                self.draw_markers(self.player1, left = (self.game.screen_width//2 + BOARD_WIDTH//2 - SQUARE_SIZE * 10 - 50), top = (self.game.screen_height//2 - BOARD_HEIGHT//2 + 100))
                myfont = self.get_font(25)
                text = self.result + " wins!!!"
                textbox = myfont.render(text, 1, WHITE)
                self.game.screen.blit(textbox, (self.game.screen_width//2 - textbox.get_width()//2, 40))
                pygame.display.update()
                self.game.battleship_game_over = True
                 
    def load_assets(self):
        self.battleship_background = pygame.image.load(os.path.join('Assets', 'retro_background3.jpg'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)