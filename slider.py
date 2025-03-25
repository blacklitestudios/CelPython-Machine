import pygame
from cell import lerp

class Slider:
    def __init__(self, game, x, y, width, height, min_value, max_value, value):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.rect = pygame.Rect(x, y, width, height)
        self.slider_rect = pygame.Rect(x, y, width, height)
        self.slider_rect.width = 4
        self.slider_rect.x = lerp(self.x, self.x+width, (self.value-self.min_value)/(self.max_value-self.min_value))
    def update(self):
        mouse = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) and mouse[0]:
            self.value = lerp(self.min_value, self.max_value, (mouse_x-self.x)/self.width)
            self.slider_rect.x = mouse_x-5
            #self.slider_rect.x = max(self.x, min(self.x+self.width-10, self.slider_rect.x))
            
    def draw(self):
        pygame.draw.rect(self.game.window, (63, 63, 63), self.rect)
        pygame.draw.rect(self.game.window, (127, 127, 127), self.slider_rect)
        #pygame.draw.rect(self.game.window, (255, 255, 255), self.slider_rect, 2)
        #font = pygame.font.Font(None, 30)
        #text = font.render(str(self.value), True, (255, 255, 255))
        #iself.game.window.blit(text, (self.x+self.width+10, self.y))
        return self.value
    def get_value(self):
        return self.value
    