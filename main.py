import pygame, sys
import math
from cell import Cell, cell_images, rot_center
import cell
from sometypes import void, Void

from button import MenuSubItem, MenuSubCategory, Button, ToolbarButton, MenuButton

# Initialize pygame
pygame.init()


def place_cell(x: int, y: int, id: int | str, dir: int, layer: dict[tuple[int, int], Cell]) -> Void:
    '''Place a cell on the cell map'''
    if not (x >= 0 and x < GRID_WIDTH and y >= 0 and y < GRID_HEIGHT):
        return void
    if (x, y) in layer.keys():
        # Target cell is not empty
        if id == 0:
            # New cell type is empty, erase cell
            del layer[(x, y)]
        else:
            # New cell type is not empty, replace cell
            layer[(x, y)] = Cell(x, y, id, dir)
    else:
        # Target cell is empty, add cell
        if id != 0:
            layer[(x, y)] = Cell(x, y, id, dir)

    if tick_number == 0:
        # Reset the initial state only if the current state is initial
        set_initial()

    return void

def get_cell(x: int, y: int) -> Cell:
    '''Get a cell from the map given the position'''
    if (x, y) in cell_map.keys():
        return cell_map[(x, y)]
    else:
        return Cell(x, y, 0, 0)

def get_all_cells() -> list[Cell]:
    '''Gets all the cells with a given ID and a direction, and orders them for sub-sub-ticking.'''
            
    result: list[Cell] = []
    cell: Cell
    for cell in cell_map.values():
        if cell.tile_x < 0 or cell.tile_y < 0 or cell.tile_x >= GRID_WIDTH or cell.tile_y >= GRID_HEIGHT:
            continue
        result.append(cell)

    return result

def reverse(cell: Cell) -> int | float:
    if cell.tile_x < 0 or cell.tile_y < 0 or cell.tile_x >= GRID_WIDTH or cell.tile_y >= GRID_HEIGHT:
        return float("-infinity")
    match cell.dir:
        case 0:
            return +cell.tile_x*GRID_HEIGHT - cell.tile_y
        case 1:
            return +cell.tile_y*GRID_WIDTH + cell.tile_x
        case 2: 
            return -cell.tile_x*GRID_HEIGHT - cell.tile_y
        case 3:
            return -cell.tile_y*GRID_WIDTH + cell.tile_x
    return float("-infinity")

def forward(cell: Cell) -> int:
    if cell.tile_x < 0 or cell.tile_y < 0 or cell.tile_x >= GRID_WIDTH or cell.tile_y >= GRID_HEIGHT:
        return float("-infinity")
    match cell.dir:
        case 0:
            return -cell.tile_x*GRID_HEIGHT + cell.tile_y
        case 1:
            return -cell.tile_y*GRID_WIDTH - cell.tile_x
        case 2: 
            return +cell.tile_x*GRID_HEIGHT + cell.tile_y
        case 3:
            return +cell.tile_y*GRID_WIDTH - cell.tile_x
    return float("-infinity")



def tick():
    '''Ticks the entire map.'''
    # Reset the suppression values
    global tick_number, delete_map
    cell: Cell
    for cell in cell_map.values():
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


    delete_map = []

    # Do freezers (subtick 9)
    for i in range(4):
        for cell in cell_map.values():
            cell.do_freeze(i)

    # Do shields (subtick 10)
    for cell in cell_map.values():
        cell.do_protect()

    # Do mirrors (subtick 38 & 41)
    for cell in sorted(get_all_cells(), key=forward):
        cell.do_mirror(0, 4)

    for cell in sorted(get_all_cells(), key=forward):
        cell.do_mirror(1, 5)

    for cell in sorted(get_all_cells(), key=forward):
        cell.do_mirror(3, 7)

    for cell in sorted(get_all_cells(), key=forward):
        cell.do_mirror(2, 6)

    # Do intakers subticks 70 to 73
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_intake(i)

    for cell in sorted(get_all_cells(), key=forward):
        cell.do_bob()

    # Do generators subticks 90 to 93
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=reverse):
            cell.do_super_gen(i)

    # Do generators subticks 90 to 93
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=reverse):
            cell.do_gen(i)

    # Do replicators subticks 102 to 105
    for i in range(4):
        for cell in sorted(get_all_cells(), key=reverse):
            cell.do_replicate(i)

    # Do gears
    for cell in sorted(get_all_cells(), key=forward):
        cell.do_gear(1)

    for cell in sorted(get_all_cells(), key=forward):
        cell.do_gear(-1)

    # Do flippers (subtick 115)
    for cell in sorted(get_all_cells(), key=forward):
        cell.do_flip()

    # Do rotators
    for cell in sorted(get_all_cells(), key=forward):
        cell.do_rot()

    # Do redirectors
    for cell in sorted(get_all_cells(), key=forward):
        cell.do_redirect()
    
    # Do impulsors
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_impulse(i)

    # Do super repulsors
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_super_repulse(i)

    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_grapulse(i)

    # Do repulsors
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_repulse(i)

    # Do movers
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_drill(i)
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_pull(i)
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=reverse):
            cell.do_grab(i)
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=reverse):
            cell.do_push(i)
    for i in [0, 2, 3, 1]:
        for cell in sorted(get_all_cells(), key=forward):
            cell.do_nudge(i)


    # Gates
    for cell in sorted(get_all_cells(), key=forward):
        for i in range(4):
            cell.do_gate(i)

    tick_number += 1

def draw():
    # divergers
    cell: Cell
    if update_timer != 0:
        for cell in delete_map:
            cell.update()
            cell.draw()
    for cell in below.values(): 
        cell.update()
        cell.draw()
    for cell in cell_map.values(): 
        cell.update()
        cell.draw()
    
    

def copy_map(cm: dict[tuple[int, int], Cell]) -> dict[tuple[int, int], Cell]:
    '''Deep-copies an entire cell map.'''
    result: dict[tuple[int, int], Cell] = {}
    key: tuple[int, int]
    value: Cell
    for key, value in zip(cm.keys(), cm.values()):
        result[key] = value.copy() # type: ignore
        value.tile_x = key[0]
        value.tile_y = key[1]

    return result

def set_initial():
    '''Sets the initial map to the current cell map.'''
    global initial_cell_map, initial_above, initial_below, tick_number
    initial_cell_map = copy_map(cell_map)
    initial_above = copy_map(above)
    initial_below = copy_map(below)
    tick_number = 0

def reset():
    '''Resets the cell map to the initial cell map.'''
    global cell_map, above, below, tick_number, paused
    cell_map = copy_map(initial_cell_map)
    tick_number = 0
    paused = True

def trash():
    global cell_map, tick_number, paused
    cell_map = {}
    i: int
    for i in range(GRID_WIDTH):
        cell_map[(i, -1)] = Cell(i, -1, border_tile, 0)
        cell_map[(i, GRID_HEIGHT)] = Cell(i, GRID_HEIGHT, border_tile, 0)

    # Create left and right border tiles
    for i in range(GRID_HEIGHT):
        cell_map[(-1, i)] = Cell(-1, i, border_tile, 0)
        cell_map[(GRID_WIDTH, i)] = Cell(GRID_WIDTH, i, border_tile, 0)

    # Create corner border tiles
        cell_map[(-1, -1)] = Cell(-1, -1, border_tile, 0)
        cell_map[(-1, GRID_HEIGHT)] = Cell(-1, GRID_HEIGHT, border_tile, 0)
        cell_map[(GRID_WIDTH, -1)] = Cell(GRID_WIDTH, -1, border_tile, 0)
        cell_map[(GRID_WIDTH, GRID_HEIGHT)] = Cell(GRID_WIDTH, GRID_HEIGHT, border_tile, 0)

    tick_number = 0
    paused = True

    set_initial()
    reset()

def delete_selected():
    global select_start, select_end, selecting
    for i in range(max(min(select_start[0], select_end[0]), 0), min(max(select_start[0]+1, select_end[0]+1), GRID_WIDTH)):
        for j in range(max(min(select_start[1], select_end[1]), 0), min(max(select_start[1]+1, select_end[1]+1), GRID_HEIGHT)):
            if (i, j) in cell_map.keys():
                del cell_map[(i, j)]
    select_start = None
    select_end = None
    selecting = False





def nokia(size):
    return pygame.font.Font(resource_path("nokiafc22.ttf"), size)

def resource_path(relative_path):
    import os, sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def scroll_up(x, y):
    global cam_x, cam_y, TILE_SIZE
    TILE_SIZE *= 2
    if TILE_SIZE > 160:
        TILE_SIZE = 160
    else:
        cam_x = (cam_x + x/2)*2
        cam_y = (cam_y + y/2)*2
def scroll_down(x, y):
    global cam_x, cam_y, TILE_SIZE
    TILE_SIZE /= 2
    if TILE_SIZE < 1.25:
        TILE_SIZE = 1.25
    else:
        cam_x = cam_x/2 - x/2
        cam_y = cam_y/2 - y/2
    




# Initialize the game window
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("CelPython Machine")
icon: pygame.Surface = pygame.image.load(resource_path("textures/icon.png"))
pygame.display.set_icon(icon)

# Constants
BACKGROUND: tuple[int, int, int] = (31, 31, 31)
TILE_SIZE: float = 20.0
GRID_WIDTH: int = 100
GRID_HEIGHT: int = 100
TOOLBAR_HEIGHT: int = 54

FPS: int = 180
clock: pygame.time.Clock = pygame.time.Clock()

fps_font = nokia(6)

menu_on = False

# Dynamic settings
scroll_speed: int = 250
border_tile: int = 41
current_menu: int = 0
suppress_place: bool = False
step_speed: float = 0.2

# Brush settings
brush: int | str = 4
brush_dir: int = 0 # 0 = right, 1 = down, 2 = left, 3 = up
selecting = False
select_start = None
select_end = None

# Camera coords
cam_x: float = float(0)
cam_y: float = float(0)

# Mouse coords
mouse_x: int = 0
mouse_y: int = 0
world_mouse_x: float = 0
world_mouse_y: float = 0
world_mouse_tile_x: int = 0
world_mouse_tile_y: int = 0

paused: bool = True
tick_number: int = 0

# Images 
bg_image: pygame.Surface = pygame.image.load(resource_path("textures/bg.png"))
bg_cache = {}
def get_bg(size):
    if size in bg_cache.keys():
        return bg_cache[size]
    img = pygame.transform.scale(bg_image, (size, size))
    bg_cache[size] = img
    return img

tools_icon_image: ToolbarButton = pygame.transform.scale(pygame.image.load(resource_path("textures/eraser.png")), (40, 40))
basic_icon_image: pygame.Surface = pygame.transform.scale(cell_images[4], (40, 40))
movers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[2], (40, 40))
generators_icon_image: pygame.Surface = pygame.transform.scale(cell_images[3], (40, 40))
rotators_icon_image: pygame.Surface = pygame.transform.scale(cell_images[9], (40, 40))
forcers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[21], (40, 40))
divergers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[16], (40, 40))
destroyers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[12], (40, 40))
misc_icon_image: pygame.Surface = pygame.transform.scale(cell_images[20], (40, 40))

#play_image: pygame.Surface = pygame.transform.scale(cell_images[2], (40, 40))
#pause_image: pygame.Surface = pygame.transform.rotate(pygame.transform.scale(cell_images[5], (40, 40)), -90)
#step_image: pygame.Surface = pygame.transform.scale(pygame.image.load(resource_path("textures/nudger.png")), (40, 40))
#reset_image: pygame.Surface = pygame.transform.scale(pygame.image.load(resource_path("textures/rotator_180.png")), (40, 40))
#initial_image: pygame.Surface = pygame.transform.scale(pygame.image.load(resource_path("textures/timewarper.png")), (40, 40))

#exit_image: pygame.Surface = pygame.transform.scale(pygame.image.load(resource_path("textures/delete.png")), (40, 40))
#clear_image: pygame.Surface = pygame.transform.scale(pygame.image.load(resource_path("textures/trash.png")), (40, 40))

#menu_image: pygame.Surface = pygame.transform.scale(pygame.image.load(resource_path("textures/menu.png")), (40, 40))

menu_bg: pygame.Surface = pygame.image.load(resource_path("textures/menubg.png"))

freeze_image: pygame.Surface = pygame.image.load(resource_path("textures/effects/frozen.png"))
protect_image: pygame.Surface = pygame.image.load(resource_path("textures/effects/protected.png"))

buttonz = pygame.sprite.Group()

play_button: Button = Button("mover.png", 40)
play_button.rect.topright = (WINDOW_WIDTH-20, 20)
pause_button: Button = Button("slide.png", 40, -90)
pause_button.rect.topright = (WINDOW_WIDTH-20, 20)
step_button: Button = Button("nudger.png", 40)
step_button.rect.topright = (WINDOW_WIDTH-70, 20)
initial_button: Button = Button("timewarper.png", 40)
initial_button.rect.topright = (WINDOW_WIDTH-70, 70)
reset_button: Button = Button("rotator_180.png", 40)
reset_button.rect.topright = (WINDOW_WIDTH-20, 70)

# Sounds
beep: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/beep.wav"))

brush_image: pygame.Surface
alpha_img: pygame.Surface

#play_rect: pygame.Rect = play_image.get_rect()
#play_rect.topright = (WINDOW_WIDTH - 20, 20)
'''pause_rect: pygame.Rect = pause_image.get_rect()
pause_rect.topright = (WINDOW_WIDTH - 20, 20)
step_rect: pygame.Rect = step_image.get_rect()
step_rect.topright = (WINDOW_WIDTH - 70, 20)
reset_rect: pygame.Rect = reset_image.get_rect()
reset_rect.topright = (WINDOW_WIDTH - 20, 70)
initial_rect: pygame.Rect = initial_image.get_rect()
initial_rect.topright = (WINDOW_WIDTH - 70, 70)

menu_rect: pygame.Rect = menu_image.get_rect()
menu_rect.topleft = (20, 20)'''

menu_button = Button("menu.png", 40)
menu_button.rect.topleft = (20, 20)

menu_bg_rect: pygame.Rect = menu_bg.get_rect()
menu_bg_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2) 

update_timer: float = step_speed



# Rects
tools_icon_rect: pygame.Rect = tools_icon_image.get_rect()
tools_icon_rect.midleft = (7, WINDOW_HEIGHT - 27)

basic_icon_rect: pygame.Rect = movers_icon_image.get_rect()
basic_icon_rect.midleft = (7+1*54, WINDOW_HEIGHT - 27)

movers_icon_rect: pygame.Rect = movers_icon_image.get_rect()
movers_icon_rect.midleft = (7+2*54, WINDOW_HEIGHT - 27)

generators_icon_rect: pygame.Rect = movers_icon_image.get_rect()
generators_icon_rect.midleft = (7+3*54, WINDOW_HEIGHT - 27)

rotators_icon_rect: pygame.Rect = rotators_icon_image.get_rect()
rotators_icon_rect.midleft = (7+4*54, WINDOW_HEIGHT - 27)

forcers_icon_rect: pygame.Rect = rotators_icon_image.get_rect()
forcers_icon_rect.midleft = (7+5*54, WINDOW_HEIGHT - 27)

divergers_icon_rect: pygame.Rect = divergers_icon_image.get_rect()
divergers_icon_rect.midleft = (7+6*54, WINDOW_HEIGHT - 27)

destroyers_icon_rect: pygame.Rect = destroyers_icon_image.get_rect()
destroyers_icon_rect.midleft = (7+7*54, WINDOW_HEIGHT - 27)

misc_icon_rect: pygame.Rect = misc_icon_image.get_rect()
misc_icon_rect.midleft = (7+9*54, WINDOW_HEIGHT - 27)

toolbar_icon_rects: list[pygame.Rect] = [tools_icon_rect, basic_icon_rect, movers_icon_rect, generators_icon_rect, rotators_icon_rect, forcers_icon_rect, divergers_icon_rect, destroyers_icon_rect, None, misc_icon_rect]
toolbar_subicons: list[MenuSubItem] = []

continue_button = MenuButton("mover.png", 40)
continue_button.rect.bottomleft = (WINDOW_WIDTH//2 - menu_bg_rect.width//2 + 32, WINDOW_HEIGHT//2 + menu_bg_rect.height//2 - 32)

menu_reset_button = MenuButton("rotator_180.png", 40)
menu_reset_button.rect.bottomleft = (WINDOW_WIDTH//2 - menu_bg_rect.width//2 + 32 + 50*1, WINDOW_HEIGHT//2 + menu_bg_rect.height//2 - 32)

clear_button = MenuButton("trash.png", 40)
clear_button.rect.bottomleft = (WINDOW_WIDTH//2 - menu_bg_rect.width//2 + 32 + 50*2, WINDOW_HEIGHT//2 + menu_bg_rect.height//2 - 32)

exit_button = MenuButton("delete.png", 40, tint=(255, 128, 128))
exit_button.rect.bottomright = (WINDOW_WIDTH//2 - menu_bg_rect.width//2 + 32 + 50*6, WINDOW_HEIGHT//2 + menu_bg_rect.height//2 - 32)

logo_image = pygame.image.load("textures/logo.png")
logo_rect = logo_image.get_rect()
logo_rect.midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

start_play_button: Button = Button("mover.png", 60)
start_play_button.rect.midtop = (WINDOW_WIDTH//2, logo_rect.bottom + 20)

quit_button: Button = Button("delete.png", 40, tint=(255, 128, 128))
quit_button.rect.topright = (WINDOW_WIDTH - 20, 20)

zoomin_button: Button = Button("zoomin.png", 40)
zoomin_button.rect.topleft = (70, 20)
zoomout_button: Button = Button("zoomout.png", 40)
zoomout_button.rect.topleft = (120, 20)
eraser_button: Button = Button("eraser.png", 40)
eraser_button.rect.topleft = (170, 20)
select_button: Button = Button("select.png", 40)
select_button.rect.topleft = (20, 70)
delete_button: Button = Button("delete.png", 40)
delete_button.rect.topleft = (170, 70)

topleft_button_group = pygame.sprite.Group()
topleft_button_group.add(menu_button, zoomin_button, zoomout_button, eraser_button, select_button, delete_button)

# Create submenu icons
cell_id: int | str
for cell_id in cell_images.keys():
    toolbar_subicons.append(MenuSubItem(cell_id))

toolbar_subcategories = {}
for cell_id in cell_images.keys():
    toolbar_subcategories[cell_id] = (MenuSubCategory(cell_id))



    

# Initialize cell maps
cell_map: dict[tuple[int, int], Cell] = {}
delete_map = []
above: dict[tuple[int, int], Cell] = {}
below: dict[tuple[int, int], Cell] = {}

# Initial maps
initial_cell_map: dict[tuple[int, int], Cell] = {}
initial_above: dict[tuple[int, int], Cell] = {}
initial_below: dict[tuple[int, int], Cell] = {}


# Play music
#pygame.mixer.music.load(resource_path("audio/scattered cells.ogg"))
#pygame.mixer.music.play(-1)

keys: list[bool]
mouse_buttons: tuple[bool, bool, bool] = (False, False, False)
current_submenu = -1

# Create border tiles

# Create top and bottom border tiles
i: int
for i in range(GRID_WIDTH):
    cell_map[(i, -1)] = Cell(i, -1, border_tile, 0)
    cell_map[(i, GRID_HEIGHT)] = Cell(i, GRID_HEIGHT, border_tile, 0)

# Create left and right border tiles
for i in range(GRID_HEIGHT):
    cell_map[(-1, i)] = Cell(-1, i, border_tile, 0)
    cell_map[(GRID_WIDTH, i)] = Cell(GRID_WIDTH, i, border_tile, 0)

# Create corner border tiles
    cell_map[(-1, -1)] = Cell(-1, -1, border_tile, 0)
    cell_map[(-1, GRID_HEIGHT)] = Cell(-1, GRID_HEIGHT, border_tile, 0)
    cell_map[(GRID_WIDTH, -1)] = Cell(GRID_WIDTH, -1, border_tile, 0)
    cell_map[(GRID_WIDTH, GRID_HEIGHT)] = Cell(GRID_WIDTH, GRID_HEIGHT, border_tile, 0)

set_initial()

# Text
title_text: pygame.Surface = nokia(15).render("CelPython Machine", True, (255, 255, 255))
title_rect = title_text.get_rect()
title_rect.midbottom = (WINDOW_WIDTH//2, WINDOW_WIDTH//2)

stepping = False

t = 0

# Loop-only variables
all_buttons: list[bool]
keys: list[bool]
events: list[pygame.event.Event]
event: pygame.event.Event

# Main game loop
running: bool = True
screen = "title"

if __name__ != "__main__":
    pass

while running:
    WINDOW_HEIGHT = window.get_height()
    WINDOW_WIDTH = window.get_width()
    all_buttons = []
            
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
            running = False

    if screen == "game":
        step_button.rect.topright =(WINDOW_WIDTH - 70, 20)
        play_button.rect.topright = (WINDOW_WIDTH - 20, 20)
        pause_button.rect.topright = (WINDOW_WIDTH - 20, 20)
        reset_button.rect.topright = (WINDOW_WIDTH - 20, 70)
        initial_button.rect.topright = (WINDOW_WIDTH - 70, 70)
        step_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        reset_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        initial_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        for i in topleft_button_group:
            i.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        if selecting:
            select_button.tint = (128, 255, 128)
        else:
            select_button.tint = (255, 255, 255)
        continue_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        exit_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        menu_reset_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        clear_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                # Player is scrolling
                if event.dict["y"] == -1:
                    # Scrolling down
                    scroll_down(mouse_x, mouse_y)
                if event.dict["y"] == 1:
                    # Scrolling up
                    scroll_up(mouse_x, mouse_y)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selecting and event.dict["button"] == 1 and True not in all_buttons:
                    select_start = (world_mouse_tile_x, world_mouse_tile_y)
                    select_end = (world_mouse_tile_x, world_mouse_tile_y)

            if event.type == pygame.MOUSEBUTTONUP:
                if selecting and event.dict["button"] == 1 and True not in all_buttons:
                    select_end = (world_mouse_tile_x, world_mouse_tile_y)
                else:
                    if tools_icon_rect.collidepoint(mouse_x, mouse_y):
                        brush = 0
                    elif basic_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 1:
                            current_menu = -1
                        else:
                            current_menu = 1
                        current_submenu = -1
                    elif movers_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 2:
                            current_menu = -1
                        else:
                            current_menu = 2
                        current_submenu = -1
                    elif generators_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 3:
                            current_menu = -1
                        else:
                            current_menu = 3
                        current_submenu = -1
                    elif rotators_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 4:
                            current_menu = -1
                        else:
                            current_menu = 4
                        current_submenu = -1
                    elif forcers_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 5:
                            current_menu = -1
                        else:
                            current_menu = 5
                        current_submenu = -1
                    elif divergers_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 6:
                            current_menu = -1
                        else:
                            current_menu = 6
                        current_submenu = -1
                    elif destroyers_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 7:
                            current_menu = -1
                        else:
                            current_menu = 7
                        current_submenu = -1
                    elif misc_icon_rect.collidepoint(mouse_x, mouse_y):
                        if current_menu == 9:
                            current_menu = -1
                        else:
                            current_menu = 9
                        current_submenu = -1
                    
                    elif play_button.rect.collidepoint(mouse_x, mouse_y):
                        paused = not paused
                    elif step_button.rect.collidepoint(mouse_x, mouse_y):
                        tick()
                    elif reset_button.rect.collidepoint(mouse_x, mouse_y):
                        beep.play()
                        reset()
                    elif initial_button.rect.collidepoint(mouse_x, mouse_y):
                        beep.play()
                        set_initial()
                    elif zoomin_button.rect.collidepoint(mouse_x, mouse_y):
                        scroll_up(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    elif zoomout_button.rect.collidepoint(mouse_x, mouse_y):
                        scroll_down(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    elif eraser_button.rect.collidepoint(mouse_x, mouse_y):
                        brush = 0
                    elif select_button.rect.collidepoint(mouse_x, mouse_y):
                        selecting = not selecting
                        if not selecting:
                            select_start = None
                            select_end = None
                    elif delete_button.rect.collidepoint(mouse_x, mouse_y):
                        if selecting and select_start != None and select_end != None:
                            delete_selected()

                    elif menu_button.rect.collidepoint(mouse_x, mouse_y):
                        menu_on = not menu_on
                    elif continue_button.rect.collidepoint(mouse_x, mouse_y) and menu_on:
                        menu_on = False
                        beep.play()
                    elif exit_button.rect.collidepoint(mouse_x, mouse_y) and menu_on:
                        beep.play()
                        screen = "title"

                    elif menu_reset_button.rect.collidepoint(mouse_x, mouse_y) and menu_on:
                        beep.play()
                        reset()

                    elif clear_button.rect.collidepoint(mouse_x, mouse_y) and menu_on:
                        beep.play()
                        trash()

                    if event.dict["button"] == 2:
                        picked_cell = get_cell(world_mouse_tile_x, world_mouse_tile_y)
                        brush = picked_cell.id
                        brush_dir = picked_cell.dir

                    for button in toolbar_subicons:
                        button.update(mouse_buttons, mouse_x, mouse_y, brush, current_menu, current_submenu)
                    for button in toolbar_subcategories.values():
                        button.handle_click(mouse_buttons, mouse_x, mouse_y, brush, current_menu)
            else:
                if mouse_buttons[0]:
                    select_end = (world_mouse_tile_x, world_mouse_tile_y)



                    
            
            if event.type == pygame.KEYDOWN:
                if event.dict["key"] == pygame.K_q:
                    brush_dir -= 1
                    brush_dir = brush_dir % 4
                if event.dict["key"] == pygame.K_e:
                    brush_dir += 1
                    brush_dir = brush_dir % 4

                if event.dict["key"] == pygame.K_f:
                    tick()
                    stepping = True
                    update_timer = step_speed

                if event.dict["key"] == pygame.K_t:
                    i = 0
                    for tile in list(cell_map.values()):
                        if (tile.tile_x, tile.tile_y) == (world_mouse_tile_x, world_mouse_tile_y):
                            print(tile.suppressed)
                
                if event.dict["key"] == pygame.K_r:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_LMETA]:
                        beep.play()
                        reset()

                if event.dict["key"] == pygame.K_ESCAPE:
                    menu_on = not menu_on

                if event.dict["key"] == pygame.K_SPACE:
                    if paused:
                        tick()
                        update_timer = step_speed
                    paused = not paused
                if event.dict["key"] == pygame.K_TAB:
                    selecting = not selecting
                    if not selecting:
                        select_start = None
                        select_end = None
                if event.dict["key"] == pygame.K_BACKSPACE:
                    if selecting:
                        delete_selected()



        # Press CTRL to speed up scrolling
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            scroll_speed = 500
        else:
            scroll_speed = 250
        
        # WASD to move the camera
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            cam_y -= scroll_speed*dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            cam_x -= scroll_speed*dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            cam_y += scroll_speed*dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            cam_x += scroll_speed*dt



        world_mouse_x = mouse_x + cam_x
        world_mouse_y = mouse_y + cam_y
        world_mouse_tile_x = int(world_mouse_x//TILE_SIZE)
        world_mouse_tile_y = int(world_mouse_y//TILE_SIZE)

        




        # Check for a press suppression
        button: MenuSubItem
        for button in toolbar_subicons:
            all_buttons.append(button.update(mouse_buttons, mouse_x, mouse_y, brush, current_menu, current_submenu))
        for button in toolbar_subcategories.values():
            all_buttons.append(button.update(mouse_buttons, mouse_x, mouse_y, brush, current_menu))

        if True in all_buttons:
            suppress_place = True
        else:
            suppress_place = False

        # Place tiles if possible
        if not selecting:
            if mouse_y < WINDOW_HEIGHT - 54 and not suppress_place:       
                if mouse_buttons[0]:
                    if "placeable" in str(brush):
                        place_cell(world_mouse_tile_x, world_mouse_tile_y, brush, brush_dir, below)
                    else:
                        place_cell(world_mouse_tile_x, world_mouse_tile_y, brush, brush_dir, cell_map)
                if mouse_buttons[2]:
                    place_cell(world_mouse_tile_x, world_mouse_tile_y, 0, 0, cell_map)
        
        # Reset background
        window.fill(BACKGROUND, window.get_rect())

        # Get border tile image
        border_image = cell_images[border_tile]

        i: int
        j: int
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if not (TILE_SIZE*i-cam_x+TILE_SIZE < 0 or TILE_SIZE*i-cam_x > WINDOW_WIDTH or TILE_SIZE*j-cam_y+TILE_SIZE < 0 or TILE_SIZE*j-cam_y > WINDOW_HEIGHT):
                    #if (i, j) not in cell_map.keys():
                        window.blit(get_bg(TILE_SIZE), (TILE_SIZE*i-cam_x, TILE_SIZE*j-cam_y))


        draw()
        
        if selecting and select_start != None and select_end != None:
            s = pygame.Surface((abs(select_end[0]-select_start[0])*TILE_SIZE+TILE_SIZE, abs(select_end[1]-select_start[1])*TILE_SIZE+TILE_SIZE), pygame.SRCALPHA)
            s.set_alpha(64)
            s.fill((255, 255, 255))
            window.blit(s, (min(select_start[0]*TILE_SIZE-cam_x, select_end[0]*TILE_SIZE-cam_x), min(select_start[1]*TILE_SIZE-cam_y, select_end[1]*TILE_SIZE-cam_y)))
            #pygame.draw.rect(window, (255, 255, 255, 128), pygame.rect.Rect(min(select_start[0]*TILE_SIZE-cam_x, select_end[0]*TILE_SIZE-cam_x), min(select_start[1]*TILE_SIZE-cam_y, select_end[1]*TILE_SIZE-cam_y), abs(select_end[0]-select_start[0])*TILE_SIZE+TILE_SIZE, abs(select_end[1]-select_start[1])*TILE_SIZE+TILE_SIZE))

        if not selecting:
            # Draw brush image
            brush_image = cell_images[brush].convert_alpha()
            alpha_img = pygame.Surface(brush_image.get_rect().size, pygame.SRCALPHA)
            alpha_img.fill((255, 255, 255, 255*0.25)) # type: ignore
            brush_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            if True not in all_buttons:
                window.blit(pygame.transform.rotate(pygame.transform.scale(brush_image, (TILE_SIZE, TILE_SIZE)), -90*brush_dir), (world_mouse_tile_x*TILE_SIZE-cam_x, world_mouse_tile_y*TILE_SIZE-cam_y))

        # Draw bottom toolbar
        pygame.draw.rect(window, (60, 60, 60), pygame.Rect(-10, WINDOW_HEIGHT-TOOLBAR_HEIGHT, WINDOW_WIDTH+20, TOOLBAR_HEIGHT+10))
        pygame.draw.rect(window, (127, 127, 127), pygame.Rect(-10, WINDOW_HEIGHT-TOOLBAR_HEIGHT, WINDOW_WIDTH+20, TOOLBAR_HEIGHT+10), 1)

        # Update toolbar positions\
        tools_icon_rect.midleft = (7, WINDOW_HEIGHT - 27)
        basic_icon_rect.midleft = (7+1*54, WINDOW_HEIGHT - 27)
        movers_icon_rect.midleft = (7+2*54, WINDOW_HEIGHT - 27)
        generators_icon_rect.midleft = (7+3*54, WINDOW_HEIGHT - 27)
        rotators_icon_rect.midleft = (7+4*54, WINDOW_HEIGHT - 27)
        forcers_icon_rect.midleft = (7+5*54, WINDOW_HEIGHT - 27)
        divergers_icon_rect.midleft = (7+6*54, WINDOW_HEIGHT - 27)
        destroyers_icon_rect.midleft = (7+7*54, WINDOW_HEIGHT - 27)
        misc_icon_rect.midleft = (7+9*54, WINDOW_HEIGHT - 27)
        # Blit toolbar icons
        window.blit(pygame.transform.rotate(tools_icon_image, 0), tools_icon_rect)
        window.blit(pygame.transform.rotate(basic_icon_image, -90*brush_dir), basic_icon_rect)
        window.blit(pygame.transform.rotate(movers_icon_image, -90*brush_dir), movers_icon_rect)
        window.blit(pygame.transform.rotate(generators_icon_image, -90*brush_dir), generators_icon_rect)
        window.blit(pygame.transform.rotate(rotators_icon_image, -90*brush_dir), rotators_icon_rect)
        window.blit(pygame.transform.rotate(forcers_icon_image, -90*brush_dir), forcers_icon_rect)
        window.blit(pygame.transform.rotate(divergers_icon_image, -90*brush_dir), divergers_icon_rect)
        window.blit(pygame.transform.rotate(destroyers_icon_image, -90*brush_dir), destroyers_icon_rect)
        window.blit(pygame.transform.rotate(misc_icon_image, -90*brush_dir), misc_icon_rect)

        for button in toolbar_subicons:
            button.draw(window)
        for button in toolbar_subcategories.values():
            button.update(mouse_buttons, mouse_x, mouse_y, brush, current_menu)
            button.draw(window)
        if paused:
            play_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            play_button.draw(window)
        else:
            pause_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
            pause_button.draw(window)

        
        step_button.draw(window)       
        reset_button.draw(window)       
        initial_button.draw(window)       
        for i in topleft_button_group:
            i.draw(window)

        title_rect.midtop = (WINDOW_WIDTH//2, menu_bg_rect.top + 10)
        menu_bg_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        

        if menu_on:
            window.blit(menu_bg, menu_bg_rect)
            continue_button.draw(window)

            exit_button.draw(window)

            menu_reset_button.draw(window)

            clear_button.draw(window)



            update_delay_text = nokia(10).render(f"Update delay: {step_speed}", True, (255, 255, 255))
            update_delay_rect = update_delay_text.get_rect()
            update_delay_rect.topleft = (menu_bg_rect.x + 20, menu_bg_rect.y + 40)
            window.blit(update_delay_text, update_delay_rect)





        


    elif screen == "title":
        # Event loop
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse_buttons[0] and start_play_button.rect.collidepoint(mouse_x, mouse_y):
                    screen = "game"
                    trash()
                    menu_on = False
                    TILE_SIZE = 20.0
                    cam_x = 0
                    cam_y = 0
                if mouse_buttons[0] and quit_button.rect.collidepoint(mouse_x, mouse_y):
                    running = False
        window.fill(BACKGROUND, window.get_rect())
        #logo_image, _ = rot_center(logo_image, logo_rect, math.sin(t))
        logo_rect.midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        window.blit(cell.rot_center(logo_image, logo_rect, math.sin(t)*5)[0], cell.rot_center(logo_image, logo_rect, math.sin(t)*5)[1])       

        start_play_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        start_play_button.draw(window)

        quit_button.update(mouse_buttons, mouse_x, mouse_y, 0, 0)
        quit_button.draw(window)

    clock.tick()
    dt = clock.get_time() / 1000
    t+=dt
    if not paused:
        if dt > step_speed:
            update_timer = 0
        else:
            update_timer -= dt
        if update_timer <= 0:
            update_timer += step_speed
            if update_timer < 0:
                update_timer = 0
                
            tick()
    else:
        if update_timer > 0:
            update_timer -= dt
        else:
            update_timer = 0

    if screen == "game":
        if (world_mouse_tile_x, world_mouse_tile_y) in cell_map.keys():
            disp = cell_map[world_mouse_tile_x, world_mouse_tile_y].__repr__()
        else:
            disp = str((world_mouse_tile_x, world_mouse_tile_y))
        coord_text = fps_font.render(f"{disp}", True, (255, 255, 255))
        coord_rect = coord_text.get_rect()
        coord_rect.topright = (WINDOW_WIDTH, 4)
        window.blit(fps_font.render(f"FPS: {str(clock.get_fps())}", True, (255, 255, 255)), (0, 4))
        window.blit(fps_font.render(f"Tick: {str(tick_number)}", True, (255, 255, 255)), (0, 13))
        window.blit(coord_text, coord_rect)
    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
