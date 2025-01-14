import pygame
import button
import os
import sys
import random
from state import State

BLUE = (0, 0, 102)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_WIDTH = 800
BOARD_HEIGHT = 500
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 100

PADDLE_INSET = 50
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
BALL_SIZE = 10
BALL_MOMENTUM = 5

class Pong(State):
    def __init__(self, game, mode):
        State.__init__(self, game)
        self.load_assets()
        self.mode = mode
        self.game.pong_mode = mode

        self.left_paddle_y = self.game.screen_height//2 - PADDLE_WIDTH - 25     # position y of left paddle
        self.right_paddle_y = self.game.screen_height//2 - PADDLE_WIDTH - 25    # position y of right paddle
        self.ball_x = self.game.screen_width//2 + 5     # position x of ball
        self.ball_y = self.game.screen_height//2        # position y of ball
        self.ball_x_momentum = -(BALL_MOMENTUM - 1)                 
        self.ball_y_momentum = 0
        
        # Number of wins 
        self.player_win = 0    
        self.computer_win = 0  

    # Draw the Pong grid
    def draw_grid(self):
        # Pong visual board
        visual_board = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.game.screen, BLACK, visual_board)
        
        # Divide line
        divide_line = pygame.Rect(self.game.screen_width//2 + 2.5, self.game.screen_height//2 - BOARD_HEIGHT//2, 5, BOARD_HEIGHT)
        pygame.draw.rect(self.game.screen, WHITE, divide_line)
        
        # Vertical borders
        vertical_line_left = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, 6, BOARD_HEIGHT)
        vertical_line_right = pygame.Rect(self.game.screen_width//2 + BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, 6, BOARD_HEIGHT)
        
        # Horizontal borders
        horizontal_line_up = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 - BOARD_HEIGHT//2, BOARD_WIDTH, 6)
        horizontal_line_down = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2, self.game.screen_height//2 + BOARD_HEIGHT//2, BOARD_WIDTH + 10, 6)
        
        # Paddles
        paddle_left = pygame.Rect(self.game.screen_width//2 - BOARD_WIDTH//2 + 50, self.left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        paddle_right = pygame.Rect(self.game.screen_width//2 + BOARD_WIDTH//2 - 50, self.right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        
        pygame.draw.rect(self.game.screen, WHITE, vertical_line_left)
        pygame.draw.rect(self.game.screen, WHITE, vertical_line_right)
        pygame.draw.rect(self.game.screen, WHITE, horizontal_line_up)
        pygame.draw.rect(self.game.screen, WHITE, horizontal_line_down)
        
        pygame.draw.rect(self.game.screen, WHITE, paddle_left)
        pygame.draw.rect(self.game.screen, WHITE, paddle_right)
        
        # Ball
        pygame.draw.circle(self.game.screen, WHITE, (self.ball_x, self.ball_y), BALL_SIZE)
    
    # Draw the score board
    def draw_score_board(self):
        score_font = self.get_font(20)
        player_score_text = score_font.render("Player", 1, WHITE)
        computer_score_text = score_font.render("Computer", 1, WHITE)
        
        self.game.screen.blit(player_score_text, (self.game.screen_width//4 - player_score_text.get_width()//2, 20))
        self.game.screen.blit(computer_score_text, (3 * self.game.screen_width//4 - computer_score_text.get_width()//2, 20))
        
        player_score = score_font.render(f"{self.player_win}", 1, WHITE)
        computer_score = score_font.render(f"{self.computer_win}", 1, WHITE)
        
        self.game.screen.blit(player_score, (self.game.screen_width//4 - player_score.get_width()//2, 60))
        self.game.screen.blit(computer_score, (3 * self.game.screen_width//4 - computer_score.get_width()//2, 60))
        
    # Draw the Pong board on the game window
    def draw_board(self):    
        self.draw_grid()
        self.draw_score_board()
        
        win_font = self.get_font(25)
        # The computer wins the series if wins 5 games
        if self.computer_win == 5: 
            # Make the sound effect when the game is over
            self.gameover_sound.play()
            computer_win_text = win_font.render("Computer wins!!!", 1, WHITE)
            self.game.screen.blit(computer_win_text, (self.game.screen_width//2 - computer_win_text.get_width()//2, 40))
            self.game.pong_game_over = True
            
        # The human player wins the series if wins 5 games
        if self.player_win == 5: 
            # Make the sound effect when the game is over
            self.gameover_sound.play()
            player_win_text = win_font.render("Player wins!!!", 1, WHITE)
            self.game.screen.blit(player_win_text, (self.game.screen_width//2 - player_win_text.get_width()//2, 40))
            self.game.pong_game_over = True
            
        pygame.display.update()
        
    def render(self):
        # Render current state to the screen
        self.game.screen.blit(pygame.transform.scale(self.pong_background,(self.game.screen_width, self.game.screen_height)), (0,0))
    
        # Buttons
        back_button = button.Button(self.game.screen_width - BUTTON_WIDTH - 10, 10, 
                                 "Back", self.get_font(17), BLACK, BLUE, self.game.screen, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Back button to return to the pong difficulty screen
        if back_button.interact_button() == True:
            pygame.mixer.music.unload()  # Unload the game background music when go back to the Game Hub
            pygame.mixer.music.load(os.path.join('Assets', 'menu_music.mp3'))   # Load the Game Hub background music
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1) # Repeat the song indefinitely
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
        
        # Human player moves
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:         # Move up with 'w'
            self.left_paddle_y -= 4.75
        elif pressed[pygame.K_s]:       # Move down with 's'
            self.left_paddle_y += 4.75
        if pressed[pygame.K_UP]:        # Move up with UP arrow
            self.left_paddle_y -= 4.75
        elif pressed[pygame.K_DOWN]:    # Move down with DOWN arrow
            self.left_paddle_y += 4.75
            
        # Left paddle hits the top
        if self.left_paddle_y < self.game.screen_height//2 - BOARD_HEIGHT//2 + 5:
            self.left_paddle_y = self.game.screen_height//2 - BOARD_HEIGHT//2 + 5
            
        # Left paddle hits the bottom
        if self.left_paddle_y > self.game.screen_height//2 + BOARD_HEIGHT//2 - PADDLE_HEIGHT:
            self.left_paddle_y = self.game.screen_height//2 + BOARD_HEIGHT//2 - PADDLE_HEIGHT
        
        # AI Normal Mode
        if self.mode == 'normal':
            right_paddle_center = self.right_paddle_y + PADDLE_HEIGHT//2
            # Check if the y position of the AI paddle's center is lower than the ball's y position  
            if (right_paddle_center + 18 < self.ball_y) and (self.right_paddle_y < self.game.screen_height//2 + BOARD_HEIGHT//2 - PADDLE_HEIGHT): 
                # If it is lower, move the paddle down
                self.right_paddle_y += 4.75
                
            # Check if the y position of the AI paddle's center is higher than the ball's y position 
            if (right_paddle_center - 18 > self.ball_y + BALL_SIZE) and (self.right_paddle_y > self.game.screen_height//2 - BOARD_HEIGHT//2 + 5): 
                # If it is higher, move the paddle up
                self.right_paddle_y -= 4.75
                
        # AI Hard mode
        elif self.mode == 'hard':
            right_paddle_center = self.right_paddle_y + PADDLE_HEIGHT//2
            # Check if the y position of the AI paddle's center is lower than the ball's y position  
            if (right_paddle_center + 10 < self.ball_y) and (self.right_paddle_y < self.game.screen_height//2 + BOARD_HEIGHT//2 - PADDLE_HEIGHT): 
                # If it is lower, move the paddle down
                self.right_paddle_y += 4.75     
                
            # Check if the y position of the AI paddle's center is higher than the ball's y position  
            if (right_paddle_center - 10 > self.ball_y + BALL_SIZE) and (self.right_paddle_y > self.game.screen_height//2 - BOARD_HEIGHT//2 + 5): 
                # If it is higher, move the paddle up
                self.right_paddle_y -= 4.75
        
        # Ball has hit the top of the board
        if self.ball_y < self.game.screen_height//2 - BOARD_HEIGHT//2 + BALL_SIZE + 5: 
            # Make the sound effect when the ball hit the top of the board
            self.pong_sound.play()
            self.ball_y_momentum = BALL_MOMENTUM
            
        # Ball has hit the bottom of the board
        if self.ball_y > self.game.screen_height//2 + BOARD_HEIGHT//2 - BALL_SIZE: 
            # Make the sound effect when the ball hit the bottom of the board
            self.pong_sound.play()
            self.ball_y_momentum = -BALL_MOMENTUM
        
        # Human player loses if the ball gets through the player to the left edge
        if self.ball_x <= self.game.screen_width//2 - BOARD_WIDTH//2 + BALL_SIZE + 5: 
            self.computer_win += 1
            # Reset the ball
            self.ball_x = self.game.screen_width//2 + 5
            self.ball_y = self.game.screen_height//2
            self.ball_x_momentum = BALL_MOMENTUM - 1
            self.ball_y_momentum = BALL_MOMENTUM - 3
            
        # AI loses if the ball gets through the AI to the right edge
        if self.ball_x >= self.game.screen_width//2 + BOARD_WIDTH//2 - BALL_SIZE: 
            self.player_win += 1
            # Reset the ball
            self.ball_x = self.game.screen_width//2 + 5
            self.ball_y = self.game.screen_height//2
            self.ball_x_momentum = -(BALL_MOMENTUM - 1)
            self.ball_y_momentum = BALL_MOMENTUM - 3
        
        # Handle collisions between the ball and the paddles
        # The ball collides with the left paddle (human player)
        if (self.ball_x <= self.game.screen_width//2 - BOARD_WIDTH//2 + PADDLE_INSET + PADDLE_WIDTH + 5) and (self.ball_x > self.game.screen_width//2 - BOARD_WIDTH//2 + PADDLE_INSET):
            if self.ball_y + 3 >= self.left_paddle_y and self.ball_y -3<= self.left_paddle_y + PADDLE_HEIGHT:
                # Make the sound effect when the ball hit the paddle
                self.pong_sound.play()
                # Check if the ball collides to the top hafl of the left paddle
                if self.ball_y >= self.left_paddle_y and self.ball_y <= self.left_paddle_y + PADDLE_HEIGHT//2:
                    self.ball_x_momentum = BALL_MOMENTUM 
                    self.ball_y_momentum = -BALL_MOMENTUM 
                # Check if the ball collides to the bottom half of the left paddle
                elif self.ball_y >= self.left_paddle_y + PADDLE_HEIGHT//2 and self.ball_y <= self.left_paddle_y + PADDLE_HEIGHT:
                    self.ball_x_momentum = BALL_MOMENTUM 
                    self.ball_y_momentum = BALL_MOMENTUM
                    
        # The ball collides with the right paddle (AI player)
        if (self.ball_x >= self.game.screen_width//2 + BOARD_WIDTH//2 - PADDLE_INSET - PADDLE_WIDTH + 5) and (self.ball_x < self.game.screen_width//2 + BOARD_WIDTH//2 - PADDLE_INSET):
            if self.ball_y +3>= self.right_paddle_y and self.ball_y -3<= self.right_paddle_y + PADDLE_HEIGHT:
                # Make the sound effect when the ball hit the paddle
                self.pong_sound.play()
                # Check if the ball collides to the top half of the right paddle
                if self.ball_y >= self.right_paddle_y and self.ball_y <= self.right_paddle_y + PADDLE_HEIGHT//3:
                    self.ball_x_momentum = -BALL_MOMENTUM 
                    self.ball_y_momentum = -BALL_MOMENTUM 
                # Check if the ball collides to the bottom half of the right paddle
                elif self.ball_y >= self.right_paddle_y + PADDLE_HEIGHT//2 and self.ball_y <= self.right_paddle_y + PADDLE_HEIGHT:
                    self.ball_x_momentum = -BALL_MOMENTUM 
                    self.ball_y_momentum = BALL_MOMENTUM
         
        self.ball_x += self.ball_x_momentum
        self.ball_y += self.ball_y_momentum
        
    def load_assets(self):
        self.pong_background = pygame.image.load(os.path.join('Assets', 'cyberpunk_background3.jpg'))
        
        # Sound effects
        self.pong_sound = pygame.mixer.Sound(os.path.join('Assets', 'pong_sound1.wav'))
        self.gameover_sound = pygame.mixer.Sound(os.path.join('Assets', 'gameover_sound.wav'))

    def get_font(self, size):
        return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)