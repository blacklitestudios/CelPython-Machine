import pygame
from cell import cell_images, cell_cats


class MenuSubItem(pygame.sprite.Sprite):
    def __init__(self, id):
        self.image = cell_images[id].convert_alpha()
        self.id = id
        self.rect = self.image.get_rect()
        self.alpha = 0.5

        self.update((0, 0, 0), 0, 0, 0, 0)
        self.draw(pygame.Surface((1, 1)))

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        import main
        if self.id in cell_cats[current_menu] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    main.brush = self.id
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False

    def draw(self, window):
        from main import current_menu, brush_dir, toolbar_icon_rects
        button_image = self.image.convert_alpha()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill(pygame.Color(255, 255, 255, int(255*self.alpha)))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if self.id in cell_cats[current_menu] and current_menu != -1:
            self.rect.topleft = (toolbar_icon_rects[current_menu].x, toolbar_icon_rects[current_menu].y-20*cell_cats[current_menu].index(self.id)-27)
            window.blit(pygame.transform.rotate(button_image, -brush_dir*90), self.rect)

