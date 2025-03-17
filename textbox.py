import pygame

# thanks to github copilot for the following code #

class Textbox:
    def __init__(self, x: int, y: int, width: int, height: int, font_name: str, text:str ='', color_active: tuple[int, int, int]=(63, 63, 63), color_inactive: tuple[int, int, int]=(63, 63, 63), size=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = self.color_inactive
        if size:
            self.font = pygame.font.Font(font_name, size)
        else:
            self.font = pygame.font.Font(font_name, height-9)
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        #self.update()
        #self.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isdigit() and len(self.text) < 3:
                        self.text += event.unicode
                # Re-render the text.
        self.txt_surface = self.font.render(self.text+("_" if self.active else ""), True, (255, 255, 255))
        

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+3))
        # Blit the rect.
