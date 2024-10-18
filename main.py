import pygame, sys
from cell import Cell, cell_images
import cell

from button import MenuSubItem

# Initialize pygame
pygame.init()

def place_cell(x: int, y: int, id: int, dir: int):
    '''Place a cell on the cell map'''
    if not (x >= 0 and x < GRID_WIDTH and y >= 0 and y < GRID_HEIGHT):
        return
    if (x, y) in cell_map.keys():
        # Target cell is not empty
        if id == 0:
            # New cell type is empty, erase cell
            del cell_map[(x, y)]
        else:
            # New cell type is not empty, replace cell
            cell_map[(x, y)] = Cell(x, y, id, dir)
    else:
        # Target cell is empty, add cell
        if id != 0:
            cell_map[(x, y)] = Cell(x, y, id, dir)

    if tick_number == 0:
        # Reset the initial state only if the current state is initial
        set_initial()

def get_cell(x: int, y: int) -> Cell:
    '''Get a cell from the map given the position'''
    if (x, y) in cell_map.keys():
        return cell_map[(x, y)]
    else:
        return Cell(x, y, 0, 0)

def get_all_cells(ids: list[int], dir: int) -> list[Cell]:
    '''Gets all the cells with a given ID and a direction, and orders them for sub-sub-ticking.'''
    def key_func(cell: Cell) -> int:
        match cell.dir:
            case 0:
                return -cell.tile_x*GRID_HEIGHT - cell.tile_y
            case 1:
                return -cell.tile_y*GRID_WIDTH + cell.tile_x
            case 2: 
                return cell.tile_x*GRID_HEIGHT -cell.tile_y
            case 3:
                return cell.tile_y*GRID_WIDTH + cell.tile_x
            
    result: list[Cell] = []
    cell: Cell
    for cell in cell_map.values():
        if cell.id in ids and cell.dir in dir:
            result.append(cell)

    result.sort(key=key_func)

    return result

def tick():
    '''Ticks the entire map.'''
    # Reset the suppression values
    cell: Cell
    for cell in cell_map.values():
        cell.suppressed = False
        cell.frozen = False

    i: int

    # Do freezers
    for cell in get_all_cells([25], [0, 1, 2, 3]):
        for i in range(4):
            cell.tick(i)

    # Do mirrors
    for cell in get_all_cells([15], [0, 1, 2, 3]):
        cell.tick(0)

    # Do generators
    for cell in get_all_cells([3, 23, 26, 27], [0, 1, 2, 3]):
        for i in range(4):
            cell.tick(i)

    # Do gearssd
    for cell in get_all_cells([18, 19], [0, 1, 2, 3]):
        cell.tick(0)

    # Do flippers
    for cell in get_all_cells([30], [0, 1, 2, 3]):
        cell.tick(0)

    # Do rotators
    for cell in get_all_cells([9, 10, 11], [0, 1, 2, 3]):
        cell.tick(0)

    # Do redirectors
    for cell in get_all_cells([17], [0, 1, 2, 3]):
        cell.tick(0)
    
    # Do impulsors
    for i in [0, 2, 3, 1]:
        for cell in get_all_cells([29], [0, 1, 2, 3]):
            cell.tick(i)
    
    # Do repulsors
    for i in [0, 2, 3, 1]:
        for cell in get_all_cells([21], [0, 1, 2, 3]):
            cell.tick(i)

    # Do pullers
    for i in range(4):
        for cell in get_all_cells([14, 28], [i]):
            cell.tick(0)

    # Do movers
    for i in range(4):
        for cell in get_all_cells([2], [i]):
            cell.tick(0)

def copy_map(cm: dict[tuple[int, int], Cell]) -> dict[tuple[int, int], Cell]:
    '''Deep-copies an entire cell map.'''
    result: dict[tuple[int, int], Cell] = {}
    key: tuple[int, int]
    value: Cell
    for key, value in zip(cm.keys(), cm.values()):
        result[key] = value.copy()
        value.tile_x = key[0]
        value.tile_y = key[1]

    return result

def set_initial():
    '''Sets the initial map to the current cell map.'''
    global initial_cell_map, initial_above, initial_below
    initial_cell_map = copy_map(cell_map)
    initial_above = copy_map(above)
    initial_below = copy_map(below)
    tick_number = 0

def reset():
    '''Resets the cell map to the initial cell map.'''
    global cell_map, above, below
    cell_map = copy_map(initial_cell_map)


# Initialize the game window
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("CelPython Machine")
icon: pygame.Surface = pygame.image.load("textures/icon.png")
pygame.display.set_icon(icon)

# Constants
BACKGROUND: tuple[int, int, int] = (31, 31, 31)
TILE_SIZE: int = 20
GRID_WIDTH: int = 100
GRID_HEIGHT: int = 100
TOOLBAR_HEIGHT: int = 54

FPS: int = 60
clock: pygame.time.Clock = pygame.time.Clock()

# Dynamic settings
scroll_speed: int = 5
border_tile: int = 1
current_menu: int = 0
suppress_place: bool = False
step_speed: float = 0.2

# Brush settings
brush: int = 4
brush_dir: int = 0 # 0 = right, 1 = down, 2 = left, 3 = up

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
bg_image: pygame.Surface = pygame.image.load("textures/bg.png")
tools_icon_image: pygame.Surface = pygame.transform.scale(pygame.image.load("textures/eraser.png"), (40, 40))
basic_icon_image: pygame.Surface = pygame.transform.scale(cell_images[4], (40, 40))
movers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[2], (40, 40))
generators_icon_image: pygame.Surface = pygame.transform.scale(cell_images[3], (40, 40))
rotators_icon_image: pygame.Surface = pygame.transform.scale(cell_images[9], (40, 40))
forcers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[21], (40, 40))
divergers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[16], (40, 40))
destroyers_icon_image: pygame.Surface = pygame.transform.scale(cell_images[12], (40, 40))
misc_icon_image: pygame.Surface = pygame.transform.scale(cell_images[20], (40, 40))

play_image: pygame.Surface = pygame.transform.scale(cell_images[2], (40, 40))
pause_image: pygame.Surface = pygame.transform.rotate(pygame.transform.scale(cell_images[5], (40, 40)), -90)
step_image: pygame.Surface = pygame.transform.scale(pygame.image.load("textures/nudger.png"), (40, 40))
reset_image: pygame.Surface = pygame.transform.scale(pygame.image.load("textures/rotator_180.png"), (40, 40))
initial_image: pygame.Surface = pygame.transform.scale(pygame.image.load("textures/timewarper.png"), (40, 40))

freeze_image: pygame.Surface = pygame.image.load("textures/effects/frozen.png")

# Sounds
beep: pygame.mixer.Sound = pygame.mixer.Sound("audio/beep.wav")

brush_image: pygame.Surface
alpha_img: pygame.Surface

play_rect: pygame.Rect = play_image.get_rect()
play_rect.topright = (WINDOW_WIDTH - 10, 10)
pause_rect: pygame.Rect = pause_image.get_rect()
pause_rect.topright = (WINDOW_WIDTH - 10, 10)
step_rect: pygame.Rect = step_image.get_rect()
step_rect.topright = (WINDOW_WIDTH - 60, 10)
reset_rect: pygame.Rect = reset_image.get_rect()
reset_rect.topright = (WINDOW_WIDTH - 10, 60)
initial_rect: pygame.Rect = initial_image.get_rect()
initial_rect.topright = (WINDOW_WIDTH - 60, 60)

update_timer: float = 0



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

# Create submenu icons
cell_id: int
for cell_id in cell_images.keys():
    toolbar_subicons.append(MenuSubItem(cell_id))
    

# Initialize cell maps
cell_map: dict[tuple[int, int], Cell] = {}
above: dict[tuple[int, int], Cell] = {}
below: dict[tuple[int, int], Cell] = {}

# Initial maps
initial_cell_map: dict[tuple[int, int], Cell] = {}
initial_above: dict[tuple[int, int], Cell] = {}
initial_below: dict[tuple[int, int], Cell] = {}


# Play music
#pygame.mixer.music.load("audio/scattered cells.ogg")
#pygame.mixer.music.play(-1)

keys: list[bool]
mouse_buttons: tuple[bool, bool, bool] = (False, False, False)

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

# Loop-only variables
all_buttons: list[bool]
keys: list[bool]
events: list[pygame.event.Event]
event: pygame.event.Event

# Main game loop
running: bool = True
while running:
    all_buttons = []
            
    # Get pressed keys
    keys: list[bool] = pygame.key.get_pressed()

    # Event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            # Player wants to quit
            running = False
        if event.type == pygame.MOUSEWHEEL:
            # Player is scrolling
            if event.dict["y"] == -1:
                # Scrolling down
                TILE_SIZE /= 2
                if TILE_SIZE < 1.25:
                    TILE_SIZE = 1.25
                else:
                    cam_x = cam_x/2 - mouse_x/2
                    cam_y = cam_y/2 - mouse_y/2
            if event.dict["y"] == 1:
                # Scrolling up
                TILE_SIZE *= 2
                if TILE_SIZE > 80:
                    TILE_SIZE = 80
                else:
                    cam_x = (cam_x + mouse_x/2)*2
                    cam_y = (cam_y + mouse_y/2)*2

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tools_icon_rect.collidepoint(mouse_x, mouse_y):
                brush = 0
            if basic_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 1:
                    current_menu = -1
                else:
                    current_menu = 1
            if movers_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 2:
                    current_menu = -1
                else:
                    current_menu = 2
            if generators_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 3:
                    current_menu = -1
                else:
                    current_menu = 3
            if rotators_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 4:
                    current_menu = -1
                else:
                    current_menu = 4
            if forcers_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 5:
                    current_menu = -1
                else:
                    current_menu = 5
            if divergers_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 6:
                    current_menu = -1
                else:
                    current_menu = 6
            if destroyers_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 7:
                    current_menu = -1
                else:
                    current_menu = 7

            if misc_icon_rect.collidepoint(mouse_x, mouse_y):
                if current_menu == 9:
                    current_menu = -1
                else:
                    current_menu = 9
            
            if play_rect.collidepoint(mouse_x, mouse_y):
                paused = not paused
            if step_rect.collidepoint(mouse_x, mouse_y):
                tick()
            if reset_rect.collidepoint(mouse_x, mouse_y):
                beep.play()
                reset()
            if initial_rect.collidepoint(mouse_x, mouse_y):
                beep.play()
                set_initial()

            if event.dict["button"] == 2:
                picked_cell = get_cell(world_mouse_tile_x, world_mouse_tile_y)
                brush = picked_cell.id
                brush_dir = picked_cell.dir

                
        
        if event.type == pygame.KEYDOWN:
            if event.dict["key"] == pygame.K_q:
                brush_dir -= 1
                brush_dir = brush_dir % 4
            if event.dict["key"] == pygame.K_e:
                brush_dir += 1
                brush_dir = brush_dir % 4

            if event.dict["key"] == pygame.K_f:
                tick()

            if event.dict["key"] == pygame.K_t:
                i = 0
                for tile in list(cell_map.values()):
                    if (tile.tile_x, tile.tile_y) == (world_mouse_tile_x, world_mouse_tile_y):
                        print(cell.get_row((tile.tile_x, tile.tile_y), (tile.dir+2)%4))#, cell.increment_with_divergers(tile.tile_x, tile.tile_y, tile.dir)
            
            if event.dict["key"] == pygame.K_r:
                if keys[pygame.K_LCTRL] or keys[pygame.KMOD_META]:
                    beep.play()
                    reset()

            if event.dict["key"] == pygame.K_SPACE:
                paused = not paused


    



    # Press CTRL to speed up scrolling
    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        scroll_speed = 10
    else:
        scroll_speed = 5
    
    # WASD to move the camera
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        cam_y -= scroll_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        cam_x -= scroll_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        cam_y += scroll_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        cam_x += scroll_speed


    # Get pressed mouse buttons
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_mouse_x = mouse_x + cam_x
    world_mouse_y = mouse_y + cam_y
    world_mouse_tile_x = world_mouse_x//TILE_SIZE
    world_mouse_tile_y = world_mouse_y//TILE_SIZE

    if play_rect.collidepoint(mouse_x, mouse_y):
        all_buttons.append(True)
    if step_rect.collidepoint(mouse_x, mouse_y):
        all_buttons.append(True)
    if reset_rect.collidepoint(mouse_x, mouse_y):
        all_buttons.append(True)
    if initial_rect.collidepoint(mouse_x, mouse_y):
        all_buttons.append(True)

    # Check for a press suppression
    button: MenuSubItem
    for button in toolbar_subicons:
        all_buttons.append(button.update(mouse_buttons))
    if True in all_buttons:
        suppress_place = True
    else:
        suppress_place = False

    # Place tiles if possible
    if mouse_y < WINDOW_HEIGHT - 54 and not suppress_place:       
        if mouse_buttons[0]:
            place_cell(world_mouse_tile_x, world_mouse_tile_y, brush, brush_dir)
        if mouse_buttons[2]:
            place_cell(world_mouse_tile_x, world_mouse_tile_y, 0, 0)
    
    # Reset background
    window.fill(BACKGROUND, window.get_rect())

    # Get border tile image
    border_image = cell_images[border_tile]

    i: int
    j: int
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            window.blit(pygame.transform.scale(bg_image, (TILE_SIZE, TILE_SIZE)), (TILE_SIZE*i-cam_x, TILE_SIZE*j-cam_y))

    # Draw tiles
    for tile in cell_map.values():
        tile.update()
        tile.draw()


    # Draw brush image
    brush_image = cell_images[brush].convert_alpha()
    alpha_img = pygame.Surface(brush_image.get_rect().size, pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 255*0.25))
    brush_image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    if True not in all_buttons:
        window.blit(pygame.transform.rotate(pygame.transform.scale(brush_image, (TILE_SIZE, TILE_SIZE)), -90*brush_dir), (world_mouse_tile_x*TILE_SIZE-cam_x, world_mouse_tile_y*TILE_SIZE-cam_y))

    # Draw bottom toolbar
    pygame.draw.rect(window, (60, 60, 60), pygame.Rect(-10, WINDOW_HEIGHT-TOOLBAR_HEIGHT, WINDOW_WIDTH+20, TOOLBAR_HEIGHT+10))
    pygame.draw.rect(window, (127, 127, 127), pygame.Rect(-10, WINDOW_HEIGHT-TOOLBAR_HEIGHT, WINDOW_WIDTH+20, TOOLBAR_HEIGHT+10), 1)

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
    if paused:
        image = play_image.convert_alpha()
        alpha_img = pygame.Surface(play_rect.size, pygame.SRCALPHA)
        if play_rect.collidepoint(mouse_x, mouse_y):
            alpha_img.fill((255, 255, 255, 255))
        else:
            alpha_img.fill((255, 255, 255, 255*0.5))
        image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        window.blit(image, play_rect)
    else:
        image = pause_image.convert_alpha()
        alpha_img = pygame.Surface(pause_rect.size, pygame.SRCALPHA)
        if pause_rect.collidepoint(mouse_x, mouse_y):
            alpha_img.fill((255, 255, 255, 255))
        else:
            alpha_img.fill((255, 255, 255, 255*0.5))
        image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        window.blit(image, pause_rect)

    image = step_image.convert_alpha()
    alpha_img = pygame.Surface(step_rect.size, pygame.SRCALPHA)
    if step_rect.collidepoint(mouse_x, mouse_y):
            alpha_img.fill((255, 255, 255, 255))
    else:
        alpha_img.fill((255, 255, 255, 255*0.5))
    image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    window.blit(image, step_rect)

    image = reset_image.convert_alpha()
    alpha_img = pygame.Surface(step_rect.size, pygame.SRCALPHA)
    if reset_rect.collidepoint(mouse_x, mouse_y):
            alpha_img.fill((255, 255, 255, 255))
    else:
        alpha_img.fill((255, 255, 255, 255*0.5))
    image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    window.blit(image, reset_rect)

    image = initial_image.convert_alpha()
    alpha_img = pygame.Surface(step_rect.size, pygame.SRCALPHA)
    if initial_rect.collidepoint(mouse_x, mouse_y):
            alpha_img.fill((255, 255, 255, 255))
    else:
        alpha_img.fill((255, 255, 255, 255*0.5))
    image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    window.blit(image, initial_rect)
    
    clock.tick()
    if not paused:
        update_timer += clock.get_time()/1000
        if update_timer > step_speed:
            update_timer -= step_speed
            tick()
    else:
        update_timer = 0


    # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()