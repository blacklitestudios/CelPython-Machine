import pygame, sys
from cell import Cell, cell_images, rot_center
import json
from button import Button, MenuButton, MenuSubCategory, MenuSubItem

class CelPython:
    def __init__(self):
        import math
        self.math = math
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("CelPython Machine")
        self.icon = pygame.image.load(self.resource_path("textures/icon.png"))
        pygame.display.set_icon(self.icon)

        self.BACKGROUND = (31, 31, 31)
        self.tile_size = 20.0
        self.TOOLBAR_HEIGHT = 54

        self.clock = pygame.time.Clock()

        self.fps_font = self.nokia(6)

        self.menu_on = False

        self.scroll_speed = 250.0

        self.border_tile = 41
        self.step_speed = 0.2
        self.grid_width = 100
        self.grid_height = 100

        self.current_menu = 0
        self.suppress_place = False

        self.brush = 4
        self.brush_dir = 0
        self.selecting = False
        self.select_start = None
        self.select_end = None

        self.clipboard = {}
        self.clipboard_above = {}
        self.clipboard_below = {}
        self.show_clipboard = False
        self.clipboard_start = None
        self.clipboard_end = None
        self.clipboard_below = None
        self.clipboard_origin = None

        self.cam_x = 0.0
        self.cam_y = 0.0

        self.mouse_x = 0
        self.mouse_y = 0
        self.world_mouse_x = 0.0
        self.world_mouse_y = 0.0
        self.world_mouse_tile_x = 0
        self.world_mouse_tile_y = 0

        self.title = ""
        self.subtitle = ""

        self.border_tiles = [1, 41]

        self.paused = True
        self.tick_number = 0
        
        self.bg_image = pygame.image.load(self.resource_path("textures/bg.png"))
        self.bg_cache = {}

        self.tools_icon_image = pygame.transform.scale(pygame.image.load(self.resource_path("textures/eraser.png")), (40, 40))
        self.basic_icon_image = pygame.transform.scale(cell_images[4], (40, 40))
        self.movers_icon_image = pygame.transform.scale(cell_images[2], (40, 40))
        self.generators_icon_image = pygame.transform.scale(cell_images[3], (40, 40))
        self.rotators_icon_image = pygame.transform.scale(cell_images[9], (40, 40))
        self.forcers_icon_image = pygame.transform.scale(cell_images[21], (40, 40))
        self.divergers_icon_image = pygame.transform.scale(cell_images[16], (40, 40))
        self.destroyers_icon_image = pygame.transform.scale(cell_images[12], (40, 40))
        self.misc_icon_image = pygame.transform.scale(cell_images[20], (40, 40))

        self.menu_bg = pygame.image.load(self.resource_path("textures/menubg.png"))

        self.placeable_overlay = pygame.image.load(self.resource_path("textures/effects/placeableoverlay.png"))
        self.freeze_image = pygame.image.load(self.resource_path("textures/effects/frozen.png"))
        self.protect_image = pygame.image.load(self.resource_path("textures/effects/protected.png"))

        self.buttonz = pygame.sprite.Group()

        self.play_button: Button = Button(self, "mover.png", 40)
        self.play_button.rect.topright = (self.window_width-20, 20)
        self.pause_button: Button = Button(self, "slide.png", 40, -90)
        self.pause_button.rect.topright = (self.window_width-20, 20)
        self.step_button: Button = Button(self, "nudger.png", 40)
        self.step_button.rect.topright = (self.window_width-70, 20)
        self.initial_button: Button = Button(self, "timewarper.png", 40)
        self.initial_button.rect.topright = (self.window_width-70, 70)
        self.reset_button: Button = Button(self, "rotator_180.png", 40)
        self.reset_button.rect.topright = (self.window_width-20, 70)

        self.beep: pygame.mixer.Sound = pygame.mixer.Sound(self.resource_path("audio/beep.wav"))
        self.brush_image: pygame.Surface
        self.alpha_img: pygame.Surface

        self.menu_button = Button(self, "menu.png", 40)
        self.menu_button.rect.topleft = (20, 20)

        self.menu_bg_rect: pygame.Rect = self.menu_bg.get_rect()
        self.menu_bg_rect.center = (self.window_width//2, self.window_height//2) 

        self.update_timer: float = self.step_speed



        # Rects
        self.tools_icon_rect: pygame.Rect = self.tools_icon_image.get_rect()
        self.tools_icon_rect.midleft = (7, self.window_height - 27)

        self.basic_icon_rect: pygame.Rect = self.movers_icon_image.get_rect()
        self.basic_icon_rect.midleft = (7+1*54, self.window_height - 27)

        self.movers_icon_rect: pygame.Rect = self.movers_icon_image.get_rect()
        self.movers_icon_rect.midleft = (7+2*54, self.window_height - 27)

        self.generators_icon_rect: pygame.Rect = self.movers_icon_image.get_rect()
        self.generators_icon_rect.midleft = (7+3*54, self.window_height - 27)

        self.rotators_icon_rect: pygame.Rect = self.rotators_icon_image.get_rect()
        self.rotators_icon_rect.midleft = (7+4*54, self.window_height - 27)

        self.forcers_icon_rect: pygame.Rect = self.rotators_icon_image.get_rect()
        self.forcers_icon_rect.midleft = (7+5*54, self.window_height - 27)

        self.divergers_icon_rect: pygame.Rect = self.divergers_icon_image.get_rect()
        self.divergers_icon_rect.midleft = (7+6*54, self.window_height - 27)

        self.destroyers_icon_rect: pygame.Rect = self.destroyers_icon_image.get_rect()
        self.destroyers_icon_rect.midleft = (7+7*54, self.window_height - 27)

        self.misc_icon_rect: pygame.Rect = self.misc_icon_image.get_rect()
        self.misc_icon_rect.midleft = (7+9*54, self.window_height - 27)

        self.toolbar_icon_rects: list[pygame.Rect] = [self.tools_icon_rect, self.basic_icon_rect, self.movers_icon_rect, self.generators_icon_rect, self.rotators_icon_rect, self.forcers_icon_rect, self.divergers_icon_rect, self.destroyers_icon_rect, None, self.misc_icon_rect]
        self.toolbar_subicons: list[MenuSubItem] = []

        self.continue_button = MenuButton(self, "mover.png", 40)
        self.continue_button.rect.bottomleft = (self.window_width//2 - self.menu_bg_rect.width//2 + 32, self.window_height//2 + self.menu_bg_rect.height//2 - 32)

        self.menu_reset_button = MenuButton(self, "rotator_180.png", 40)
        self.menu_reset_button.rect.bottomleft = (self.window_width//2 - self.menu_bg_rect.width//2 + 32 + 50*1, self.window_height//2 + self.menu_bg_rect.height//2 - 32)

        self.clear_button = MenuButton(self, "trash.png", 40)
        self.clear_button.rect.bottomleft = (self.window_width//2 - self.menu_bg_rect.width//2 + 32 + 50*2, self.window_height//2 + self.menu_bg_rect.height//2 - 32)

        self.save_button = MenuButton(self, "generator.png", 40, rot=90)
        self.save_button.rect.bottomleft = (self.window_width//2 - self.menu_bg_rect.width//2 + 32 + 50*3, self.window_height//2 + self.menu_bg_rect.height//2 - 32)

        self.load_button = MenuButton(self, "pencil.png", 40)
        self.load_button.rect.bottomleft = (self.window_width//2 - self.menu_bg_rect.width//2 + 32 + 50*4, self.window_height//2 + self.menu_bg_rect.height//2 - 32)

        self.exit_button = MenuButton(self, "delete.png", 40, tint=(255, 128, 128))
        self.exit_button.rect.bottomright = (self.window_width//2 - self.menu_bg_rect.width//2 + 32 + 50*6, self.window_height//2 + self.menu_bg_rect.height//2 - 32)

        self.logo_image = pygame.image.load("textures/logo.png")
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.midbottom = (self.window_width//2, self.window_height//2)

        self.start_play_button: Button = Button(self, "mover.png", 60)
        self.start_play_button.rect.midtop = (self.window_width//2, self.logo_rect.bottom + 20)

        self.quit_button: Button = Button(self, "delete.png", 40, tint=(255, 128, 128))
        self.quit_button.rect.topright = (self.window_width - 20, 20)

        self.zoomin_button: Button = Button(self, "zoomin.png", 40)
        self.zoomin_button.rect.topleft = (70, 20)
        self.zoomout_button: Button = Button(self, "zoomout.png", 40)
        self.zoomout_button.rect.topleft = (120, 20)
        self.eraser_button: Button = Button(self, "eraser.png", 40)
        self.eraser_button.rect.topleft = (170, 20)
        self.select_button: Button = Button(self, "select.png", 40)
        self.select_button.rect.topleft = (20, 70)
        self.copy_button: Button = Button(self, "copy.png", 40)
        self.copy_button.rect.topleft = (70, 70)
        self.paste_button: Button = Button(self, "paste.png", 40)
        self.paste_button.rect.topleft = (120, 70)
        self.delete_button: Button = Button(self, "delete.png", 40)
        self.delete_button.rect.topleft = (170, 70)

        self.topleft_button_group = pygame.sprite.Group()
        self.topleft_button_group.add(self.menu_button, self.zoomin_button, self.zoomout_button, self.eraser_button, self.select_button, self.delete_button, self.copy_button, self.paste_button)

        # Create submenu icons
        cell_id: int | str
        for cell_id in cell_images.keys():
            self.toolbar_subicons.append(MenuSubItem(cell_id, self))

        self.toolbar_subcategories = {}
        for cell_id in cell_images.keys():
            self.toolbar_subcategories[cell_id] = (MenuSubCategory(cell_id, self))



            

        # Initialize cell maps
        self.cell_map: dict[tuple[int, int], Cell] = {}
        self.delete_map = []
        self.above: dict[tuple[int, int], Cell] = {}
        self.below: dict[tuple[int, int], Cell] = {}

        # Initial maps
        self.initial_cell_map: dict[tuple[int, int], Cell] = {}
        self.initial_above: dict[tuple[int, int], Cell] = {}
        self.initial_below: dict[tuple[int, int], Cell] = {}


        # Play music
        #pygame.mixer.music.load(resource_path("audio/scattered cells.ogg"))
        #pygame.mixer.music.play(-1)

        self.keys: list[bool]
        self.mouse_buttons: tuple[bool, bool, bool] = (False, False, False)
        self.current_submenu = -1

        # Create border tiles

        # Create top and bottom border tiles
        i: int
        for i in range(self.grid_width):
            self.cell_map[(i, -1)] = Cell(self, i, -1, self.border_tile, 0)
            self.cell_map[(i, self.grid_height)] = Cell(self, i, self.grid_height, self.border_tile, 0)
        
        # Create left and right border tiles
        for i in range(self.grid_height):
            self.cell_map[(-1, i)] = Cell(self, -1, i, self.border_tile, 0)
            self.cell_map[(self.grid_width, i)] = Cell(self, self.grid_width, i, self.border_tile, 0)

        # Create corner border tiles
            self.cell_map[(-1, -1)] = Cell(self, -1, -1, self.border_tile, 0)
            self.cell_map[(-1, self.grid_height)] = Cell(self, -1, self.grid_height, self.border_tile, 0)
            self.cell_map[(self.grid_width, -1)] = Cell(self, self.grid_width, -1, self.border_tile, 0)
            self.cell_map[(self.grid_width, self.grid_height)] = Cell(self, self.grid_width, self.grid_height, self.border_tile, 0)

        self.set_initial()

        # Text
        title_text: pygame.Surface = self.nokia(15).render("CelPython Machine", True, (255, 255, 255))
        title_rect = title_text.get_rect()
        title_rect.midbottom = (self.window_width//2, self.window_height//2)

        self.stepping = False

        self.t = 0

        # Loop-only variables
        self.all_buttons: list[bool] = []
        self.keys: list[bool]
        self.events: list[pygame.event.Event]
        self.event: pygame.event.Event

        # Main game loop
        self.running: bool = True
        self.screen = "title"

        self.all_buttons = []


    def set_initial(self):
        '''Sets the initial map to the current cell map.'''
        #global initial_cell_map, initial_above, initial_below, tick_number
        self.initial_cell_map = self.copy_map(self.cell_map)
        self.initial_above = self.copy_map(self.above)
        self.initial_below = self.copy_map(self.below)
        self.tick_number = 0

    def copy_map(self, cm: dict[tuple[int, int], Cell]) -> dict[tuple[int, int], Cell]:
        '''Deep-copies an entire cell map.'''
        result: dict[tuple[int, int], Cell] = {}
        key: tuple[int, int]
        value: Cell
        for key, value in zip(cm.keys(), cm.values()):
            result[key] = value.copy() # type: ignore
            value.tile_x = key[0]
            value.tile_y = key[1]

        return result


    def resource_path(self, relative_path):
        import os, sys
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def nokia(self, size):
        return pygame.font.Font(self.resource_path("nokiafc22.ttf"), size)
    
    def get_bg(self, size):
        if size in self.bg_cache.keys():
            return self.bg_cache[size]
        img = pygame.transform.scale(self.bg_image, (size, size))
        self.bg_cache[size] = img
        return img
    
    def place_cell(self, x: int, y: int, id: int | str, dir: int, layer: dict[tuple[int, int], Cell]):
        '''Place a cell on the cell map'''
        if not (x >= 0 and x < self.grid_width and y >= 0 and y < self.grid_height):
            return
        if (x, y) in layer.keys():
            # Target cell is not empty
            if id == 0:
                # New cell type is empty, erase cell
                del layer[(x, y)]
            else:
                # New cell type is not empty, replace cell
                layer[(x, y)] = Cell(self, x, y, id, dir, layer=layer)
        else:
            # Target cell is empty, add cell
            if id != 0:
                layer[(x, y)] = Cell(self, x, y, id, dir, layer=layer)

        if self.tick_number == 0:
            # Reset the initial state only if the current state is initial
            self.set_initial()

        return
    
    def get_cell(self, x: int, y: int) -> Cell:
        '''Get a cell from the map given the position'''
        if (x, y) in self.cell_map.keys():
            return self.cell_map[(x, y)]
        else:
            return Cell(self, x, y, 0, 0)
        
    def get_all_cells(self) -> list[Cell]:
        '''Gets all the cells with a given ID and a direction, and orders them for sub-sub-ticking.'''
                
        result: list[Cell] = []
        cell: Cell
        for cell in self.cell_map.values():
            if cell.tile_x < 0 or cell.tile_y < 0 or cell.tile_x >= self.grid_width or cell.tile_y >= self.grid_height:
                continue
            result.append(cell)

        return result
    
    def reverse(self, cell: Cell) -> int | float:
        if cell.tile_x < 0 or cell.tile_y < 0 or cell.tile_x >= self.grid_width or cell.tile_y >= self.grid_height:
            return float("-infinity")
        match cell.dir:
            case 0:
                return +cell.tile_x*self.grid_height - cell.tile_y
            case 1:
                return +cell.tile_y*self.grid_width + cell.tile_x
            case 2: 
                return -cell.tile_x*self.grid_height - cell.tile_y
            case 3:
                return -cell.tile_y*self.grid_width + cell.tile_x
        return float("-infinity")
    
    def forward(self, cell: Cell) -> int:
        if cell.tile_x < 0 or cell.tile_y < 0 or cell.tile_x >= self.grid_width or cell.tile_y >= self.grid_height:
            return float("-infinity")
        match cell.dir:
            case 0:
                return -cell.tile_x*self.grid_height + cell.tile_y
            case 1:
                return -cell.tile_y*self.grid_width - cell.tile_x
            case 2: 
                return +cell.tile_x*self.grid_height + cell.tile_y
            case 3:
                return +cell.tile_y*self.grid_width - cell.tile_x
        return float("-infinity")
    
    def tick(self):
        '''Ticks the entire map.'''
        # Reset the suppression values
        #global tick_number, delete_map
        cell: Cell
        for cell in self.cell_map.values():
            cell.suppressed = False
            cell.frozen = False
            cell.protected = False
            cell.old_x = cell.tile_x
            cell.old_y = cell.tile_y
            cell.old_dir = cell.dir
            cell.eat_top = False
            cell.eat_bottom = False
            cell.eat_left = False
            cell.eat_right = False
            cell.delta_dir = 0

        i: int


        self.delete_map = []

        # Do freezers (subtick 9)
        for i in range(4):
            for cell in self.cell_map.values():
                cell.do_freeze(i)

        # Do shields (subtick 10)
        for cell in self.cell_map.values():
            cell.do_protect()

        # Do mirrors (subtick 38 & 41)
        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_mirror(0, 4)

        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_mirror(1, 5)

        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_mirror(3, 7)

        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_mirror(2, 6)

        # Do intakers subticks 70 to 73
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_intake(i)

        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_bob()

        # Do generators subticks 90 to 93
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.reverse):
                cell.do_super_gen(i)

        # Do generators subticks 90 to 93
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.reverse):
                cell.do_gen(i)

        # Do replicators subticks 102 to 105
        for i in range(4):
            for cell in sorted(self.get_all_cells(), key=self.reverse):
                cell.do_replicate(i)

        # Do gears
        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_gear(1)

        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_gear(-1)

        # Do flippers (subtick 115)
        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_flip()

        # Do rotators
        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_rot()

        # Do redirectors
        for cell in sorted(self.get_all_cells(), key=self.forward):
            cell.do_redirect()
        
        # Do impulsors
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_impulse(i)

        # Do super repulsors
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_super_repulse(i)

        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_grapulse(i)

        # Do repulsors
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_repulse(i)

        # Do movers
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_drill(i)
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_pull(i)
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_grab(i)
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.reverse):
                cell.do_push(i)
        for i in [0, 2, 3, 1]:
            for cell in sorted(self.get_all_cells(), key=self.forward):
                cell.do_nudge(i)


        # Gates
        for cell in sorted(self.get_all_cells(), key=self.forward):
            for i in range(4):
                cell.do_gate(i)

        self.tick_number += 1

    def draw(self):
        # divergers
        cell: Cell
        if self.update_timer != 0:
            for cell in self.delete_map:
                cell.update()
                cell.draw()
        for cell in self.below.values(): 
            cell.update()
            cell.draw()
        for cell in self.cell_map.values(): 
            cell.update()
            cell.draw()

    def copy_map(self, cm: dict[tuple[int, int], Cell]) -> dict[tuple[int, int], Cell]:
        '''Deep-copies an entire cell map.'''
        result: dict[tuple[int, int], Cell] = {}
        key: tuple[int, int]
        value: Cell
        for key, value in zip(cm.keys(), cm.values()):
            result[key] = value.copy() # type: ignore
            value.tile_x = key[0]
            value.tile_y = key[1]

        return result
    
    def set_initial(self):
        '''Sets the initial map to the current cell map.'''
        #global initial_cell_map, initial_above, initial_below, tick_number
        self.initial_cell_map = self.copy_map(self.cell_map)
        self.initial_above = self.copy_map(self.above)
        self.initial_below = self.copy_map(self.below)
        self.tick_number = 0

    def reset(self):
        '''Resets the cell map to the initial cell map.'''
        #global cell_map, above, below, tick_number, paused
        self.cell_map = self.copy_map(self.initial_cell_map)
        self.below = self.copy_map(self.initial_below)
        self.above = self.copy_map(self.initial_above)
        for i in range(self.grid_width):
            self.cell_map[(i, -1)] = Cell(self, i, -1, self.border_tile, 0)
            self.cell_map[(i, self.grid_height)] = Cell(self, i, self.grid_height, self.border_tile, 0)

        # Create left and right border tiles
        for i in range(self.grid_height):
            self.cell_map[(-1, i)] = Cell(self, -1, i, self.border_tile, 0)
            self.cell_map[(self.grid_width, i)] = Cell(self, self.grid_width, i, self.border_tile, 0)

        # Create corner border tiles
            self.cell_map[(-1, -1)] = Cell(self, -1, -1, self.border_tile, 0)
            self.cell_map[(-1, self.grid_height)] = Cell(self, -1, self.grid_height, self.border_tile, 0)
            self.cell_map[(self.grid_width, -1)] = Cell(self, self.grid_width, -1, self.border_tile, 0)
            self.cell_map[(self.grid_width, self.grid_height)] = Cell(self, self.grid_width, self.grid_height, self.border_tile, 0)
        self.tick_number = 0
        self.paused = True


    def trash(self):
        #global cell_map, tick_number, paused
        self.cell_map = {}
        i: int
        for i in range(self.grid_width):
            self.cell_map[(i, -1)] = Cell(self, i, -1, self.border_tile, 0)
            self.cell_map[(i, self.grid_height)] = Cell(self, i, self.grid_height, self.border_tile, 0)

        # Create left and right border tiles
        for i in range(self.grid_height):
            self.cell_map[(-1, i)] = Cell(self, -1, i, self.border_tile, 0)
            self.cell_map[(self.grid_width, i)] = Cell(self, self.grid_width, i, self.border_tile, 0)

        # Create corner border tiles
            self.cell_map[(-1, -1)] = Cell(self, -1, -1, self.border_tile, 0)
            self.cell_map[(-1, self.grid_height)] = Cell(self, -1, self.grid_height, self.border_tile, 0)
            self.cell_map[(self.grid_width, -1)] = Cell(self, self.grid_width, -1, self.border_tile, 0)
            self.cell_map[(self.grid_width, self.grid_height)] = Cell(self, self.grid_width, self.grid_height, self.border_tile, 0)

        self.tick_number = 0
        self.paused = True

        self.below = {}
        self.above = {}

        self.set_initial()
        self.reset()

    def delete_selected(self):
        #global select_start, select_end, selecting
        for i in range(max(min(self.select_start[0], self.select_end[0]), 0), min(max(self.select_start[0]+1, self.select_end[0]+1), self.grid_width)):
            for j in range(max(min(self.select_start[1], self.select_end[1]), 0), min(max(self.select_start[1]+1, self.select_end[1]+1), self.grid_height)):
                if (i, j) in self.cell_map.keys():
                    del self.cell_map[(i, j)]
        self.select_start = None
        self.select_end = None
        self.selecting = False

    def copy_selected(self):
        #global select_start, select_end, selecting, clipboard_start, clipboard_end, clipboard_origin
        self.clipboard.clear()
        for i in range(max(min(self.select_start[0], self.select_end[0]), 0), min(max(self.select_start[0]+1, self.select_end[0]+1), self.grid_width)):
            for j in range(max(min(self.select_start[1], self.select_end[1]), 0), min(max(self.select_start[1]+1, self.select_end[1]+1), self.grid_height)):
                if (i, j) in self.cell_map.keys():
                    self.clipboard[i-self.world_mouse_tile_x, j-self.world_mouse_tile_y] = self.cell_map[i, j].copy()
        self.clipboard_start = (self.world_mouse_tile_x - self.select_start[0], self.world_mouse_tile_y - self.select_start[1])
        self.clipboard_end = (self.world_mouse_tile_x - self.select_end[0], self.world_mouse_tile_y - self.select_end[1])
        self.select_start = None
        self.select_end = None
        self.selecting = False

    def scroll_up(self, x, y):
        #global cam_x, cam_y, TILE_SIZE
        self.tile_size *= 2
        if self.tile_size > 160:
            self.tile_size = 160
        else:
            self.cam_x = (self.cam_x + x/2)*2
            self.cam_y = (self.cam_y + y/2)*2
    def scroll_down(self, x, y):
        #global cam_x, cam_y, TILE_SIZE
        self.tile_size /= 2
        if self.tile_size < 1.25:
            self.tile_size = 1.25
        else:
            self.cam_x = self.cam_x/2 - x/2
            self.cam_y = self.cam_y/2 - y/2

    def update(self):
        #print(self.world_mouse_tile_x, self.world_mouse_tile_y)
        WINDOW_HEIGHT = self.window.get_height()
        WINDOW_WIDTH = self.window.get_width()
        #all_buttons = []
                
        # Get pressed keys
        keys: list[bool]= pygame.key.get_pressed() # type: ignore

            # Get pressed mouse buttons
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Event loop
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                # Player wants to quit
                self.running = False

        if self.screen == "game":
            paste_falg = False
            continue_falg = False
            
            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    # Player is scrolling
                    if event.dict["y"] == -1:
                        # Scrolling down
                        self.scroll_down(mouse_x, mouse_y)
                    if event.dict["y"] == 1:
                        # Scrolling up
                        self.scroll_up(mouse_x, mouse_y)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(True not in self.all_buttons)
                    if self.selecting and event.dict["button"] == 1 and True not in self.all_buttons:
                        self.select_start = (self.world_mouse_tile_x, self.world_mouse_tile_y)
                        self.select_end = (self.world_mouse_tile_x, self.world_mouse_tile_y)
                    

                if event.type == pygame.MOUSEBUTTONUP:
                    
                    print(True not in self.all_buttons)
                    if self.selecting and event.dict["button"] == 1 and True not in self.all_buttons:
                        self.select_end = (self.world_mouse_tile_x, self.world_mouse_tile_y)

                    if self.show_clipboard and mouse_buttons[0]:
                        for pos, cell in zip(self.clipboard.keys(), self.clipboard.values()):
                            self.place_cell(self.world_mouse_tile_x + pos[0], self.world_mouse_tile_y + pos[1], cell.id, cell.dir, self.cell_map)
                        self.show_clipboard = False
                        self.all_buttons.append(True)
                        paste_falg = True
                    if True:
                        if self.tools_icon_rect.collidepoint(mouse_x, mouse_y):
                            self.brush = 0
                        elif self.basic_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 1:
                                self.current_menu = -1
                            else:
                                self.current_menu = 1
                            self.current_submenu = -1
                        elif self.movers_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 2:
                                self.current_menu = -1
                            else:
                                self.current_menu = 2
                            self.current_submenu = -1
                        elif self.generators_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 3:
                                self.current_menu = -1
                            else:
                                self.current_menu = 3
                            self.current_submenu = -1
                        elif self.rotators_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 4:
                                self.current_menu = -1
                            else:
                                self.current_menu = 4
                            self.current_submenu = -1
                        elif self.forcers_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 5:
                                self.current_menu = -1
                            else:
                                self.current_menu = 5
                            self.current_submenu = -1
                        elif self.divergers_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 6:
                                self.current_menu = -1
                            else:
                                self.current_menu = 6
                            self.current_submenu = -1
                        elif self.destroyers_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 7:
                                self.current_menu = -1
                            else:
                                self.current_menu = 7
                            self.current_submenu = -1
                        elif self.misc_icon_rect.collidepoint(mouse_x, mouse_y):
                            if self.current_menu == 9:
                                self.current_menu = -1
                            else:
                                self.current_menu = 9
                            self.current_submenu = -1
                        
                        elif self.play_button.rect.collidepoint(mouse_x, mouse_y):
                            paused = not paused
                        elif self.step_button.rect.collidepoint(mouse_x, mouse_y):
                            self.tick()
                        elif self.reset_button.rect.collidepoint(mouse_x, mouse_y):
                            self.beep.play()
                            self.reset()
                        elif self.initial_button.rect.collidepoint(mouse_x, mouse_y):
                            self.beep.play()
                            self.set_initial()
                        elif self.zoomin_button.rect.collidepoint(mouse_x, mouse_y):
                            self.scroll_up(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                        elif self.zoomout_button.rect.collidepoint(mouse_x, mouse_y):
                            self.scroll_down(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                        elif self.eraser_button.rect.collidepoint(mouse_x, mouse_y):
                            self.brush = 0
                        elif self.copy_button.rect.collidepoint(mouse_x, mouse_y):
                            print("copy")
                            self.copy_selected()
                        elif self.paste_button.rect.collidepoint(mouse_x, mouse_y):
                            self.show_clipboard = not self.show_clipboard
                        elif self.select_button.rect.collidepoint(mouse_x, mouse_y):
                            self.selecting = not self.selecting
                            if not self.selecting:
                                self.select_start = None
                                self.select_end = None
                            self.show_clipboard = False
                        elif self.delete_button.rect.collidepoint(mouse_x, mouse_y):
                            if self.selecting and self.select_start != None and self.select_end != None:
                                self.delete_selected()

                        elif self.menu_button.rect.collidepoint(mouse_x, mouse_y):
                            self.menu_on = not self.menu_on
                        elif self.continue_button.rect.collidepoint(mouse_x, mouse_y) and self.menu_on:
                            self.menu_on = False
                            self.all_buttons.append(True)
                            continue_falg = True
                            self.beep.play()
                        elif self.exit_button.rect.collidepoint(mouse_x, mouse_y) and self.menu_on:
                            self.beep.play()
                            self.screen = "title"

                        elif self.menu_reset_button.rect.collidepoint(mouse_x, mouse_y) and self.menu_on:
                            self.beep.play()
                            self.reset()

                        elif self.clear_button.rect.collidepoint(mouse_x, mouse_y) and self.menu_on:
                            self.beep.play()
                            self.trash()

                        elif self.save_button.rect.collidepoint(mouse_x, mouse_y) and self.menu_on:
                            self.save_map()

                        elif self.load_button.rect.collidepoint(mouse_x, mouse_y) and self.menu_on:
                            self.load_map()

                        if event.dict["button"] == 2:
                            picked_cell = self.get_cell(self.world_mouse_tile_x, self.world_mouse_tile_y)
                            self.brush = picked_cell.id
                            self.brush_dir = picked_cell.dir

                        for button in self.toolbar_subicons:
                            button.update(mouse_buttons, mouse_x, mouse_y, self.brush, self.current_menu, self.current_submenu)
                        for button in self.toolbar_subcategories.values():
                            button.handle_click(mouse_buttons, mouse_x, mouse_y, self.brush, self.current_menu)


                else:
                    if mouse_buttons[0]:
                        self.select_end = (self.world_mouse_tile_x, self.world_mouse_tile_y)



                        
                
                if event.type == pygame.KEYDOWN:
                    if event.dict["key"] == pygame.K_q:
                        self.brush_dir -= 1
                        self.brush_dir = self.brush_dir % 4
                    if event.dict["key"] == pygame.K_e:
                        self.brush_dir += 1
                        self.brush_dir = self.brush_dir % 4

                    if event.dict["key"] == pygame.K_f:
                        self.tick()
                        self.stepping = True
                        self.update_timer = self.step_speed

                    if event.dict["key"] == pygame.K_t:
                        if (self.world_mouse_tile_x, self.world_mouse_tile_y) in self.cell_map.keys():
                            self.save_map()
                    
                    if event.dict["key"] == pygame.K_3:
                        #if (self.world_mouse_tile_x, self.world_mouse_tile_y) in self.cell_map.keys():
                            self.load_map()
                    
                    if event.dict["key"] == pygame.K_r:
                        if keys[pygame.K_LCTRL] or keys[ pygame.K_LMETA]:
                            self.beep.play()
                            self.reset()
                    if event.dict["key"] == pygame.K_c:
                        if keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]:
                            self.copy_selected()
                    if event.dict["key"] == pygame.K_v:
                        if keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]:
                            self.show_clipboard = not self.show_clipboard

                    if event.dict["key"] == pygame.K_ESCAPE:
                        self.menu_on = not self.menu_on

                    if event.dict["key"] == pygame.K_SPACE:
                        if self.paused:
                            self.tick()
                            self.update_timer = self.step_speed
                        self.paused = not self.paused
                    if event.dict["key"] == pygame.K_TAB:
                        self.selecting = not self.selecting
                        if not self.selecting:
                            self.select_start = None
                            self.select_end = None
                        self.show_clipboard = False
                    if event.dict["key"] == pygame.K_BACKSPACE:
                        if self.selecting:
                            self.delete_selected()



            # Press CTRL to speed up scrolling
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                scroll_speed = 500
            else:
                scroll_speed = 250
            
            # WASD to move the camera
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.cam_y -= scroll_speed*self.dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.cam_x -= scroll_speed*self.dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.cam_y += scroll_speed*self.dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.cam_x += scroll_speed*self.dt



            self.world_mouse_x = mouse_x + self.cam_x
            self.world_mouse_y = mouse_y + self.cam_y
            self.world_mouse_tile_x = int(self.world_mouse_x//self.tile_size)
            self.world_mouse_tile_y = int(self.world_mouse_y//self.tile_size)

            self.step_button.rect.topright =(WINDOW_WIDTH - 70, 20)
            self.play_button.rect.topright = (WINDOW_WIDTH - 20, 20)
            self.pause_button.rect.topright = (WINDOW_WIDTH - 20, 20)
            self.reset_button.rect.topright = (WINDOW_WIDTH - 20, 70)
            self.initial_button.rect.topright = (WINDOW_WIDTH - 70, 70)

            self.all_buttons = []
            self.step_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.reset_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.initial_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            for i in self.topleft_button_group:
                i.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            if self.selecting:
                self.select_button.tint = (128, 255, 128)
            else:
                self.select_button.tint = (255, 255, 255)
            self.continue_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.exit_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.menu_reset_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.clear_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.save_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.load_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)

            




            # Check for a press suppression
            button: MenuSubItem
            for button in self.toolbar_subicons:
                self.all_buttons.append(button.update(mouse_buttons, mouse_x, mouse_y, self.brush, self.current_menu, self.current_submenu))
            for button in self.toolbar_subcategories.values():
                self.all_buttons.append(button.update(mouse_buttons, mouse_x, mouse_y, self.brush, self.current_menu))

            if True in self.all_buttons:
                self.suppress_place = True
            else:
                self.suppress_place = False

            # Place tiles if possible

            if not self.selecting and not self.show_clipboard and not paste_falg and not continue_falg:
                if mouse_y < WINDOW_HEIGHT - 54 and not self.suppress_place:       
                    if mouse_buttons[0]:
                        if "placeable" in str(self.brush):
                            self.place_cell(self.world_mouse_tile_x, self.world_mouse_tile_y, self.brush, self.brush_dir, self.below)
                        else:
                            self.place_cell(self.world_mouse_tile_x, self.world_mouse_tile_y, self.brush, self.brush_dir, self.cell_map)
                    if mouse_buttons[2]:
                        if (self.world_mouse_tile_x, self.world_mouse_tile_y) in self.above.keys():
                            self.place_cell(self.world_mouse_tile_x, self.world_mouse_tile_y, 0, 0, self.above)
                        elif (self.world_mouse_tile_x, self.world_mouse_tile_y) in self.cell_map.keys():
                            self.place_cell(self.world_mouse_tile_x, self.world_mouse_tile_y, 0, 0, self.cell_map)
                        elif (self.world_mouse_tile_x, self.world_mouse_tile_y) in self.below.keys():
                            self.place_cell(self.world_mouse_tile_x, self.world_mouse_tile_y, 0, 0, self.below)

            
            # Reset background
            self.window.fill(self.BACKGROUND, self.window.get_rect())

            # Get border tile image
            border_image = cell_images[self.border_tile]

            i: int
            j: int
            for i in range(self.grid_width):
                for j in range(self.grid_height):
                    if not (self.tile_size*i-self.cam_x+self.tile_size < 0 or self.tile_size*i-self.cam_x > WINDOW_WIDTH or self.tile_size*j-self.cam_y+self.tile_size < 0 or self.tile_size*j-self.cam_y > WINDOW_HEIGHT):
                        #if (i, j) not in cell_map.keys():
                            self.window.blit(self.get_bg(self.tile_size), (self.tile_size*i-self.cam_x, self.tile_size*j-self.cam_y))


            self.draw()
            
            if self.selecting and self.select_start != None and self.select_end != None:
                s = pygame.Surface((abs(self.select_end[0]-self.select_start[0])*self.tile_size+self.tile_size, abs(self.select_end[1]-self.select_start[1])*self.tile_size+self.tile_size), pygame.SRCALPHA)
                s.set_alpha(64)
                s.fill((255, 255, 255))
                self.window.blit(s, (min(self.select_start[0]*self.tile_size-self.cam_x, self.select_end[0]*self.tile_size-self.cam_x), min(self.select_start[1]*self.tile_size-self.cam_y, self.select_end[1]*self.tile_size-self.cam_y)))
            if self.show_clipboard and self.clipboard_start != None and self.clipboard_end != None:
                s = pygame.Surface((abs(self.clipboard_end[0]-self.clipboard_start[0])*self.tile_size+self.tile_size, abs(self.clipboard_end[1]-self.clipboard_start[1])*self.tile_size+self.tile_size), pygame.SRCALPHA)
                #print(self.clipboard)
                tlcorner = (min((-self.clipboard_start[0]+self.world_mouse_tile_x), (-self.clipboard_end[0]+self.world_mouse_tile_x)), min((-self.clipboard_start[1]+self.world_mouse_tile_y), (-self.clipboard_end[1]+self.world_mouse_tile_y)))
                anchor = (tlcorner[0] - self.world_mouse_tile_x, tlcorner[1] - self.world_mouse_tile_y)


                s.fill((255, 255, 255, 128))
                for key, tile in zip(self.clipboard.keys(), self.clipboard.values()):
                    s.blit(tile.loadscale(self.tile_size), ((key[0]-anchor[0])*self.tile_size, (key[1]-anchor[1])*self.tile_size))
                s.set_alpha(128)

                self.window.blit(s, (min((-self.clipboard_start[0]+self.world_mouse_tile_x)*self.tile_size-self.cam_x, (-self.clipboard_end[0]+self.world_mouse_tile_x)*self.tile_size-self.cam_x), min((-self.clipboard_start[1]+self.world_mouse_tile_y)*self.tile_size-self.cam_y, (-self.clipboard_end[1]+self.world_mouse_tile_y)*self.tile_size-self.cam_y)))


            if not self.selecting and not self.show_clipboard:
                # Draw brush image
                brush_image = cell_images[self.brush].convert_alpha()
                alpha_img = pygame.Surface(brush_image.get_rect().size, pygame.SRCALPHA)
                alpha_img.fill((255, 255, 255, 255*0.25)) # type: ignore
                brush_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                if True not in self.all_buttons:
                    self.window.blit(pygame.transform.rotate(pygame.transform.scale(brush_image, (self.tile_size, self.tile_size)), -90*self.brush_dir), (self.world_mouse_tile_x*self.tile_size-self.cam_x, self.world_mouse_tile_y*self.tile_size-self.cam_y))

            # Draw bottom toolbar
            pygame.draw.rect(self.window, (60, 60, 60), pygame.Rect(-10, WINDOW_HEIGHT-self.TOOLBAR_HEIGHT, WINDOW_WIDTH+20, self.TOOLBAR_HEIGHT+10))
            pygame.draw.rect(self.window, (127, 127, 127), pygame.Rect(-10, WINDOW_HEIGHT-self.TOOLBAR_HEIGHT, WINDOW_WIDTH+20, self.TOOLBAR_HEIGHT+10), 1)

            # Update toolbar positions\
            self.tools_icon_rect.midleft = (7, WINDOW_HEIGHT - 27)
            self.basic_icon_rect.midleft = (7+1*54, WINDOW_HEIGHT - 27)
            self.movers_icon_rect.midleft = (7+2*54, WINDOW_HEIGHT - 27)
            self.generators_icon_rect.midleft = (7+3*54, WINDOW_HEIGHT - 27)
            self.rotators_icon_rect.midleft = (7+4*54, WINDOW_HEIGHT - 27)
            self.forcers_icon_rect.midleft = (7+5*54, WINDOW_HEIGHT - 27)
            self.divergers_icon_rect.midleft = (7+6*54, WINDOW_HEIGHT - 27)
            self.destroyers_icon_rect.midleft = (7+7*54, WINDOW_HEIGHT - 27)
            self.misc_icon_rect.midleft = (7+9*54, WINDOW_HEIGHT - 27)
            # Blit toolbar icons
            self.window.blit(pygame.transform.rotate(self.tools_icon_image, 0), self.tools_icon_rect)
            self.window.blit(pygame.transform.rotate(self.basic_icon_image, -90*self.brush_dir), self.basic_icon_rect)
            self.window.blit(pygame.transform.rotate(self.movers_icon_image, -90*self.brush_dir), self.movers_icon_rect)
            self.window.blit(pygame.transform.rotate(self.generators_icon_image, -90*self.brush_dir), self.generators_icon_rect)
            self.window.blit(pygame.transform.rotate(self.rotators_icon_image, -90*self.brush_dir), self.rotators_icon_rect)
            self.window.blit(pygame.transform.rotate(self.forcers_icon_image, -90*self.brush_dir), self.forcers_icon_rect)
            self.window.blit(pygame.transform.rotate(self.divergers_icon_image, -90*self.brush_dir), self.divergers_icon_rect)
            self.window.blit(pygame.transform.rotate(self.destroyers_icon_image, -90*self.brush_dir), self.destroyers_icon_rect)
            self.window.blit(pygame.transform.rotate(self.misc_icon_image, -90*self.brush_dir), self.misc_icon_rect)

            for button in self.toolbar_subicons:
                button.draw(self.window)
            for button in self.toolbar_subcategories.values():
                button.update(mouse_buttons, mouse_x, mouse_y, self.brush, self.current_menu)
                button.draw(self.window)
            if self.paused:
                self.play_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
                self.play_button.draw(self.window)
            else:
                self.pause_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
                self.pause_button.draw(self.window)

            
            self.step_button.draw(self.window)       
            self.reset_button.draw(self.window)       
            self.initial_button.draw(self.window)       
            for i in self.topleft_button_group:
                i.draw(self.window)

            self.menu_bg_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            

            if self.menu_on:
                self.window.blit(self.menu_bg, self.menu_bg_rect)
                self.continue_button.draw(self.window)

                self.exit_button.draw(self.window)

                self.menu_reset_button.draw(self.window)

                self.clear_button.draw(self.window)
                self.save_button.draw(self.window)
                self.load_button.draw(self.window)



                update_delay_text = self.nokia(10).render(f"Update delay: {self.step_speed}", True, (255, 255, 255))
                update_delay_rect = update_delay_text.get_rect()
                update_delay_rect.topleft = (self.menu_bg_rect.x + 20, self.menu_bg_rect.y + 40)
                self.window.blit(update_delay_text, update_delay_rect)





            


        elif self.screen == "title":
            # Event loop
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouse_buttons[0] and self.start_play_button.rect.collidepoint(mouse_x, mouse_y):
                        self.screen = "game"
                        self.trash()
                        self.menu_on = False
                        self.tile_size = 20.0
                        self.cam_x = 0
                        self.cam_y = 0
                    if mouse_buttons[0] and self.quit_button.rect.collidepoint(mouse_x, mouse_y):
                        self.running = False
            self.window.fill(self.BACKGROUND, self.window.get_rect())
            #logo_image, _ = rot_center(logo_image, logo_rect, math.sin(t))
            self.logo_rect.midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            self.window.blit(rot_center(self.logo_image, self.logo_rect, self.math.sin(self.t)*5)[0], rot_center(self.logo_image, self.logo_rect, self.math.sin(self.t)*5)[1])       

            self.start_play_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.start_play_button.draw(self.window)

            self.quit_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            self.quit_button.draw(self.window)

        self.clock.tick()
        self.dt = self.clock.get_time() / 1000
        self.t+=self.dt
        if not self.paused:
            if self.dt > self.step_speed:
                self.update_timer = 0
            else:
                self.update_timer -= self.dt
            if self.update_timer <= 0:
                self.update_timer += self.step_speed
                if self.update_timer < 0:
                    self.update_timer = 0
                    
                self.tick()
        else:
            if self.update_timer > 0:
                self.update_timer -= self.dt
            else:
                self.update_timer = 0

        if self.screen == "game":
            if (self.world_mouse_tile_x, self.world_mouse_tile_y) in self.cell_map.keys():
                disp = self.cell_map[self.world_mouse_tile_x, self.world_mouse_tile_y].__repr__()
            else:
                disp = str((self.world_mouse_tile_x, self.world_mouse_tile_y))
            coord_text = self.fps_font.render(f"{disp}", True, (255, 255, 255))
            coord_rect = coord_text.get_rect()
            coord_rect.topright = (WINDOW_WIDTH, 4)
            self.window.blit(self.fps_font.render(f"FPS: {str(self.clock.get_fps())}", True, (255, 255, 255)), (0, 4))
            self.window.blit(self.fps_font.render(f"Tick: {str(self.tick_number)}", True, (255, 255, 255)), (0, 13))
            self.window.blit(coord_text, coord_rect)
        # Update the display
        pygame.display.update()

    def save_map(self):
        from encoding import base84, cheatsheet
        from zlib import compress
        import base64
        import pyperclip
        currentcell = 0
        result = "K3::;"
        result = result+base84(self.grid_width)+";"+base84(self.grid_height)+';'
        result = result+base84(self.border_tiles.index(self.border_tile))+';'
        cellcode = ""
        cellcodes = {}
        for y in range(0, self.grid_height):
            cellcodes[y] = ""
            for x in range(0, self.grid_width):
                for layer in range(0, 2):
                    '''if (x, y) in layer.keys():
                        cell = [self.below, self.cell_map, self.above][layer][x, y]
                    else'''
                    c = self.get_cell(x, y, layer)
                    if c.id != 0 or layer == 0:
                        if c.id != 0 or (x, y) in self.below.keys() :
                            pass
                        if layer == 0:
                            c=self.encode_cell(x, y, 0)
                        else:
                            c=self.encode_raw_cell(c)

                        cellcodes[y] = cellcodes[y]+("\\"+cheatsheet[layer] if layer != 0  else "")+c	#please tell me we wont have more than 84 layers

        for i in range(len(cellcodes)):
            cellcode = cellcode+cellcodes[i]

        with open("cellcode.txt", "w") as f:
            f.write(cellcode)
        cellcode = base64.b64encode(compress(str.encode(cellcode),9)).decode("utf-8")
        result = result + cellcode + ";"
        print(result)
        pyperclip.copy(result)

    def decode_K3(self, code):
        from encoding import unbase84, cheatsheet, reverse_cheatsheet
        from zlib import decompress
        import base64
        if code[:5] != "K3::;":
            return
        charindex = 5 # start after K3::;

        # Read width
        readstring = ""
        while code[charindex] != ";":
            readstring+=code[charindex]
            charindex += 1
        self.grid_width = unbase84(readstring)

        # Read height
        readstring = ""
        charindex += 1
        while code[charindex] != ";":
            readstring+=code[charindex]
            charindex += 1
        self.grid_height = unbase84(readstring)

        # Read border tile
        readstring = ""
        charindex += 1
        while code[charindex] != ";":
            readstring+=code[charindex]
            charindex += 1
        self.border_tile = self.border_tiles[unbase84(readstring)]

        # Read cell code
        readstring = ""
        charindex += 1
        while code[charindex] != ";":
            readstring+=code[charindex]
            charindex += 1

        cellcode = decompress(base64.b64decode(readstring)).decode("utf-8")
        charindex = 0
        cellindex = 0
        readstring = ""

        self.trash()
        layer = 99
        while True:
            oldlayer = layer
            if charindex >= len(cellcode):
                break
            if cellcode[charindex] == "\\":
                charindex += 1
                layer = reverse_cheatsheet[cellcode[charindex]]
                #charindex += 1

            elif cellcode[charindex] == "]":
                charindex += 1
                layer = -1
                #cellindex -= 1

            else:
                layer = 0
                #cellindex += 1

            if cellcode[charindex] == "(":
                charindex += 1
                cellidrot = unbase84(cellcode[charindex:charindex+2])
                charindex += 2
                cellid = cellidrot // 4
                cellrot = cellidrot %4
            elif cellcode[charindex] == ")":
                charindex += 1
                idrot_length = unbase84(cellcode[charindex])
                charindex += 1
                cellidrot = cellcode[charindex:charindex+idrot_length]
                charindex += idrot_length
                cellid = cellidrot // 4
                cellrot = cellidrot % 4
            elif cellcode[charindex] == "<":
                charindex += 1
                readstring = ""
                while cellcode[charindex] != "<":
                    readstring += cellcode[charindex]
                    charindex += 1
                cellid = readstring
                charindex += 1
                cellrot = int(cellcode[charindex])
            else:
                cellidrot = unbase84(cellcode[charindex])
                cellid = cellidrot // 4
                cellrot = cellidrot % 4
                charindex += 1
            if cellid != 0:
                pass
            vars = {}
            if charindex >= len(cellcode):
                break
            if cellcode[charindex] == "[":
                charindex += 1

                while True:
                    key = unbase84(cellcode[charindex])
                    charindex += 1
                    if cellcode[charindex] == "(":
                        charindex += 1
                        decoded = unbase84(cellcode[charindex:charindex+2])
                        charindex += 2
                    elif cellcode[charindex] == ")":
                        charindex += 1
                        idrot_length = unbase84(cellcode[charindex])
                        charindex += 1
                        decoded = cellcode[charindex:charindex+idrot_length]
                        charindex += idrot_length

                    elif cellcode[charindex] == "<":
                        charindex += 1
                        readstring = ""
                        while cellcode[charindex] != "<":
                            readstring += cellcode[charindex]
                            charindex += 1
                        decoded = readstring

                    else:
                        decoded = unbase84(cellcode[charindex])
                        charindex += 1

                    vars[key] = decoded

                    if cellcode[charindex] == "[":
                        charindex += 1
                    else:
                        break

            cell = Cell(self, cellindex % self.grid_width, cellindex // self.grid_width, cellid, cellrot)
            cell.set_vars(vars)
            cell.layer = {0: self.cell_map, 1: self.above, -1: self.below}[layer]

            

            if cellid != 0:
                match layer:
                    case -1:
                        self.below[cellindex % self.grid_width, cellindex // self.grid_width] = cell
                    case 1:
                        self.above[cellindex % self.grid_width, cellindex // self.grid_width] = cell
                    case _:
                        self.cell_map[cellindex % self.grid_width, cellindex // self.grid_width] = cell

            if layer <= oldlayer:
                cellindex += 1


        

        self.set_initial()



            
            
            


    def get_cell(self, x, y, z):
        if z == 0:
            return self.cell_map[x, y] if (x, y) in self.cell_map.keys() else Cell(self, x, y, 0, 0)
        elif z == 1:
            return self.above[x, y] if (x, y) in self.above.keys() else Cell(self, x, y, 0, 0)
        elif z == -1:
            return self.below[x, y] if (x, y) in self.below.keys() else Cell(self, x, y, 0, 0)
                        
    def encode_cell(self, x, y, l):
        from encoding import base84
        map = [self.initial_below, self.initial_cell_map, self.initial_above][l]
        cell: Cell = self.get_cell(x, y, l)
        code = ""
        id = cell.id
        rot = cell.dir
        if type(id) is int:
            code = self.encode_data(id*4+rot)
        elif type(id) is str:
            code = "<"+id+"<"+(str(rot))
        if cell.as_dict():
            for k, v in enumerate(cell.as_dict()):
                code = code+"["+self.encode_data(k)+self.encode_data(v)

        if (x, y) in self.initial_below.keys():
            code = "]"+self.encode_raw_cell(self.initial_below[x, y])+code

        return code
    
    def decode_cell(self, string):
        if string[0] == "<":
            string = string[1:-1]
            rot = string[-1]
            id = string[:-1]
            cell = Cell(self, 0, 0, id, rot)
        elif string[0] == "":
            decoded_rotid = self.decode_data(string)
            rot = decoded_rotid % 4
            id = decoded_rotid // 4
            cell = Cell(self, 0, 0, id, rot)

        return cell
    
    def encode_raw_cell(self, cell: Cell):
        #cell: Cell = self.get_cell(x, y, l)
        code = ""
        id = cell.id
        rot = cell.dir
        if type(id) is int:
            code = self.encode_data(id*4+rot)
        elif type(id) is str:
            code = "<"+id+"<"+("" if ("placeable" in id or "bg" in id) else str(rot))
        if cell.as_dict():
            for k, v in enumerate(cell.as_dict()):
                code = code+"["+self.encode_data(k)+self.encode_data(v)

        return code
        
            
    def encode_data(self, data)->str:
        from encoding import base84
        if type(data) is int:
            code = base84(data)
            if len(code) > 2:	
                code = ")"+len(code)+code	
            elif len(code) > 1:	
                code = "("+code	
            return code
        elif type(data) is str:
            #return "<"+string.gsub(string.gsub(data,"\\","\\\\"),"<","\\<").."<"	
            return "<"+str.replace(str.replace(data, "\\", "\\\\"), "<", "\\<")+"<"
        elif type(data) is bool and data:
            return "1"
        return "0"
        
    def decode_data(self, code):
        from encoding import unbase84
        if code[0] == "<":
            string_code = code[1:-1]
            string_code = str.replace(string_code, "\\<", "<")  
            string_code = str.replace(string_code, "\\\\", "\\")
            return string_code
        elif code[0] == "(":
            return unbase84(code[1:])
        elif code[0] == ")":
            return unbase84(code[2:])
        elif code == "1":
            return True
        
    def load_map(self):
        import pyperclip
        self.decode_K3(pyperclip.paste())
        
    

            


    def play(self):
        while self.running:
            self.update()

        pygame.quit()
        sys.exit()

