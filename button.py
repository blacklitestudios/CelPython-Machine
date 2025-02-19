import pygame
from cell import cell_images, cell_cats_new


class MenuSubItem(pygame.sprite.Sprite):
    def __init__(self, id, game):
        self.image = cell_images[id].convert_alpha()
        self.id = id
        self.rect = self.image.get_rect()
        self.alpha = 0.5
        self.game = game

        '''self.update((0, 0, 0), 0, 0, 0, 1, 0)
        self.draw(pygame.Surface((1, 1)))'''

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu, current_submenu) -> bool: # type: ignore
        #from main import current_menu
        if current_menu == -1 or current_submenu == -1:
            return False
        if self.id in cell_cats_new[current_menu][current_submenu] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    self.game.brush = self.id
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False

    def draw(self, window):
        button_image = self.image.copy()
        if self.game.current_menu == -1 or self.game.current_submenu == -1:
            return False
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill(pygame.Color(255, 255, 255, int(255*self.alpha)))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        parent_button = self.game.toolbar_subcategories[cell_cats_new[self.game.current_menu][self.game.current_submenu][0]]
        if self.id in cell_cats_new[self.game.current_menu][self.game.current_submenu] and self.game.current_menu != -1 and self.game.current_submenu != -1:
            self.rect.topleft = (parent_button.rect.x+20*cell_cats_new[self.game.current_menu][self.game.current_submenu].index(self.id)+20, parent_button.rect.y)
            window.blit(pygame.transform.rotate(button_image, -self.game.brush_dir*90), self.rect)

class MenuSubCategory(pygame.sprite.Sprite):
    def __init__(self, id, game):
        self.image = cell_images[id].convert_alpha()
        self.id = id
        self.rect = self.image.get_rect()
        self.alpha = 0.5
        self.block = False
        self.game = game

        self.update((0, 0, 0), 0, 0, 0, 0)
        self.draw(pygame.Surface((1, 1)))

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False
    
    def handle_click(self, mouse, mouse_x, mouse_y, brush, current_menu):
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    cache = [i[0] for i in cell_cats_new[current_menu]].index(self.id)
                    if self.game.current_submenu == cache:
                        self.game.current_submenu = -1
                    else:
                        self.game.current_submenu = cache
                else:
                    self.block = True
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False
        

    def draw(self, window):
        #from main import current_menu, brush_dir, toolbar_icon_rects
        button_image = self.image.copy()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill((255, 255, 255, 255*self.alpha))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if self.id in [i[0] for i in cell_cats_new[self.game.current_menu]] and self.game.current_menu != -1:
            #print(int(255*self.alpha))
            self.rect.topleft = (self.game.toolbar_icon_rects[self.game.current_menu].x, self.game.toolbar_icon_rects[self.game.current_menu].y-20*[i[0] for i in cell_cats_new[self.game.current_menu]].index(self.id)-27)
            window.blit(pygame.transform.rotate(button_image, -self.game.brush_dir*90), self.rect)

class Button(pygame.sprite.Sprite):
    def __init__(self, game, img, size, rot=0, tint=(255, 255, 255)):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"textures/{img}").convert_alpha(), (size, size)), rot)
        self.rect = self.image.get_rect()
        self.alpha = 0.5
        self.brightness = 1
        self.tint = tint
        self.block = False
        self.game = game

        #self.update((0, 0, 0), 0, 0, 0, 0)
        #self.draw(pygame.Surface((1, 1)))

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        #from main import all_buttons
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.game.all_buttons.append(True)
            if mouse[0]:
                self.brightness = 0.5
            else:
                self.brightness = 1
            self.alpha = 1
        else:
            self.alpha = 0.5

    def draw(self, window):
        #from main import current_menu, brush_dir, toolbar_icon_rects
        button_image = self.image.copy()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill((self.brightness*self.tint[0], self.brightness*self.tint[1], self.brightness*self.tint[2], 255*self.alpha))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        window.blit(pygame.transform.rotate(button_image, -self.game.brush_dir*90*0), self.rect)

    def handle_click(self, mouse, mouse_x, mouse_y, brush, current_menu):
        #import main
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    cache = [i[0] for i in cell_cats_new[current_menu]].index(self.id)
                    if self.game.current_submenu == cache:
                        self.game.current_submenu = -1
                    else:
                        self.game.current_submenu = cache
                else:
                    self.block = True
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False
    

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, game, img, size, rot=0, tint=(255, 255, 255)):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"textures/{img}").convert_alpha(), (size, size)), rot)
        self.rect = self.image.get_rect()
        self.alpha = 0.5
        self.brightness = 1
        self.tint = tint
        self.block = False
        self.game = game

        #self.update((0, 0, 0), 0, 0, 0, 0)
        #self.draw(pygame.Surface((1, 1)))

    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        #from main import all_buttons, menu_on
        if self.rect.collidepoint(mouse_x, mouse_y):
            if self.game.menu_on:
                self.game.all_buttons.append(True)
            if mouse[0]:
                self.brightness = 0.5
            else:
                self.brightness = 1
            self.alpha = 1
        else:
            self.brightness = 1
            self.alpha = 0.5


    def draw(self, window):
        #from main import current_menu, brush_dir, toolbar_icon_rects
        button_image = self.image.copy()
        alpha_img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        alpha_img.fill((self.brightness*self.tint[0], self.brightness*self.tint[1], self.brightness*self.tint[2], 255*self.alpha))
        button_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        window.blit(pygame.transform.rotate(button_image, -self.game.brush_dir*90), self.rect)

    def handle_click(self, mouse, mouse_x, mouse_y, brush, current_menu):
        #import main
        if self.id in [i[0] for i in cell_cats_new[current_menu]] and current_menu != -1:
            if self.rect.collidepoint(mouse_x, mouse_y):
                if mouse[0]:
                    cache = [i[0] for i in cell_cats_new[current_menu]].index(self.id)
                    if self.game.current_submenu == cache:
                        self.game.current_submenu = -1
                    else:
                        self.game.current_submenu = cache
                else:
                    self.block = True
                self.alpha = 1
                return True
            else:
                self.alpha = 0.5
        return False

class ToolbarButton(Button):
    def update(self, mouse, mouse_x, mouse_y, brush, current_menu) -> bool: # type: ignore
        from main import all_buttons
        if self.rect.collidepoint(mouse_x, mouse_y):
            all_buttons.append(True)
            if mouse[0]:
                self.brightness = 0.5
            else:
                self.brightness = 1
            self.alpha = 1
        else:
            self.alpha = 1

    


