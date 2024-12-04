import pygame
from math import atan2, pi

pygame.init()

# Forward declaration
class Cell: # type: ignore
    pass

cell_names: dict[int|str, str] = {
    # Names of cells based on their id
    "placeable": "placeable",
    0: "eraser", #
    1: "wall", #
    2: "mover", #
    3: "generator", #
    4: "push", #
    5: "slide", #
    6: "onedirectional", #
    7: "twodirectional", #
    8: "threedirectional", #
    9: "rotator_cw", #
    10: "rotator_ccw", #
    11: "rotator_180", #
    12: "trash", #
    13: "enemy", #
    14: "puller", #
    15: "mirror", #
    16: "diverger",
    17: "redirector", #
    18: "gear_cw", #
    19: "gear_ccw", #
    20: "ungeneratable", #
    21: "repulsor", #
    22: "weight", #
    23: "crossgenerator", #
    24: "strongenemy", #
    25: "freezer", #
    26: "cwgenerator", #
    27: "ccwgenerator", #
    28: "advancer", #
    29: "impulsor", #
    30: "flipper", #
    31: "bidiverger", #
    32: "gate_or", #
    33: "gate_and", #
    34: "gate_xor", #
    35: "gate_nor", #
    36: "gate_nand", #
    37: "gate_xnor", #
    38: "straightdiverger", #
    39: "crossdiverger", #
    40: "twistgenerator", #
    41: "ghost", #
    42: "bias", #
    43: "shield", #
    44: "intaker", #
    45: "replicator", #
    46: "crossreplicator", #
    47: "fungal", #
    48: "forker", #
    49: "triforker", #
    50: "superrepulsor", #
    51: "demolisher", #
    52: "opposition", #
    53: "crossopposition", #
    54: "slideopposition", #
    55: "supergenerator",
    56: "crossmirror",
    57: "birotator",
    58: "driller",
    59: "auger",
    60: "corkscrew",
    61: "bringer",
    62: "outdirector",
    63: "indirector",
    64: "cw-director",
    65: "ccw-director",
    66: "semirotator_cw",
    67: "semirotator_ccw",
    68: "semirotator_180",
    69: "toughslide",
    208: "diodediverger"
}

cell_cats: list[list[int]] = [
    # Categories of cells in the UI
    [], # Tools
    [1, 4, 5, 6, 7, 8, 22, 41, 42, 52, 53, 54, 69], # Basic
    [2, 14, 28, 58, 59, 60, 61], # Movers
    [3, 23, 26, 27, 32, 33, 34, 35, 36, 37, 40, 45, 46, 55], # Generators
    [9, 10, 11, 17, 18, 19, 30, 57, 62, 63, 64, 65, 66, 67, 68], # Rotators
    [21, 29, 15, 18, 19, 44, 50, 56], # Forcers
    [16, 31, 38, 39, 48, 49, 208], # Divergers
    [12, 13, 24, 44, 51], # Destroyers
    [], # Transformers
    [20, 25, 43, 47, "placeable"] # Misc
]

flip_guide: list[list[int]] = [
    # Guide for flipping cells
    [2, 0, 2, 0],
    [1, -1, 1, -1],
    [0, 2, 0, 2],
    [-1, 1, -1, 1]
]



def resource_path(relative_path):
    import os, sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

cell_images_raw: list[tuple[int | str, pygame.Surface]] = [] # The raw images of the cells
cell_id: int | str # Initialize cell_id
for cell_id in cell_names.keys(): # Iterate through the cell names
    cell_images_raw.append((cell_id, pygame.image.load(resource_path(f"textures/{cell_names[cell_id]}.png")))) # Load the image of the cell and add it to the list

cell_images: dict[int | str, pygame.Surface] = dict(cell_images_raw); # Convert the list to a dictionary

move_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/move.ogg")) # Load the move sound
rot_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/rotate.ogg")) # Load the rotate sound
trash_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/destroy.ogg")) # Load the destroy sound

def lerp(a, b, factor):
    '''Linear interpolation function'''
    return a + (b-a)*factor

def get_row(coord: tuple[int, int], dir: int, force_type: int = 0) -> tuple[list[tuple[int, int, int, tuple[int, int], int]], list[tuple[int, int]], list[int], bool]:
    '''Get a row of cells in a direction'''
    from main import cell_map # Import the cell map
    test: tuple[int, int, int, tuple[int, int], int] = (coord[0], coord[1], int(0), (0, 0), dir) # Initialize the test case
    temp: Cell # Initialize the temporary cell
    incr: tuple[int, int, int, tuple[int, int], int] # Initialize the incremented case
    result: list[tuple[int, int, int, tuple[int, int], int]] = [] # Initialize the result
    deltas: list[tuple[int, int]] = [] # Initialize the deltas
    delt_dirs: list[int] = [] # Initialize the delta directions
    fail = False # Initialize the fail flag
    current_dir: int = dir # Initialize the current direction
    while True:
        deltas.append(increment_with_divergers(test[0], test[1], current_dir, force_type)[3]) # Append the delta
        delt_dirs.append(increment_with_divergers(test[0], test[1], current_dir, force_type)[2]) # Append the delta direction
        if test[:2] not in cell_map.keys(): # If the cell is not in the cell map, break
            break
        temp = cell_map[test[:2]] # Get the cell

        incr = increment_with_divergers(test[0], test[1], test[4], force_type) # Increment the cell
        
        if (temp.tile_x, temp.tile_y) in [i[:2] for i in result]: # If the cell is already in the result, break
            #fail = True
            #break
            pass

        failure_sides = []
        if force_type == 0:
            failure_sides = ["wall", "undirectional", "unpushable"]
        elif force_type == 2:
            failure_sides = ["wall", "undirectional", "unpullable"]

        result.append(test) # Append the test case
        if temp.get_side((current_dir+2+force_type)%4) in failure_sides: # If the cell is a wall or unpushable,
            if temp.tile_x != coord[0] or temp.tile_y != coord[1]: # and if the cell is not the starting cell, break
                fail = True # Set the fail flag
                break


        current_dir += incr[2] # Increment the current direction
        current_dir %= 4 # Mod the current direction

        
        test = incr # Set the test case to the incremented case
        test = (test[0], test[1], current_dir, test[3], test[4]) # Set the test case to the incremented case
        
    return result, deltas, delt_dirs, fail # Return the result

def get_deltas(dir: int) -> tuple[int, int]:
    '''Gets the delta values of a direction.'''
    dx: int = 0 # Initialize the delta x
    dy: int = 0 # Initialize the delta y
    match dir%4:
        case 0: # Right
            dx = 1
            dy = 0
        case 1: # Down
            dx = 0
            dy = 1
        case 2: # Left
            dx = -1
            dy = 0
        case 3: # Up
            dx = 0
            dy = -1

    return dx, dy

def swap_cells(a: tuple[int, int], b: tuple[int, int]):
    '''Swaps two cells in the cell map.'''
    import main # Import the main module
    a_flag, b_flag = False, False # Initialize the flags
    first: Cell = Cell(0, 0, 0, 0) # Initialize the first cell
    second: Cell = Cell(0, 0, 0, 0) # Initialize the second cell
    if a in main.cell_map.keys(): # If a is in the cell map,
        first = main.cell_map[a] # Set the first cell to the cell at a
        first.tile_x, first.tile_y = b[0], b[1] # Set the tile x and y of the first cell to b
        a_flag = True # Set the a flag to True
    if b in main.cell_map.keys(): # If b is in the cell map,
        second = main.cell_map[b] # Set the second cell to the cell at b
        second.tile_x, second.tile_y = a[0], a[1] # Set the tile x and y of the second cell to a
        b_flag = True # Set the b flag to True
    if not a_flag and not b_flag: # If neither a nor b are in the cell map,
        return
    
    if a_flag: # If a is in the cell map,
         main.cell_map[b] = first # Set the cell at b to the first cell
    else: # If a is not in the cell map,
        del main.cell_map[b] # Delete the cell at b
    if b_flag: # If b is in the cell map,
        main.cell_map[a] = second # Set the cell at a to the second cell
    else: # If b is not in the cell map,
        del main.cell_map[a] # Delete the cell at a
   
def increment_with_divergers(x, y, dir: int, force_type = 0) -> tuple[int, int, int, tuple[int, int], int]:
    from main import cell_map # Import the cell map
    dx: int # Initialize the delta x
    dy: int # Initialize the delta y 
    dx, dy = get_deltas(dir) # Get the delta values of the direction
    current_x: int = x #+ dx # Set the current x to x plus dx
    current_y: int = y #+ dy # Set the current y to y plus dy
    current_dir: int = dir # Set the current direction to dir
    
    if (current_x, current_y) in cell_map.keys(): # If the current x and y are in the cell map,
        next_cell: Cell = cell_map[(current_x, current_y)] # Set the next cell to the cell at the current x and y
    else: # If the current x and y are not in the cell map,
        next_cell: Cell = Cell(current_x, current_y, 0, dir) # Set the next cell to a new cell at the current x and y with the id 0 and direction dir
    while True: # Loop forever
        dx, dy = get_deltas(current_dir) # Get the delta values of the current direction
        current_x += dx # Increment the current x by dx
        current_y += dy # Increment the current y by dy
        if (current_x, current_y) in cell_map.keys(): # If the current x and y are in the cell map,
            next_cell = cell_map[(current_x, current_y)] # Set the next cell to the cell at the current x and y
        else: # If the current x and y are not in the cell map,
            break # Break the loop
        
        match force_type: # Match the force type
            case 0: # Push force
                if next_cell.get_side((current_dir+2)%4) == "cwdiverger": # If the next cell is a CW diverger,
                    current_dir = (current_dir+1) # Rotate CW
                elif next_cell.get_side((current_dir+2)%4) == "ccwdiverger": # If the next cell is a CCW diverger,
                    current_dir = (current_dir-1) # Rotate CCW
                elif next_cell.get_side((current_dir+2)%4) == "diverger": # If the next cell is a straight diverger,
                    pass # Do nothing
                else: # If the next cell is not a diverger,
                    break # Break the loop
            case 2: # Pull force
                if next_cell.get_side((current_dir-1)%4) in ["cwdiverger", "forker", "triforker", "cwforker"]: # If the next cell is a CW diverger, forker, triforker, or CW forker,
                    current_dir = (current_dir-1) # Rotate CCW
                elif next_cell.get_side((current_dir+1)%4) in ["ccwdiverger", "forker", "triforker", "ccwforker"]: # If the next cell is a CCW diverger, forker, triforker, or CCW forker,
                    current_dir = (current_dir+1) # Rotate CW
                elif next_cell.get_side((current_dir)%4) in ["diverger", "triforker", "cwforker", "ccwforker"]: # If the next cell is a straight diverger, triforker, CW forker, or CCW forker,
                    pass # Do nothing
                else: # If the next cell is not a diverger, triforker, CW forker, or CCW forker,
                    break # Break the loop
            case _: # Default
                pass  # Do nothing



    return current_x, current_y, (current_dir - dir), (current_x-x, current_y-y), current_dir # Return the current x, current y, the difference between the current direction and the input direction, the delta x and y, and the current direction




def rot_center(image: pygame.Surface, rect: pygame.Rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle) # Rotate the image
    rot_rect = rot_image.get_rect(center=rect.center) # Get the rect of the rotated image
    return rot_image,rot_rect # Return the rotated image and rect

class Cell(pygame.sprite.Sprite):
    '''A class to represent a cell.'''
    def __init__(self, x: int, y: int, id: int | str, dir: int):
        '''Initialize the cell.'''
        # Initialize the sprite
        super().__init__()

        # Cell variables
        self.tile_x: int = x # Set the tile x to x
        self.tile_y: int = y # Set the tile y to y
        self.old_x: int = x # Set the old x to x
        self.old_y: int = y # Set the old y to y
        self.old_dir: int = dir # Set the old direction to dir
        self.id: int | str = id # Set the id to id
        self.name = cell_names[self.id] # Set the name to the name of the cell
        self.dir: int = dir # Set the direction to dir
        self.actual_dir: int = dir*-90 # Set the actual direction to dir times -90

        self.chirality = [-1, 0, 1, 2] # Set the chirality to -1, 0, 1, 2

        self.delta_dir = 0 # Set the delta direction to 0

        self.die_flag = False # Set the die flag to False

        # Image variables
        self.image: pygame.Surface = cell_images[self.id] # Set the image to the image of the cell
        self.rect: pygame.Rect = self.image.get_rect() # Set the rect to the rect of the image

        # Effect variables
        self.frozen: bool = False # Set the frozen flag to False
        self.protected: bool = False # Set the protected flag to False

        

        # Set cell-specific variables
        self.set_id(self.id) # Set the id of the cell

    def __repr__(self) -> str:
        '''Represent the cell as a string.'''
        return f"{self.name.title()} at {self.tile_x}, {self.tile_y}, id {self.id}, direction {self.dir}"
    
    def copy(self) -> Cell:
        '''Copy constructor'''
        return Cell(self.tile_x, self.tile_y, self.id, self.dir) # type: ignore

    def update(self):
        '''Update the cell, once per frame'''
        from main import cam_x, cam_y, TILE_SIZE, cell_map, update_timer, step_speed
        self.rect.centerx = lerp(int(self.tile_x*TILE_SIZE-cam_x), int(self.old_x*TILE_SIZE-cam_x), update_timer/step_speed)+TILE_SIZE/2
        self.rect.centery = lerp(int(self.tile_y*TILE_SIZE-cam_y), int(self.old_y*TILE_SIZE-cam_y), update_timer/step_speed)+TILE_SIZE/2
        self.actual_dir = lerp(self.dir*-90, (self.dir-self.delta_dir)*-90, update_timer/step_speed)

    def draw(self):
        '''Draw the cell on the screen'''
        from main import window, TILE_SIZE, freeze_image, WINDOW_HEIGHT, WINDOW_WIDTH, protect_image
        img: pygame.Surface = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        true_img, true_rect = rot_center(img, self.rect, self.actual_dir)
        if true_rect.y+TILE_SIZE < 0:
            return
        if true_rect.y > WINDOW_HEIGHT:
            return
        if true_rect.x+TILE_SIZE < 0:
            return 
        if true_rect.x > WINDOW_WIDTH:
            return
        # old_rect = self.rect.copy()
        
        window.blit(true_img, true_rect)
        if self.frozen:
            window.blit(pygame.transform.scale(freeze_image, (TILE_SIZE, TILE_SIZE)), true_rect)

        if self.protected:
            window.blit(pygame.transform.scale(protect_image, (TILE_SIZE, TILE_SIZE)), true_rect)

    def tick(self, dir: int):
        '''Tick the cell, once per tick'''
        
        self.push_extended = False
        self.pull_extended = False
        
        if (self.suppressed or self.frozen):
            return False
        self.do_replicate(dir)
        #self.do_flip()
        #self.do_rot()
        #self.do_gear()
        self.do_redirect()
        self.do_impulse(dir)
        self.do_repulse(dir)
        return True
    
    def on_force(self, dir, cell: Cell, suppress: bool = True, force_type = 0):
        from main import cell_map
        if self.id in [32, 33, 34, 35, 36, 37]:
            if self.get_side((dir+2)%4) == "trash":
                match (self.dir+dir)%4:
                    case 0:
                        self.eat_right = True
                    case 1:
                        self.eat_bottom = True
                    case 2:
                        self.eat_left = True
                    case 3: 
                        self.eat_top = True

        if self.get_side((dir+2)%4) == "fungal":
            cell.set_id(47)

        if force_type in [0, 2]:
            if self.get_side((dir+2)%4) in ["cwforker", "ccwforker", "triforker"]:
                new_cell_3: Cell = cell.copy()
                temp = increment_with_divergers(self.tile_x, self.tile_y, dir, 0)
                dx3, dy3 = temp[3]
                ddir = temp[2]
                new_cell_3.rot(ddir)
                new_cell_3.tile_x = self.tile_x+dx3
                new_cell_3.tile_y = self.tile_y+dy3
                if force_type == 0:
                    self.test_push((dir)%4, False, force=1)
                if (self.tile_x+dx3, self.tile_y+dy3) not in cell_map.keys():
                    cell_map[self.tile_x+dx3, self.tile_y+dy3] = new_cell_3
                    new_cell_3.suppressed = suppress
                    foo = increment_with_divergers(temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_3)
                elif "forker" in cell_map[self.tile_x+dx3, self.tile_y+dy3].get_side((dir+2+ddir)%4):
                    cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir)%4, new_cell_3, suppress=suppress)
                    del new_cell_3
                else:
                    print(cell_map[self.tile_x+dx3, self.tile_y+dy3])
                    cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir)%4, new_cell_3, suppress=suppress)

            if self.get_side((dir+2)%4) in ["forker", "cwforker", "triforker"]:

                # Fork CW
                new_cell_1: Cell = cell.copy()
                temp = increment_with_divergers(self.tile_x, self.tile_y, (dir-1)%4, 0)
                dx1, dy1 = temp[3]
                ddir = temp[2]
                new_cell_1.tile_x = self.tile_x+dx1
                new_cell_1.tile_y = self.tile_y+dy1
                new_cell_1.rot(-1+ddir)
                if force_type == 0:
                    self.test_push((dir-1)%4, False, force=1)
                if (self.tile_x+dx1, self.tile_y+dy1) not in cell_map.keys():
                    cell_map[self.tile_x+dx1, self.tile_y+dy1] = new_cell_1
                    new_cell_1.suppressed = suppress
                    foo = increment_with_divergers(temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_1)
                elif "forker" in cell_map[self.tile_x+dx1, self.tile_y+dy1].get_side((dir+1+ddir)%4):
                    cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+3+ddir)%4, new_cell_1, suppress=suppress)
                    del new_cell_1
                else:
                    cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+1+ddir)%4, new_cell_1)

            if self.get_side((dir+2)%4) in ["forker", "ccwforker", "triforker"]:
                # Fork CCW
                new_cell_2: Cell = cell.copy()
                temp = increment_with_divergers(self.tile_x, self.tile_y, (dir+1)%4, 0)
                dx2, dy2 = temp[3]
                ddir = temp[2]
                new_cell_2.tile_x = self.tile_x+dx2
                new_cell_2.tile_y = self.tile_y+dy2
                new_cell_2.rot(1+ddir)
                if force_type == 0:
                    self.test_push((dir+1)%4, False, force=1)
                if (self.tile_x+dx2, self.tile_y+dy2) not in cell_map.keys():
                    cell_map[self.tile_x+dx2, self.tile_y+dy2] = new_cell_2
                    new_cell_2.suppressed = suppress
                    foo = increment_with_divergers(temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_2)
                elif "forker" in cell_map[self.tile_x+dx2, self.tile_y+dy2].get_side((dir+3+ddir)%4):
                    cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+1+ddir)%4, new_cell_2, suppress=suppress)
                    del new_cell_2
                else:
                    cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+1+ddir)%4, new_cell_2)
            

        if self.demolishes:
            for i in range(4):
                dx, dy = get_deltas(i)
                if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
                    cell: Cell = cell_map[self.tile_x + dx, self.tile_y + dy]
                    if cell.get_side_by_delta(dx, dy) not in ["wall", "trash"]:
                        if dir != (i+2)%4:
                            del cell_map[self.tile_x + dx, self.tile_y + dy] 

            

    def set_id(self, id: int):
        '''Setter to set the id, while changing the image'''
        self.id = id
        self.image = cell_images[self.id]
        self.name = cell_names[self.id]

        # Wall: self explanatory
        # Undirectional: Like wall but can be affected by swap force and can be rotated
        # Generator: Generator OUTPUT
        # Unpushable / Unpullable: cannot be forced in the OPPOSITE direection

        # Sides
        self.left: str = "pushable" # Set the left side to pushable
        self.right: str = "pushable" # Set the right side to pushable
        self.top: str = "pushable" # Set the top side to pushable
        self.bottom: str = "pushable" # Set the bottom side to pushable

        self.br = "pushable"
        self.bl = "pushable"
        self.tl = "pushable"
        self.tr = "pushable"

        # Other cell variables
        self.hp: int = 1 # Set the hp to 1
        self.generation: str | int = "normal" # Set the generation to normal
        self.weight = 1 # Set the weight to 1

        # Push/pull variables
        self.pushes = False # Set the pushes flag to False
        self.pulls = False # Set the pulls flag to False
        self.drills = False
        self.swaps = False # Set the swaps flag to False
        self.gears = 0 # Set the gears flag to False
        self.demolishes = False
        self.mirrors = []

        # Flags
        self.suppressed = False # Set the suppressed flag to False
        self.eat_left = False # Set the eat left flag to False
        self.eat_right = False # Set the eat right flag to False
        self.eat_top = False # Set the eat top flag to False
        self.eat_bottom = False # Set the eat bottom flag to False

        match self.id:
            case 1:
                self.left = "wall"
                self.right = "wall"
                self.top = "wall"
                self.bottom = "wall"
            case 2:
                self.pushes = True
                self.chirality = [0]
            case 3:
                self.right = "generator"
                self.chirality = [0]
            case 5:
                self.top = "undirectional"
                self.bottom = "undirectional"
                self.chirality = [0, 2]
            case 6:
                self.top = "undirectional"
                self.bottom = "undirectional"
                self.right = "undirectional"
                self.chirality = [0]
            case 7:
                self.top = "undirectional"
                self.right = "undirectional"
                self.chirality = [-1]
            case 8:
                self.right = "undirectional"
                self.chirality = [0]
            case 9:
                self.top = "cwrotator"
                self.right = "cwrotator"
                self.bottom = "cwrotator"
                self.left = "cwrotator"
            case 10:
                self.top = "ccwrotator"
                self.right = "ccwrotator"
                self.bottom = "ccwrotator"
                self.left = "ccwrotator"
            case 11:
                self.top = "180rotator"
                self.right = "180rotator"
                self.bottom = "180rotator"
                self.left = "180rotator"
            case 12:
                self.left = "trash"
                self.right = "trash"
                self.top = "trash"
                self.bottom = "trash"
            case 13:
                self.left = "enemy"
                self.right = "enemy"
                self.top = "enemy"
                self.bottom = "enemy"
            case 14:
                self.pulls = True
                self.chirality = [0]
            case 15:
                self.swaps = True
                self.chirality = [0, 2]
                self.mirrors = [(0, 4)]
            case 16:
                self.right = "ccwdiverger"
                self.bottom = "cwdiverger"
                self.chirality = [-1]
            case 17:
                self.right = "redirector"
                self.bottom = "redirector"
                self.top = "redirector"
                self.left = "redirector"
                self.chirality = [0]
            case 18:
                self.gears = 1
            case 19:
                self.gears = -1
            case 20:
                self.generation = 0
            case 21:
                self.left = "repulse"
                self.right = "repulse"
                self.top = "repulse"
                self.bottom = "repulse"
            case 22:
                self.left = "weight"
                self.right = "weight"
                self.top = "weight"
                self.bottom = "weight"
            case 23:
                self.right = "generator"
                self.top = "generator"
                self.chirality = [1]
            case 24:
                self.left = "enemy"
                self.right = "enemy"
                self.top = "enemy"
                self.bottom = "enemy"
                self.hp = 2
            case 25:
                self.right = "freezer"
                self.top = "freezer"
                self.left = "freezer"
                self.bottom = "freezer"
            case 26:
                self.right = "cwgenerator"
                self.chirality = [0]
            case 27:
                self.right = "ccwgenerator"
                self.chirality = [0]
            case 28:
                self.pushes = True
                self.pulls = True
                self.chirality = [0]
            case 29:
                self.right = "impulse"
                self.top = "impulse"
                self.left = "impulse"
                self.bottom = "impulse"
            case 30:
                self.right = "flipper"
                self.top = "flipper"
                self.left = "flipper"
                self.bottom = "flipper"
                self.chirality = [0, 2]
            case 31:
                self.right = "ccwdiverger"
                self.bottom = "cwdiverger"
                self.top = "cwdiverger"
                self.left = "ccwdiverger"
                self.chirality = [1]
            case 32 | 33 | 34 | 35 | 36 | 37:
                self.left = "undirectional"
                self.right = "undirectional"
                self.top = "trash"
                self.bottom = "trash"
                self.chirality = [0]
            case 38:
                self.right = "diverger"
                self.left = "diverger"
                self.chirality = [0, 2]
            case 39:
                self.right = "diverger"
                self.bottom = "diverger"
                self.left = "diverger"
                self.top = "diverger"
            case 40:
                self.right = "twistgenerator"
                self.chirality = [0]
            case 41:
                self.left = "wall"
                self.right = "wall"
                self.top = "wall"
                self.bottom = "wall"
                self.generation = "ghost"
            case 42:
                self.left = "antiweight"
                self.right = "weight"
                self.chirality = [0]
            case 43:
                self.right = "shield"
                self.top = "shield"
                self.left = "shield"
                self.bottom = "shield"
            case 44:
                self.right = "intaker"
                self.chirality = [0]
            case 45:
                self.right = "replicator"
                self.chirality = [0]
            case 46:
                self.right = "replicator"
                self.top = "replicator"
                self.chirality = [1]
            case 47:
                self.right = "fungal"
                self.top = "fungal"
                self.left = "fungal"
                self.bottom = "fungal"
            case 48:
                self.left = "forker"
                self.chirality = [0]
            case 49:
                self.left = "triforker"
                self.chirality = [0]
            case 50:
                self.left = "superrepulse"
                self.right = "superrepulse"
                self.top = "superrepulse"
                self.bottom = "superrepulse"
            case 51:
                self.left = "trash"
                self.right = "trash"
                self.top = "trash"
                self.bottom = "trash"
                self.demolishes = True
            case 52:
                self.left = "unpullable"
                self.right = "unpushable"
                self.top = "undirectional"
                self.bottom = "undirectional"
                self.chirality = [0]
            case 53:
                self.left = "unpullable"
                self.right = "unpushable"
                self.bottom = "unpullable"
                self.top = "unpushable"
                self.chirality = [1]
            case 54:
                self.left = "unpullable"
                self.right = "unpushable"
                self.chirality = [0]
            case 55:
                self.right = "supergenerator"
                self.chirality = [0]
            case 56:
                self.mirrors = [(0, 4), (2, 6)]
                self.chirality = [0, 1, 2, 3]
            case 57:
                self.right = "cwrotator"
                self.bottom = "cwrotator"
                self.left = "ccwrotator"
                self.top = "ccwrotator"
                self.chirality = [3]
            case 58:
                self.drills = True
                self.chirality = [0]
            case 59:
                self.drills = True
                self.pushes = True
                self.chirality = [0]
            case 60:
                self.drills = True
                self.pushes = True
                self.pulls = True
                self.chirality = [0]
            case 61:
                self.drills = True
                self.pulls = True
                self.chirality = [0]
            case 62:
                self.right = "outdirector"
                self.bottom = "outdirector"
                self.left = "outdirector"
                self.top = "outdirector"
            case 63:
                self.right = "indirector"
                self.bottom = "indirector"
                self.left = "indirector"
                self.top = "indirector"
            case 64:
                self.right = "cwdirector"
                self.bottom = "cwdirector"
                self.left = "cwdirector"
                self.top = "cwdirector"
            case 65:
                self.right = "ccwdirector"
                self.bottom = "ccwdirector"
                self.left = "ccwdirector"
                self.top = "ccwdirector"
            case 66:
                self.left = "cwrotator"
                self.right = "cwrotator"
            case 67:
                self.left = "ccwrotator"
                self.right = "ccwrotator"
            case 68:
                self.left = "180rotator"
                self.right = "180rotator"
            case 69:
                self.top = "wall"
                self.bottom = "wall"
            case 208:
                self.left = "diverger"
                self.chirality = [0]

    def test_push(self, dir: int, move: bool, hp: int = 1, force: int = 0, speed: int = 1) -> bool | int:
        '''Tests a push, and returns False if failed'''
        from main import cell_map, delete_map
        if self not in cell_map.values():
            return False
        if speed == 1 or not move:
            dx: int
            dy: int
            dx, dy = get_deltas(dir)
            bias: int = force
            row, deltas, ddirs, fail = get_row((self.tile_x, self.tile_y), dir, 0)
            trash_flag = False
            suicide_flag = False
            enemy_flag = False
            killer_cell = None
            killer_cell_hp = 0
            affected_cells = [row[0]]
            new_x: int = 0
            new_y: int = 0
            new_dir: int = 0

            #if move:
            new_x, new_y, new_dir, _, _ = increment_with_divergers(self.tile_x, self.tile_y, dir)
            for x, y, _, __, con_dir in row[1:]:
                affected_cells.append((x, y, _, __, con_dir))
                cell = cell_map[x, y]
                if cell.get_side((con_dir+2)%4) in ["wall", "undirectional", "unpushable"]:
                    cell.on_force(con_dir, cell_map[affected_cells[-2][:2]])
                    return False
                if  ("trash" in cell.get_side((con_dir+2)%4)) or ("forker" in cell.get_side((con_dir+2)%4)):
                    trash_flag = True
                    break
                if "enemy" in cell.get_side((con_dir+2)%4):
                    if not cell_map[affected_cells[-2][:2]].protected and not cell.protected:
                        enemy_flag = True
                        break
                if cell.pushes and cell.dir == con_dir:
                    cell.suppressed = True

            if self.pushes and self.dir == row[0][4]:
                    self.suppressed = True


            cell = cell_map[affected_cells[0][:2]]
            if cell.get_side((dir+2)%4) in ["wall", "trash", "undirectional", "forker", "triforker", "cwforker", "ccwforker"]:
                return False
            con_dir = affected_cells[0][4]
            x = affected_cells[0][0]
            y = affected_cells[0][1]
            if (cell.pushes, cell.dir) == (True, con_dir):
                bias += 1
            if (cell.pushes, cell.dir) == (True, (con_dir+2)%4) and not cell.frozen:
                bias -= 1
            if cell.get_side((dir+2)%4) == "repulse":
                bias -= 1
            if self.get_side((dir)%4) == "repulse":
                bias += 1
            if cell.get_side((dir+2)%4) == "weight":
                bias -= cell_map[x, y].weight
            if cell.get_side((dir+2)%4) == "antiweight":
                bias += cell_map[x, y].weight

            if bias <= 0:
                print("fell")
                return False
            
            row = affected_cells[:]

            if trash_flag:
                killer_cell = row[-1]
                if move or len(row) > 2:
                    if "trash" in cell_map[killer_cell[:2]].get_side((dir+2)%4):             
                        trash_sound.play()
                    cell_map[row[-2][:2]].die_flag = True

                    cell_map[killer_cell[:2]].on_force(killer_cell[4], cell_map[row[-2][:2]])
                if row[-2][:2] == (self.tile_x, self.tile_y):
                    suicide_flag = True
                else:
                    cell_map[row[-2][:2]].tile_x = killer_cell[0]
                    cell_map[row[-2][:2]].tile_y = killer_cell[1]
                    if "forker" not in cell_map[killer_cell[:2]].get_side((dir+2)%4):  
                        delete_map.append(cell_map[row[-2][:2]])
                    del cell_map[row[-2][:2]]
                del row[-2]
                del row[-1]
            elif enemy_flag:
                killer_cell: Cell = row[-1][:2]
                if not cell_map[killer_cell].protected and not cell_map[row[-2][:2]].protected:
                    trash_sound.play()
                    cell_map[row[-2][:2]].die_flag = True
                    if cell_map[row[-2][:2]] == self:
                        suicide_flag = True
                    else:
                        #cell_map[row[-2][:2]].tile_x = killer_cell[0]
                        #cell_map[row[-2][:2]].tile_y = killer_cell[1]
                        #delete_map.append(cell_map[row[-2][:2]])
                        del cell_map[row[-2][:2]]
                        del row[-2]
                    killer_cell_hp = cell_map[killer_cell].hp
                    cell_map[killer_cell].hp -= hp
                    if cell_map[killer_cell].hp <= 0:
                        del cell_map[killer_cell]
                    elif cell_map[killer_cell].id == 24:
                        cell_map[killer_cell].set_id(13)
                    del row[-1]
            
            move_sound.play()
            temp: list[Cell] = []
            for x, y, _, _, _ in row[1:]:
                temp.append(cell_map[(x, y)])
            '''for cell in temp:
                if (cell.tile_x, cell.tile_y) in cell_map.keys():
                    del cell_map[cell.tile_x, cell.tile_y]'''

            if move:
                if len(temp) > 0:
                    temp[0].on_force((dir+new_dir)%4, self)

            if False:
                for i, item in enumerate(row[1:]):
                    
                    dx, dy = deltas[i+1]
                    ddir = ddirs[i+1]
                    cell_map[(item[0]+dx, item[1]+dy)] = temp[i]
                    #if temp[i].dir == dir - 
                    temp[i].tile_x += dx
                    temp[i].tile_y += dy
                    temp[i].rot(ddirs[i+1])
                    #temp[i].dir %= 4
                    temp[i].on_force(item[4], temp[i-1])
            else:
                if move:
                    del cell_map[(self.tile_x, self.tile_y)]
                if (new_x, new_y) in cell_map.keys():
                    #if (new_x, new_y) != (self.tile_x, self.tile_y):
                        try:
                            if not cell_map[new_x, new_y].test_push(dir+new_dir, True, force=bias, speed=speed):
                                pass
                                #return False
                        except RecursionError:
                            return False

        
            if move:
                
                if not suicide_flag:
                    if (new_x, new_y) in cell_map.keys():
                        cell_map[(self.tile_x, self.tile_y)] = self
                        return False
                    
                    #
                    cell_map[new_x, new_y] = self
                    self.tile_x = new_x
                    self.tile_y = new_y
                    self.rot(new_dir)
                else:
                    if (self.tile_x, self.tile_y) in cell_map.keys():
                        del cell_map[(self.tile_x, self.tile_y)]
                    self.tile_x = killer_cell[0]
                    self.tile_y = killer_cell[1]
                    self.rot(new_dir)
                    if trash_flag:
                        if "forker" not in cell_map[killer_cell[:2]].get_side((dir+2)%4):  
                            delete_map.append(self)

                if self.pushes or self.pulls:
                    if self.dir == dir+new_dir:
                        self.suppressed = True

            if killer_cell is not None:
                return hp-killer_cell_hp
            else:
                return hp
        elif speed != float("inf"):
            for i in range(speed):
                self.test_push(dir, move, hp, force)
        else:
            if move:
                while self.test_push(dir, move, hp, force):
                    pass

        return True

    
    def test_pull(self, dir: int, move: bool, force: int = 0) -> bool:
        '''Tests a pull, and returns False if failed'''
        from main import cell_map, delete_map
        dx, dy = get_deltas(dir)
        push_flag = False
        new_x: int = 0
        new_y: int = 0
        new_dir: int = 0
        old_x = self.tile_x
        old_y = self.tile_y
        old_dir = self.dir
        killer_cell: tuple[int, int] = (0, 0)
        fail = False
        affected = []

        if move:
            row, deltas, ddirs, fail = get_row((self.tile_x, self.tile_y), (dir+2)%4, 2)
        else:
            back_cell_coord = increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4, 2)[:2]
            starting_x, starting_y = increment_with_divergers(back_cell_coord[0], back_cell_coord[1], (dir+2)%4, 2)[:2]
            
            row, deltas, ddirs, fail = get_row((starting_x, starting_y), (dir+2)%4, 2)
        
        row_cells = [cell_map[item[:2]] for item in row]
            
        suicide_flag = False
        enemy_flag = False
        row_interrupt_flag = False
        if move:
            new_x, new_y, new_dir, delta, _ = increment_with_divergers(self.tile_x, self.tile_y, dir, 0)
            bias = force+int(self.pulls)
            total_bias = force
        else:
            bias = force+1
            total_bias = force+1

        for i, cell in enumerate(row_cells):
            if cell.pushes and (cell.dir+2)%4 == row[i][4]:
                push_flag = True
        if move:
            if (new_x, new_y) in cell_map.keys():
                front_cell = cell_map[new_x, new_y]
                if front_cell.pushes:
                    push_flag = True
                if "trash" in front_cell.get_side((dir+new_dir+2)%4) or "enemy" in front_cell.get_side((dir+new_dir+2)%4) or "forker" in front_cell.get_side((dir+new_dir+2)%4):
                    killer_cell = (new_x, new_y)
                    if move:
                        suicide_flag = True
                        if cell_map[killer_cell].id in [13, 24]:
                            if not self.protected:
                                enemy_flag = True
                        cell_map[killer_cell].on_force(self.dir + new_dir, self, force_type=2)
                else:
                    if move:
                        if (not (push_flag or front_cell.pushes)):
                            return False
        if increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4, 2)[:2] in cell_map.keys():
            if not move:
                return False
        for x, y, ddir, a, con_dir in row:
            cell = cell_map[x, y]
            affected.append((x, y, ddir, a, con_dir))
            #cell = cell_map[x, y]
            if (cell.pulls, cell.dir) == (True, (con_dir+2)%4):
                total_bias += 1
            if (cell.pulls, cell.dir) == (True, con_dir) and not cell.frozen:
                total_bias -= 1
            if cell.get_side((con_dir+2)%4) == "impulse":
                total_bias -= 1
            if cell.get_side((dir+2)%4) == "weight":
                total_bias -= cell_map[x, y].weight
            if cell.get_side((dir+2)%4) == "antiweight":
                total_bias += cell_map[x, y].weight

        

        if len(row) > 1:
            cell = cell_map[row[1][:2]]
            if (cell.pulls, cell.dir) == (True, (con_dir+2)%4):
                bias += 1
            if (cell.pulls, cell.dir) == (True, con_dir) and not cell.frozen:
                bias -= 1
            if cell.get_side((con_dir+2)%4) == "impulse":
                bias -= 1
            if cell.get_side((dir+2)%4) == "weight":
                bias -= cell_map[x, y].weight
            if cell.get_side((dir+2)%4) == "antiweight":
                bias += cell_map[x, y].weight

        if total_bias <= 0:
            if self.pulls:
                print("fail")
            return False

        if fail:
            return False
        if row_interrupt_flag:
            cell_map[affected[-1][:2]].on_force((-affected[-1][4])%4, cell_map[affected[-2][:2]], force_type=2)
            affected = affected[:-1]
        row = affected[:]

        if enemy_flag:
            if cell_map[killer_cell].id == 24:
                cell_map[killer_cell].set_id(13)
            else:
                del cell_map[killer_cell]
        if bias <= 0:
            return False
        if fail and len(row) > 1:
            return False
        
        if push_flag:
            print("e")
            if not self.test_push(dir, False):
                print("f")
                #return False
        move_sound.play()
        if (new_x, new_y) in cell_map.keys() and not suicide_flag:
            return False
        if move:
            del cell_map[(self.tile_x, self.tile_y)]
            if not suicide_flag:
                cell_map[(new_x, new_y)] = self
                self.tile_x = new_x
                self.tile_y = new_y
                self.rot(new_dir)

            else:
                trash_sound.play()
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                if not enemy_flag and "forker" not in cell_map[killer_cell].get_side((dir+2)%4):
                    delete_map.append(self)
        
        temp: list[Cell] = []
        affected_cells = row[:]
        if move:
            if affected_cells:
                del affected_cells[0]

        if move:
            pulled_cells = row[1:]
        else:
            pulled_cells = row

        #if move:
            #if len(temp) > 0:
                #temp[0].on_force((self.dir+new_dir)%4, self)
        if False:
            for i, item in enumerate(pulled_cells):
                
                dx, dy = deltas[i]
                cell_map[(item[0]-dx, item[1]-dy)] = temp[i]
                temp[i].tile_x -= dx
                temp[i].tile_y -= dy
                temp[i].rot(-ddirs[i])
                temp[i].on_force(item[4], temp[i-1], force_type=1)
        else:
            if move:
                if len(row) > 1:
                    
                    if move:
                        if cell_map[row[1][:2]].get_side((dir+2)%4) not in ["wall", "undirectional", "unpullable", "trash"]:
                            cell_map[row[1][:2]].test_pull((row[1][4]+2)%4, True, force=bias)
            else:
                if len(row) > 0:
                    if cell_map[starting_x, starting_y].get_side((dir+2)%4) not in ["wall", "undirectional", "unpullable", "trash"]:
                        cell_map[starting_x, starting_y].test_pull((row[0][4]+2)%4, True, force=bias)


        if self.pulls or self.pushes:
            if self.dir == dir+new_dir:
                self.suppressed = True


        return True
    
    def test_swap(self, dx1, dy1, dx2, dy2) -> bool:
        '''0: horizontal, 1: neg-diag, 2: vertical, 3: pos-diag'''
        from main import cell_map

        if (self.tile_x + dx1, self.tile_y + dy1) in cell_map.keys():
            if cell_map[(self.tile_x + dx1, self.tile_y + dy1)].get_side_by_delta(dx1, dy1) in ["wall", "trash", "enemy"] or cell_map[(self.tile_x + dx1, self.tile_y + dy1)].swaps:
                return False
        if (self.tile_x + dx2, self.tile_y + dy2) in cell_map.keys():
            if cell_map[(self.tile_x + dx2, self.tile_y + dy2)].get_side_by_delta(dx2, dy2) in ["wall", "trash", "enemy"] or cell_map[(self.tile_x + dx2, self.tile_y + dy2)].swaps:
                return False
        
        swap_cells((self.tile_x + dx1, self.tile_y + dy1), (self.tile_x + dx2, self.tile_y + dy2))

        return True

    def test_rot(self, dir: int, rot: int) -> bool:
        from main import cell_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) in cell_map.keys():
            target_cell: Cell = cell_map[(self.tile_x+dx, self.tile_y+dy)]
        else:
            return False
        if target_cell.get_side((dir+2)%4) == "wall":
            return False
        
        rot_sound.play()
        target_cell.rot(rot)
        return True
    
    def test_redirect(self, dir: int, rot: int) -> bool:
        from main import cell_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) in cell_map.keys():
            target_cell: Cell = cell_map[(self.tile_x+dx, self.tile_y+dy)]
        else:
            return False
        if target_cell.get_side((dir+2)%4) == "wall":
            return False
        
        rot_sound.play()
        target_cell.rot((-target_cell.dir+rot+1)%4-1)
        return True
    
    def redirect(self, dir) -> bool:
        self.rot((-self.dir+dir+1)%4-1)

    def gen(self, dir, cell: Cell) -> Cell:
        from main import cell_map
        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.tile_x, self.tile_y, (dir)%4)[3]
        odx, ody = increment_with_divergers(self.tile_x, self.tile_y, (dir)%4)[3]
        generated_cell: Cell = cell
        if generated_cell.generation == "ghost":
            return False
        # Cells have already been pushed
        # Just create new cells if you have to
        behind_hp = self.test_push(dir, False, cell.hp, force=1)
        if not behind_hp:
            return False
        # Cells have already been pushed
        # Just create new cells if you have to
        if (self.tile_x + dx, self.tile_y + dy) not in cell_map.keys():
            generated_cell.hp = behind_hp
            generated_cell.old_x = self.tile_x
            generated_cell.old_y = self.tile_y
            if generated_cell.hp == 1 and generated_cell.id == 24:
                generated_cell.set_id(13)
            if generated_cell.hp == 0:
                return True

            if cell.generation != 'normal':
                cell.generation -= 1

            cell_map[(self.tile_x + dx, self.tile_y + dy)] = generated_cell
            return generated_cell
        else:
            return None
        
    def check_generation(self):
        from main import cell_map
        if type(self.generation) != int:
            return
        if self.generation < 0:
            del cell_map[self.tile_x, self.tile_y]


    
    def test_gen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False) -> bool:
        from main import cell_map

        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.tile_x, self.tile_y, (dir-angle+2)%4)[3]
        oddir, (odx, ody) = increment_with_divergers(self.tile_x, self.tile_y, dir)[2:4]
        enemy_flag = False
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():

            behind_cell: Cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
        else:
            return False
        generated_cell: Cell = Cell(self.tile_x+odx, self.tile_y+ody, behind_cell.id, (behind_cell.dir+angle)%4)
        if clone:
            generated_cell.flip((dir*2+2)%4)
        if suppress:
            generated_cell.suppressed = True        
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
            
            print(oddir)
            #generated_cell.rot(oddir)
            if clone:
                generated_cell.dir = behind_cell.dir
        else: 
            return False
        
        if behind_cell.generation == "ghost":
            return False
        temp = increment_with_divergers(self.tile_x, self.tile_y, (dir-angle)%4)
        if temp[:2] in cell_map.keys():
            cell_map[temp[:2]].on_force(temp[4], generated_cell, suppress=False)


        new_cell = self.gen(dir, generated_cell)
        if type(new_cell) == Cell:
            new_cell.check_generation()

    
    def test_supergen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False) -> bool:
        from main import cell_map

        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.tile_x, self.tile_y, (dir-angle+2)%4)[3]
        oddir, (odx, ody) = increment_with_divergers(self.tile_x, self.tile_y, dir)[2:4]
        row, _, ddirs, _ = get_row((self.tile_x, self.tile_y), (dir+2)%4, force_type=2)
        total_ddir = 0
        new_cells = []
        for i, item in enumerate(row[1:]):
            cell = cell_map[item[:2]]
            generated_cell = cell.copy()
            generated_cell.tile_x = self.tile_x+odx
            generated_cell.tile_y = self.tile_y+ody
            total_ddir -= ddirs[i]
            generated_cell.dir += (total_ddir)
            new_cell = self.gen(dir, generated_cell)
            if not new_cell:
                return
            new_cells.append(new_cell)

        for cell in new_cells:
            cell.check_generation()
        

        
    def test_replicate(self, dir: int) -> bool:
        self.test_gen(dir, 2, clone=True)
    
    def test_gear(self, rot: int) -> bool:
        from main import cell_map
        if rot == 0:
            return False
        surrounding_cells = [(self.tile_x + 1, self.tile_y),
                             (self.tile_x + 1, self.tile_y + 1),
                             (self.tile_x, self.tile_y + 1),
                             (self.tile_x - 1, self.tile_y + 1),
                             (self.tile_x - 1, self.tile_y),
                             (self.tile_x - 1, self.tile_y - 1),
                             (self.tile_x, self.tile_y - 1),
                             (self.tile_x + 1, self.tile_y - 1),]
        if rot > 0:
            surrounding_cells.reverse()
        for i, coord in enumerate(surrounding_cells):
            if coord in cell_map.keys():
                if cell_map[coord].get_side(i//2) == "wall":
                    return False
                if cell_map[coord].id in [18, 19]:
                    return False
        for i in range(7):
            swap_cells(surrounding_cells[i], surrounding_cells[i+1])
        for i in range(1, 8, 2):
            if surrounding_cells[i] in cell_map.keys():
                cell_map[surrounding_cells[i]].dir += rot
                cell_map[surrounding_cells[i]].dir %= 4

        return True
            
    def test_freeze(self, dir: int) -> bool:
        from main import cell_map
        dx, dy = get_deltas(dir)
        if ((self.tile_x + dx, self.tile_y + dy)) in cell_map.keys():
            target_cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
            if target_cell.get_side(dir) == "wall" or target_cell.id == 25:
                return False
            target_cell.frozen = True
        return True
    
    def test_protect(self, dx: int, dy: int) -> bool:
        from main import cell_map
        #dx, dy = get_deltas(dir)
        if ((self.tile_x + dx, self.tile_y + dy)) in cell_map.keys():
            target_cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
            target_cell.protected = True
        return True
    
    def test_intake(self, dir: int):
        from main import cell_map, delete_map
        deleted = increment_with_divergers(self.tile_x, self.tile_y, dir, 2)
        if deleted[:2] not in cell_map.keys():
            return False
        deleted_cell = cell_map[deleted[:2]]
        if deleted_cell.get_side(dir%4) in ["wall", "undirectional", "unpullable"]:
            return False
        del cell_map[deleted[:2]]
        if not self.test_pull((dir+2)%4, False):
            cell_map[deleted[:2]] = deleted_cell
            return False
        trash_sound.play()
        delete_map.append(deleted_cell)
        deleted_cell.tile_x = self.tile_x
        deleted_cell.tile_y = self.tile_y

    
    def rot(self, rot: int):
        #rot %= 4
        self.dir += rot
        self.delta_dir += rot
        self.dir %= 4
    
    def flip(self, rot: int):
        target_cell = self
        cell_symmetry = (self.chirality[0] + 2*self.dir)%4
        self.rot(flip_guide[(rot-cell_symmetry)%4][0])
        if "ccw" in target_cell.name:
            target_cell.set_id(target_cell.id-1)
        elif "cw" in target_cell.name:
            target_cell.set_id(target_cell.id+1)

    def test_flip(self, dir: int, rot: int) ->  bool:
        from main import cell_map
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) not in cell_map.keys():
            return False

        target_cell = cell_map[self.tile_x+dx, self.tile_y+dy]
        target_cell.flip(rot)

        return True

        


    def do_push(self, dir):
        if self.suppressed or self.frozen:
            return
        if self.pushes and not self.pulls and self.dir == dir and not self.drills:
            self.test_push(dir, True)

    def do_repulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "repulse":
            self.test_push(dir, False, force=1)

    def do_super_repulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "superrepulse":
            self.test_push(dir, False, 1, float("inf"), float("inf"))

    def do_impulse(self, dir: int):
        if self.frozen:
            return
        if self.id == 29:
            self.test_pull(dir, False)

    def do_pull(self, dir):
        if self.frozen or self.suppressed:
            return
        if self.pulls and self.dir == dir and not self.drills:
            self.test_pull(dir, True)

    def test_drill(self, dir):
        from main import cell_map, delete_map
        dx, dy = get_deltas(dir)
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
            if cell_map[(self.tile_x + dx, self.tile_y + dy)].get_side((dir+2)%4) == "wall":
                return False
            elif cell_map[(self.tile_x + dx, self.tile_y + dy)].get_side((dir+2)%4) == "trash":
                del cell_map[self.tile_x, self.tile_y]
                delete_map.append(self)
                self.tile_x += dx
                self.tile_y += dy
                return
        swap_cells((self.tile_x, self.tile_y), (self.tile_x + dx, self.tile_y + dy))
        return True
    def do_drill(self, dir):
        falg=False
        if self.frozen or self.suppressed:
            return
        if self.pushes:
            if self.test_push(dir, True):
                falg=True
            if self.pulls:
                self.test_pull(dir, False)
            if falg:
                return
        if self.drills and self.dir == dir:
            self.test_drill(dir)
            if self.pulls:
                self.test_pull(dir, False)
    
    def do_gen(self, dir: int):
        if self.frozen:
            return

        if self.get_side(dir) == "generator":
            print("g")
            self.test_gen(dir, 0)
        if self.get_side(dir) == "cwgenerator":
            print("g")
            self.test_gen(dir, 1)
        if self.get_side(dir) == "ccwgenerator":
            print("g")
            self.test_gen(dir, -1)

    def do_super_gen(self, dir: int):
        if self.frozen:
            return

        if self.get_side(dir) == "supergenerator":
            print("g")
            self.test_supergen(dir, 0)
        if self.get_side(dir) == "cwsupergenerator":
            print("g")
            self.test_supergen(dir, 1)
        if self.get_side(dir) == "ccwsupergenerator":
            print("g")
            self.test_supergen(dir, -1)

    def do_gate(self, dir: int):
        if self.frozen:
            return

        if self.id == 32:
            if self.eat_top or self.eat_bottom:
                if self.dir == dir:
                    self.test_gen(dir, 0)

        if self.id == 33:
            if self.eat_top and self.eat_bottom:
                if self.dir == dir:
                    self.test_gen(dir, 0)

        if self.id == 34:
            if self.eat_top != self.eat_bottom:
                if self.dir == dir:
                    self.test_gen(dir, 0)

        if self.id == 35:
            if not (self.eat_top or self.eat_bottom):
                if self.dir == dir:
                    self.test_gen(dir, 0)

        if self.id == 36:
            if not (self.eat_top and self.eat_bottom):
                if self.dir == dir:
                    self.test_gen(dir, 0)

        if self.id == 37:
            if not (self.eat_top != self.eat_bottom):
                if self.dir == dir:
                    self.test_gen(dir, 0)

        if self.id == 40:
            if self.dir == dir:
                self.test_gen(dir, 0, True)

    def do_replicate(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "replicator":
            self.test_replicate(dir)

    def do_intake(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "intaker":
            self.test_intake(dir)

    def do_rot(self):
        if self.frozen:
            return
        for i in range(4):
            if self.get_side(i) == "cwrotator":
                self.test_rot(i, 1)
            if self.get_side(i) == "ccwrotator":
                self.test_rot(i, -1)
            if self.get_side(i) == "180rotator":
                self.test_rot(i, 2)

    def do_flip(self):
        if self.frozen:
            return
        if self.id == 30:
            if self.dir in [0, 2]:
                for i in range(4):
                    self.test_flip(i, 0)
            if self.dir in [1, 3]:
                for i in range(4):
                    self.test_flip(i, 2)

    def do_mirror(self, dir1, dir2):
        dir_to_delta: list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        dx1, dy1 = dir_to_delta[dir1]
        dx2, dy2 = dir_to_delta[dir2]
        if self.frozen:
            return
        if (dir1, dir2) in self.mirrors or (dir2, dir1) in self.mirrors:
            self.test_swap(dx1, dy1, dx2, dy2)

    def do_redirect(self):
        if self.frozen:
            return
        for i in range(4):
            if self.get_side(i) == "redirector":
                self.test_redirect(i, self.dir)
            if self.get_side(i) == "outdirector":
                self.test_redirect(i, i)
            if self.get_side(i) == "indirector":
                self.test_redirect(i, (i+2)%4)
            if self.get_side(i) == "cwdirector":
                self.test_redirect(i, (i+1)%4)
            if self.get_side(i) == "ccwdirector":
                self.test_redirect(i, (i+3)%4)
    
    def do_gear(self, dir):
        if self.frozen:
            return
        if self.gears == dir:
            self.test_gear(self.gears)

    def do_freeze(self, dir):
        if self.frozen:
            return
        if self.get_side(dir) == "freezer":
            self.test_freeze(dir)

    def do_protect(self):
        if self.frozen:
            return
        if self.id == 43:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.test_protect(i, j)

    def get_side(self, dir: int) -> str:
        dir%=4
        dir *= 2
        dir = int(dir)
        match self.dir:
            case 0:
                return [self.right, self.br, self.bottom, self.bl, self.left, self.tl, self.top, self.tr][dir]
            case 1:
                return [self.top, self.tr, self.right, self.br, self.bottom, self.bl, self.left, self.tl][dir]
            case 2:
                return [self.left, self.tl, self.top, self.tr, self.right, self.br, self.bottom, self.bl][dir]
            case 3:
                return [self.bottom, self.bl, self.left, self.tl, self.top, self.tr, self.right, self.br][dir]
        return "error"
    
    def get_side_by_delta(self, dx, dy):
        if dx == 0 and dy == 0:
            return "error"
        if dx == 0:
            if dy > 0:
                return self.get_side(1)
            if dy < 0:
                return self.get_side(3)
        if dy == 0:
            if dx > 0:
                return self.get_side(0)
            if dx < 0:
                return self.get_side(2)
        
        tangent = atan2(dy, dx)
        if tangent < pi/2:
            return self.get_side(3.5)
        elif tangent < pi:
            return self.get_side(2.5)
        elif tangent < 3*pi/2:
            return self.get_side(1.5)
        else:
            return self.get_side(0.5)




        
        
        
