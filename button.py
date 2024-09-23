import pygame
from cell import cell_images, cell_cats

class MenuSubItem(pygame.sprite.Sprite):
    def __init__(self, id):
        self.image = cell_images[id].convert_alpha()
        self.id = id
        self.rect = self.image.get_rect()
        self.alpha = 0.5

    def update(self, mouse):
        import main
        if self.id in cell_cats[main.current_menu] and main.current_menu != -1:
            if self.rect.collidepoint(main.mouse_x, main.mouse_y):
                if mouse[0]:
                    main.brush = self.id
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False

    def draw(self, window):
        import main
        button_image = self.image.convert_alpha()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill((255, 255, 255, 255*self.alpha))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if self.id in cell_cats[main.current_menu] and main.current_menu != -1:
            self.rect.topleft = (main.toolbar_icon_rects[main.current_menu].x, main.toolbar_icon_rects[main.current_menu].y-20*cell_cats[main.current_menu].index(self.id)-27)
            main.window.blit(pygame.transform.rotate(button_image, -main.brush_dir*90), self.rect)

