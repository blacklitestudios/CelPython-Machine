import pygame
from cell import cell_images, cell_cats_new


class MenuSubItem(pygame.sprite.Sprite):
    def __init__(self, id):
        self.image = cell_images[id].convert_alpha()
        self.id = id
        self.rect = self.image.get_rect()
        self.alpha = 0.5

        '''self.update((0, 0, 0), 0, 0, 0, 1, 0)
        self.draw(pygame.Surface((1, 1)))'''

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu, current_submenu) -> bool: # type: ignore
        import main
        #from main import current_menu
        if current_menu == -1 or current_submenu == -1:
            return False
        if self.id in cell_cats_new[current_menu][current_submenu] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    main.brush = self.id
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False

    def draw(self, window):
        from main import current_menu, brush_dir, toolbar_icon_rects, current_submenu, toolbar_subcategories
        button_image = self.image.copy()
        if current_menu == -1 or current_submenu == -1:
            return False
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill(pygame.Color(255, 255, 255, int(255*self.alpha)))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        parent_button = toolbar_subcategories[cell_cats_new[current_menu][current_submenu][0]]
        if self.id in cell_cats_new[current_menu][current_submenu] and current_menu != -1 and current_submenu != -1:
            self.rect.topleft = (parent_button.rect.x+20*cell_cats_new[current_menu][current_submenu].index(self.id)+20, parent_button.rect.y)
            window.blit(pygame.transform.rotate(button_image, -brush_dir*90), self.rect)

class MenuSubCategory(pygame.sprite.Sprite):
    def __init__(self, id):
        self.image = cell_images[id].convert_alpha()
        self.id = id
        self.rect = self.image.get_rect()
        self.alpha = 0.5
        self.block = False

        self.update((0, 0, 0), 0, 0, 0, 0)
        self.draw(pygame.Surface((1, 1)))

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        import main
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False
    
    def handle_click(self, mouse, mouse_x, mouse_y, brush, current_menu):
        import main
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    cache = [i[0] for i in cell_cats_new[current_menu]].index(self.id)
                    if main.current_submenu == cache:
                        main.current_submenu = -1
                    else:
                        main.current_submenu = cache
                else:
                    self.block = True
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False
        

    def draw(self, window):
        from main import current_menu, brush_dir, toolbar_icon_rects
        button_image = self.image.copy()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill((255, 255, 255, 255*self.alpha))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            #print(int(255*self.alpha))
            self.rect.topleft = (toolbar_icon_rects[current_menu].x, toolbar_icon_rects[current_menu].y-20*[i[0] for i in cell_cats_new[current_menu]].index(self.id)-27)
            window.blit(pygame.transform.rotate(button_image, -brush_dir*90), self.rect)

class Button(pygame.sprite.Sprite):
    def __init__(self, img, size):
        self.image = pygame.transform.scale(pygame.image.load(f"textures/{img}").convert_alpha(), (40, 40))
        self.rect = self.image.get_rect()
        self.alpha = 0.5
        self.brightness = 255
        self.block = False

        #self.update((0, 0, 0), 0, 0, 0, 0)
        #self.draw(pygame.Surface((1, 1)))

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        from main import all_buttons
        if self.rect.collidepoint(mouse_x, mouse_y):
            all_buttons.append(True)
            if mouse[0]:
                self.brightness = 128
            else:
                self.brightness = 255
            self.alpha = 1
        else:
            self.alpha = 0.5

    def draw(self, window):
        from main import current_menu, brush_dir, toolbar_icon_rects
        button_image = self.image.copy()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill((self.brightness, self.brightness, self.brightness, 255*self.alpha))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        window.blit(pygame.transform.rotate(button_image, -brush_dir*90), self.rect)

    def handle_click(self, mouse, mouse_x, mouse_y, brush, current_menu):
        import main
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    cache = [i[0] for i in cell_cats_new[current_menu]].index(self.id)
                    if main.current_submenu == cache:
                        main.current_submenu = -1
                    else:
                        main.current_submenu = cache
                else:
                    self.block = True
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False


