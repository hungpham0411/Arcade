import pygame

WHITE = (255,255,255)

class Button:
    def __init__(self, x, y, text, font, base_color, hovering_color, surface, width, height):
        self.x = x     # Position x on the board
        self.y = y     # Postion y on the board
        self.font = font
        self.text = self.font.render(text, True, WHITE)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.surface = surface # The window that contains the button
        self.width = width     # The width of the button
        self.height = height   # The height of the button
        self.rect = pygame.draw.rect(self.surface, self.base_color, (self.x, self.y, self.width, self.height))
        self.text_rect = self.text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        surface.blit(self.text, self.text_rect)
        
    def draw_button(self, surface):
        action = False

        # Get mouse position
        mouse_position = pygame.mouse.get_pos()
       
        # Check hover and clicked conditions
        if self.rect.collidepoint(mouse_position):
            self.rect = pygame.draw.rect(self.surface, self.hovering_color, (self.x, self.y, self.width, self.height))
            surface.blit(self.text, self.text_rect)
            if pygame.mouse.get_pressed()[0] == 1:
               action = True
               
        return action
        