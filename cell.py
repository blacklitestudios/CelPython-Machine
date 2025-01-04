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
    70: "pararotator",
    71: "grabber",
    72: "heaver",
    73: "lugger",
    74: "hoister",
    75: "raker",
    76: "borer",
    77: "carrier",
    78: "omnipower",
    79: "ice",
    80: "termirror",
    81: "grapulsor_cw",
    82: "grapulsor_ccw",
    83: "bivalvediverger",
    84: "paravalvediverger_cw",
    85: "paravalvediverger_ccw",
    86: "bivalvedisplacer",
    87: "paravalvedisplacer_cw",
    88: "paravalvedisplacer_ccw",
    89: "semiflipper_h",
    90: "semiflipper_v",
    91: "displacer",
    92: "bidisplacer",
    93: "valvediverger_cw",
    94: "valvediverger_ccw",
    95: "valvedisplacer_cw",
    96: "valvedisplacer_ccw",
    97: "cwforker",
    98: "ccwforker",
    114: "nudger",
    208: "diodediverger",
}

cell_cats: list[list[int | str]] = [
    # Categories of cells in the UI
    [], # Tools
    [1, 4, 5, 6, 7, 8, 22, 41, 42, 52, 53, 54, 69], # Basic
    [2, 14, 28, 58, 59, 60, 61, 71, 72, 73, 74, 75, 76, 77, 78, 114], # Movers
    [3, 23, 26, 27, 32, 33, 34, 35, 36, 37, 40, 45, 46, 55], # Generators
    [9, 10, 11, 17, 18, 19, 30, 57, 62, 63, 64, 65, 66, 67, 68, 70, 89, 90], # Rotators
    [21, 29, 15, 18, 19, 44, 50, 56, 80, 81, 82], # Forcers
    [16, 31, 38, 39, 48, 49, 79, 83, 84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 96, 97, 98, 208], # Divergers
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
        base_path = sys._MEIPASS # type: ignore
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
        elif force_type == 3:
            failure_sides = ["wall", "undirectional", "ungrabbable"]

        result.append(test) # Append the test case
        if temp.get_side((current_dir+2+force_type)) in failure_sides: # If the cell is a wall or unpushable,
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
   
def increment_with_divergers(x, y, dir: int, force_type = 0, displace=False) -> tuple[int, int, int, tuple[int, int], int]:
    dir %= 4
    from main import cell_map # Import the cell map
    dx: int # Initialize the delta x
    dy: int # Initialize the delta y 
    dx, dy = get_deltas(dir) # Get the delta values of the direction
    current_x: int = x #+ dx # Set the current x to x plus dx
    current_y: int = y #+ dy # Set the current y to y plus dy
    current_dir: int = dir # Set the current direction to dir
    stop_flag: bool = False
    
    if (current_x, current_y) in cell_map.keys(): # If the current x and y are in the cell map,
        next_cell: Cell = cell_map[(current_x, current_y)] # Set the next cell to the cell at the current x and y
    else: # If the current x and y are not in the cell map,
        next_cell: Cell = Cell(current_x, current_y, 0, dir) # Set the next cell to a new cell at the current x and y with the id 0 and direction dir
    while True: # Loop forever
        dx, dy = get_deltas(current_dir) # Get the delta values of the current direction
        cwdx, cwdy = get_deltas(current_dir+1)
        ccwdx, ccwdy = get_deltas(current_dir - 1)
        if not stop_flag:
            current_x += dx # Increment the current x by dx
            current_y += dy # Increment the current y by dy

        stop_flag = False

        if (current_x, current_y) in cell_map.keys(): # If the current x and y are in the cell map,
            next_cell = cell_map[(current_x, current_y)] # Set the next cell to the cell at the current x and y
        else: # If the current x and y are not in the cell map,
            if (current_x+cwdx, current_y+cwdy) in cell_map.keys():
                if cell_map[current_x+cwdx, current_y+cwdy].get_side(current_dir-1) in ["ice"]:
                    continue
                else:
                    break
            elif (current_x+ccwdx, current_y+ccwdy) in cell_map.keys():
                if cell_map[current_x+ccwdx, current_y+ccwdy].get_side(current_dir+1) in ["ice"]:
                    continue
                else:
                    break
            else:
                break
        
        
        
        match force_type: # Match the force type

            case 2: # Pull force

                if next_cell.get_side((current_dir-1)) in ["cwdiverger", "forker", "triforker", "cwforker"]: # If the next cell is a CW diverger, forker, triforker, or CW forker,
                    current_dir = (current_dir-1) # Rotate CCW
                elif next_cell.get_side((current_dir+1)) in ["ccwdiverger", "forker", "triforker", "ccwforker"]: # If the next cell is a CCW diverger, forker, triforker, or CCW forker,
                    current_dir = (current_dir+1) # Rotate CW
                elif next_cell.get_side((current_dir)) in ["diverger", "triforker", "cwforker", "ccwforker"]: # If the next cell is a straight diverger, triforker, CW forker, or CCW forker,
                    pass # Do nothing

                else: # If the next cell is not a diverger, triforker, CW forker, or CCW forker,
                    break # Break the loop
            case _: # Push force
                #print(cell_map[current_x+cwdx, current_y+cwdy])
                if next_cell.get_side((current_dir+2)) == "cwdiverger": # If the next cell is a CW diverger,
                    current_dir = (current_dir+1) # Rotate CW
                    continue
                elif next_cell.get_side((current_dir+2)) == "ccwdiverger": # If the next cell is a CCW diverger,
                    current_dir = (current_dir-1) # Rotate CCW
                    continue
                elif next_cell.get_side((current_dir+2)) == "diverger": # If the next cell is a straight diverger,
                    continue # Do nothing
                if not displace:
                    if next_cell.get_side((current_dir+2)) == "cwdisplacer": # If the next cell is a CW diverger,
                        current_dir = (current_dir+1) # Rotate CW
                        continue
                    elif next_cell.get_side((current_dir+2)) == "ccwdisplacer": # If the next cell is a CCW diverger,
                        current_dir = (current_dir-1) # Rotate CCW
                        continue
                else:
                    if next_cell.get_side((current_dir+2)) == "cwdisplacer": # If the next cell is a CW diverger,
                        current_x += cwdx
                        current_y += cwdy # Rotate CW
                        stop_flag = True
                        continue
                    elif next_cell.get_side((current_dir+2)) == "ccwdisplacer": # If the next cell is a CCW diverger,
                        print("eeee")
                        current_x += ccwdx
                        current_y += ccwdy # Rotate CW
                        stop_flag = True
                        continue

                
            
                break # Break the loop



    return current_x, current_y, (current_dir - dir), (current_x-x, current_y-y), current_dir # Return the current x, current y, the difference between the current direction and the input direction, the delta x and y, and the current direction




def rot_center(image: pygame.Surface, rect: pygame.Rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle) # Rotate the image
    rot_rect = rot_image.get_rect(center=rect.center) # Get the rect of the rotated image
    return rot_image,rot_rect # Return the rotated image and rect

class Cell(pygame.sprite.Sprite):
    '''A class to represent a cell.'''
    def __init__(self, x: int, y: int, id: int | str, dir: int) -> None:
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
        self.rect.centerx = int(lerp(int(self.tile_x*TILE_SIZE-cam_x), int(self.old_x*TILE_SIZE-cam_x), update_timer/step_speed)+TILE_SIZE/2)
        self.rect.centery = int(lerp(int(self.tile_y*TILE_SIZE-cam_y), int(self.old_y*TILE_SIZE-cam_y), update_timer/step_speed)+TILE_SIZE/2)
        self.actual_dir = int(lerp(self.dir*-90, (self.dir-self.delta_dir)*-90, update_timer/step_speed))

    def draw(self):
        '''Draw the cell on the screen'''
        from main import window, TILE_SIZE, freeze_image, WINDOW_HEIGHT, WINDOW_WIDTH, protect_image, cell_map, delete_map
        if self not in cell_map.values() and self not in delete_map:
            return
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
    
    def on_force(self, dir, origin: Cell, suppress: bool = True, force_type = 0):
        from main import cell_map
        dir %= 4
        if self.id in [32, 33, 34, 35, 36, 37]:
            if self.get_side((dir+2)) == "trash":
                match (self.dir+dir)%4:
                    case 0:
                        self.eat_right = True
                    case 1:
                        self.eat_bottom = True
                    case 2:
                        self.eat_left = True
                    case 3: 
                        self.eat_top = True

        if self.get_side((dir+2)) == "fungal":
            origin.set_id(47)

        if self.get_side((dir+2)) in ["cwforker", "ccwforker", "triforker"]:
            new_cell_3: Cell = origin.copy()
            temp = increment_with_divergers(self.tile_x, self.tile_y, dir, 0)
            dx3, dy3 = temp[3]
            ddir = temp[2]
            new_cell_3.rot(ddir)
            new_cell_3.tile_x = self.tile_x+dx3
            new_cell_3.tile_y = self.tile_y+dy3
            if force_type == 0:
                self.push((dir), False, force=1)
            if (self.tile_x+dx3, self.tile_y+dy3) not in cell_map.keys():
                cell_map[self.tile_x+dx3, self.tile_y+dy3] = new_cell_3
                new_cell_3.suppressed = suppress
                foo = increment_with_divergers(temp[0], temp[1], temp[4])
                if (foo[0], foo[1]) in cell_map.keys():
                    cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_3)
            elif "forker" in cell_map[self.tile_x+dx3, self.tile_y+dy3].get_side((dir+2+ddir)):
                cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir), new_cell_3, suppress=suppress, force_type=force_type)
                del new_cell_3
            else:
                cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir), new_cell_3, suppress=suppress)

        if self.get_side((dir+2)) in ["forker", "cwforker", "triforker"]:

            # Fork CW
            new_cell_1: Cell = origin.copy()
            temp = increment_with_divergers(self.tile_x, self.tile_y, (dir-1), 0)
            dx1, dy1 = temp[3]
            ddir = temp[2]
            new_cell_1.tile_x = self.tile_x+dx1
            new_cell_1.tile_y = self.tile_y+dy1
            new_cell_1.rot(-1+ddir)
            if force_type == 0:
                self.push((dir-1), False, force=1)
            if (self.tile_x+dx1, self.tile_y+dy1) not in cell_map.keys():
                cell_map[self.tile_x+dx1, self.tile_y+dy1] = new_cell_1
                new_cell_1.suppressed = suppress
                foo = increment_with_divergers(temp[0], temp[1], temp[4])
                if (foo[0], foo[1]) in cell_map.keys():
                    cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_1)
            elif "forker" in cell_map[self.tile_x+dx1, self.tile_y+dy1].get_side((dir+1+ddir)):
                cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+3+ddir), new_cell_1, suppress=suppress, force_type=force_type)
                del new_cell_1
            else:
                cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+1+ddir), new_cell_1)

            if self.get_side((dir+2)) in ["forker", "ccwforker", "triforker"]:
                # Fork CCW
                new_cell_2: Cell = origin.copy()
                temp = increment_with_divergers(self.tile_x, self.tile_y, (dir+1), 0)
                dx2, dy2 = temp[3]
                ddir = temp[2]
                new_cell_2.tile_x = self.tile_x+dx2
                new_cell_2.tile_y = self.tile_y+dy2
                new_cell_2.rot(1+ddir)
                if force_type == 0:
                    self.push((dir+1), False, force=1)
                if (self.tile_x+dx2, self.tile_y+dy2) not in cell_map.keys():
                    cell_map[self.tile_x+dx2, self.tile_y+dy2] = new_cell_2
                    new_cell_2.suppressed = suppress
                    foo = increment_with_divergers(temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_2)
                elif "forker" in cell_map[self.tile_x+dx2, self.tile_y+dy2].get_side((dir+3+ddir)):
                    cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+1+ddir), new_cell_2, suppress=suppress, force_type=force_type)
                    del new_cell_2
                else:
                    cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+1+ddir), new_cell_2)
            

        if self.demolishes:
            for i in range(4):
                dx, dy = get_deltas(i)
                if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
                    temp_cell: Cell = cell_map[self.tile_x + dx, self.tile_y + dy]
                    if temp_cell.get_side_by_delta(dx, dy) not in ["wall", "trash"]:
                        if dir != (i+2)%4:
                            del cell_map[self.tile_x + dx, self.tile_y + dy] 

            

    def set_id(self, id: int | str) -> None:
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
        self.cwgrabs = False
        self.ccwgrabs = False
        self.swaps = False # Set the swaps flag to False
        self.gears = 0 # Set the gears flag to False
        self.demolishes = False
        self.nudges = False
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
            case 70:
                self.right = "cwrotator"
                self.left = "cwrotator"
                self.bottom = "ccwrotator"
                self.top = "ccwrotator"
                self.chirality = [0, 2]
            case 71:
                self.cwgrabs = True
                self.ccwgrabs = True
            case 72:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.pushes = True
            case 73:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.pulls = True
            case 74:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.pushes = True
                self.pulls = True
            case 75:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.drills = True
            case 76:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.drills = True
                self.pushes = True
            case 77:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.drills = True
                self.pulls = True
            case 78:
                self.cwgrabs = True
                self.ccwgrabs = True
                self.drills = True
                self.pulls = True
                self.pushes = True
            case 79:
                self.left = "ice"
                self.top = "ice"
                self.right = "ice"
                self.bottom = "ice"
            case 80:
                self.mirrors = [(0, 4), (1, 5), (2, 6), (3, 7)]
            case 81:
                self.top = "cwgrapulse"
                self.right = "cwgrapulse"
                self.bottom = "cwgrapulse"
                self.left = "cwgrapulse"
            case 82: 
                self.top = "ccwgrapulse"
                self.right = "ccwgrapulse"
                self.bottom = "ccwgrapulse"
                self.left = "ccwgrapulse"
            case 83: 
                self.top = "ccwdiverger"
                self.left = "diverger"
                self.bottom = "cwdiverger"
            case 84:
                self.left = "diverger"
                self.right = "diverger"
                self.top = "cwdiverger"
                self.bottom = "cwdiverger"
            case 85:
                self.left = "diverger"
                self.right = "diverger"
                self.bottom = "ccwdiverger"
                self.top = "ccwdiverger"
            case 86: 
                self.left = "displacer"
                self.right = "displacer"
                self.top = "ccwdisplacer"
                self.left = "displacer"
                self.bottom = "cwdisplacer"
            case 87:
                self.left = "displacer"
                self.right = "displacer"
                self.top = "cwdisplacer"
                self.bottom = "cwdisplacer"
            case 88:
                self.left = "displacer"
                self.right = "displacer"
                self.bottom = "ccwdisplacer"
                self.top = "ccwdisplacer"
            case 89:
                self.left = "flipper"
                self.right = "flipper"
            case 90:
                self.top = "flipper"
                self.right = "flipper"

            case 91:
                self.bottom = "cwdisplacer"
                self.right = "ccwdisplacer"
            case 114:
                self.nudges = True
            case 208:
                self.left = "diverger"
                self.chirality = [0]
            case _:
                pass

        if self.pushes or self.pulls or self.drills or self.cwgrabs or self.ccwgrabs or self.nudges:
            self.moves = True
        else:
            self.moves = False

    def mexican_standoff(self, cell: Cell):
        from main import cell_map
        if self.protected or cell.protected:
            return True
        dec_hp = min(self.hp, cell.hp)
        self.hp -= dec_hp
        cell.hp -= dec_hp
        self.check_hp()
        cell.check_hp()

        if self.hp <= 0:
            return False
        return True


    def push(self, dir: int, move: bool, hp: int = 1, force: int = 0, speed: int = 1, test: bool = False, active=True) -> bool | int:
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
            new_x, new_y, new_dir, _, b = increment_with_divergers(self.tile_x, self.tile_y, dir, displace=True)

            fx, fy, fdir, _, ppp = increment_with_divergers(self.tile_x, self.tile_y, dir)

            if move:
                if (new_x, new_y) in cell_map.keys():
                    cell = cell_map[new_x, new_y]
                    if "enemy" in cell.get_side(b+2):
                        if not self.mexican_standoff(cell):
                            return False

            print(self.tile_x, self.tile_y, fx, fy)
            if (fx, fy) in cell_map.keys():
                cell = cell_map[fx, fy]
                if cell.get_side((dir+2)) in ["wall", "undirectional", "forker", "triforker", "cwforker", "ccwforker"]:
                    print("flase")
                    return False
            con_dir = ppp
            x = fx
            y = fy
            cell = self
            
            if (cell.pushes, cell.dir) == (True, dir):
                bias += 1
            if (cell.pushes, cell.dir) == (True, (dir+2)%4) and not cell.frozen:
                bias -= 1
            if cell.get_side((dir+2)) == "repulse":
                bias -= 1
            if self.get_side((dir)) == "repulse":
                bias += 1
            if cell.get_side((dir+2)) == "weight":
                bias -= cell_map[x, y].weight
            if cell.get_side((dir+2)) == "antiweight":
                bias += cell_map[x, y].weight

            if bias <= 0:
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
                pass
            if move:
                del cell_map[(self.tile_x, self.tile_y)]
            if (fx, fy) in cell_map.keys():
                #if (new_x, new_y) != (self.tile_x, self.tile_y):
                try:
                    if not cell_map[fx, fy].push(dir+fdir, True, force=bias, speed=speed, test=test, active=False):
                        if test:
                            return False
                except RecursionError:
                    return False

            if move and not test:
                if not self.nudge(dir, not test):
                    return False
            if killer_cell is not None:
                return hp-killer_cell_hp
            else:
                return hp
        elif speed != float("inf"):
            for i in range(speed):
                self.push(dir, move, hp, force)
        else:
            if move:
                while self.push(dir, move, hp, force):
                    pass

        return True
    
        

    
    def pull(self, dir: int, move: bool, force: int = 0, test: bool = False) -> bool:
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
            incr = increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4, 2)
            back_cell_coord = incr[:2]
            row, deltas, ddirs, fail = get_row((self.tile_x, self.tile_y), (dir+2)%4, 2)
        else:
            incr = increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4, 2)
            back_cell_coord = incr[:2]
            starting_x, starting_y, dir_e, _, b = increment_with_divergers(back_cell_coord[0], back_cell_coord[1], (incr[4])%4, 2)
            print(incr)
            print(starting_x, starting_y)
            
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
            if i != 0:
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
            return False

        if fail:
            return False
        if back_cell_coord in cell_map.keys():
            cell_map[back_cell_coord].on_force((-affected[-1][4])%4, self, force_type=2)
        if row_interrupt_flag:
            
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
            if not self.push(dir, False):
                pass
                #return False
        if (new_x, new_y) in cell_map.keys() and not suicide_flag:
            return False
        if self.moves and self.dir == dir:
            self.suppressed = True
        if move:
            if not self.nudge(dir, not test):
                return False
        
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
                            cell_map[row[1][:2]].pull((row[1][4]+2)%4, True, force=bias)
            else:
                if (starting_x, starting_y) in cell_map.keys():
                    if cell_map[starting_x, starting_y].get_side((dir+2)%4) not in ["wall", "undirectional", "unpullable", "trash"]:
                        cell_map[starting_x, starting_y].pull((b+2)%4, True, force=bias)


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
        # Cells have already been pushed
        # Just create new cells if you have to
        if not self.push(dir, False):
            return
        if (self.tile_x + dx, self.tile_y + dy) not in cell_map.keys():
            generated_cell.hp = 1
            generated_cell.old_x = self.tile_x
            generated_cell.old_y = self.tile_y
            if generated_cell.hp == 1 and generated_cell.id == 24:
                generated_cell.set_id(13)
            if generated_cell.hp == 0:
                return True

            if cell.generation != 'normal':
                cell.generation -= 1

            print("eee")
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
        if twist:
            generated_cell.flip((dir*2+2)%4)
        if suppress:
            generated_cell.suppressed = True        
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
            
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
                cell_map[surrounding_cells[i]].rot(rot)
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
        if not self.pull((dir+2)%4, False):
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

        if (self.pushes) and self.dir == dir:
            self.push(dir, True)
            #self.suppressed = True

    def do_repulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "repulse":
            self.push(dir, False, force=1)

    def do_super_repulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "superrepulse":
            self.push(dir, False, 1, float("inf"), float("inf"))

    def do_impulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "impulse":
            self.pull(dir, False)

    def do_grapulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "cwgrapulse":
            self.ccw_grab(dir, False)
        elif self.get_side(dir) == "ccwgrapulse":
            self.cw_grab(dir, False)

    def do_pull(self, dir):
        if self.frozen or self.suppressed:
            return
        if self.pulls and self.dir == dir:


            if self.cwgrabs or self.ccwgrabs:
                if self.cwgrabs:
                    if self.ccwgrabs:
                        self.grab(self.dir, False)
                    else:
                        self.cw_grab(self.dir, False)
                elif self.ccwgrabs:
                    self.ccw_grab(self.dir, False)
            if self.pushes:
                self.push(self.dir, True)
            else:
                self.nudge(self.dir, True)

            self.pull(self.dir, False)
            self.suppressed = True

    def drill(self, dir, test: bool = False):
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
                return True
        if not test:
            swap_cells((self.tile_x, self.tile_y), (self.tile_x + dx, self.tile_y + dy))
        return True
    def do_drill(self, dir):
        if self.frozen or self.suppressed:
            return
        if not self.drills:
            return
        if self.dir != dir:
            return

        print()

        if self.pushes:
            if not self.drill(self.dir, test=True):
                self.suppressed = True
                return 
        else:
            if not self.nudge(self.dir, False):
                self.suppressed = True
                return 

        if self.cwgrabs or self.ccwgrabs:
            if self.cwgrabs:
                if self.ccwgrabs:
                    self.grab(self.dir, False)
                else:
                    self.cw_grab(self.dir, False)
            elif self.ccwgrabs:
                self.ccw_grab(self.dir, False)

        if self.pushes:
            if not self.push(self.dir, True):
                self.drill(self.dir)
        else:
            self.drill(self.dir)
                
        if self.pulls:
            self.pull(self.dir, False)

        self.suppressed = True
    
    def do_gen(self, dir: int):
        if self.frozen:
            return

        if self.get_side(dir) == "generator":
            self.test_gen(dir, 0)
        if self.get_side(dir) == "cwgenerator":
            self.test_gen(dir, 1)
        if self.get_side(dir) == "ccwgenerator":
             
            self.test_gen(dir, -1)

    def do_super_gen(self, dir: int):
        if self.frozen:
            return

        if self.get_side(dir) == "supergenerator":
             
            self.test_supergen(dir, 0)
        if self.get_side(dir) == "cwsupergenerator":
             
            self.test_supergen(dir, 1)
        if self.get_side(dir) == "ccwsupergenerator":
             
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
        for i in range(4):
            if self.get_side(i) == "flipper":
                if self.dir in [0, 2]:
                        self.test_flip(i, 0)
                if self.dir in [1, 3]:
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
        
    def cw_grab(self, dir: int, move: bool, hp: int = 1, force: int = 1, speed: int = 1) -> bool | int:
        if move:
            if not self.nudge(dir, False):
                return
        from main import cell_map, delete_map
        suicide_flag = False
        trash_flag = False
        fail = False
        incr = increment_with_divergers(self.tile_x, self.tile_y, (dir+1)%4)
        new_x, new_y, new_dir, a, b = increment_with_divergers(self.tile_x, self.tile_y, dir)
        bias = force
        if (new_x, new_y) in cell_map.keys():
            cell = cell_map[new_x, new_y]
            if "trash" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                suicide_flag = True
                killer_cell = (new_x, new_y, new_dir, a, b)
            if "forker" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                suicide_flag = True
                killer_cell = (new_x, new_y, new_dir, a, b)
            if "enemy" in cell.get_side(b+2):
                    if not self.mexican_standoff(cell):
                        return
        if incr[:2] in cell_map.keys():
            if cell_map[incr[:2]].get_side((dir+3+incr[2])%4) == "wall":
                fail = True
            if cell_map[incr[:2]].get_side((dir+3+incr[2])%4) == "trash":
                trash_flag = True

            if "forker" in cell_map[incr[:2]].get_side((dir+3)%4):
                trash_flag = True
                

        if incr[:2] in cell_map.keys():
            cell = cell_map[incr[:2]]
            if cell.cwgrabs and (cell.dir+1)%4 == incr[4]:
                bias+=1
            if cell.ccwgrabs and (cell.dir-1)%4 == incr[4]:
                bias -= 1
            if cell.get_side((incr[4]+2)%4) == "cwgrapulse":
                bias+=1
            if cell.get_side((incr[4]+2)%4) == "ccwgrapulse":
                bias-=1
            if cell.get_side((incr[4])%4) == "cwgrapulse":
                bias-=1
            if cell.get_side((incr[4])%4) == "ccwgrapulse":
                bias+=1
            cell.on_force(dir, self, force_type=1)

        if bias <= 0:
            return False

        if fail:
            return False


        if move:
            del cell_map[(self.tile_x, self.tile_y)]
        if incr[:2] in cell_map.keys():
            #if (new_x, new_y) != (self.tile_x, self.tile_y):
            if not trash_flag:
                try:
                    if not cell_map[incr[:2]].cw_grab((incr[4]-1)%4, True, force=bias, speed=speed):
                        cell_map[(self.tile_x, self.tile_y)] = self
                        pass
                        #return False
                except RecursionError:
                    return False

        
        if move:
            self.suppressed = True
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
                cell_map[killer_cell[:2]].on_force(dir, self, force_type=1)
                if (self.tile_x, self.tile_y) in cell_map.keys():
                    del cell_map[(self.tile_x, self.tile_y)]
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                self.rot(new_dir)
                if suicide_flag:
                    if "forker" not in cell_map[killer_cell[:2]].get_side((dir+new_dir+2)%4):  
                        delete_map.append(self)

            if self.pushes or self.pulls or self.cwgrabs or self.ccwgrabs:
                if self.dir == (incr[4])%4:
                    self.suppressed = True

            

        return True
    
    def ccw_grab(self, dir: int, move: bool, hp: int = 1, force: int = 1, speed: int = 1) -> bool | int:
        from main import cell_map, delete_map 
        if move:
            if not self.nudge(dir, False):
                return
        suicide_flag = False
        trash_flag = False
        fail = False
        incr = increment_with_divergers(self.tile_x, self.tile_y, (dir+3)%4)
        new_x, new_y, new_dir, a, b = increment_with_divergers(self.tile_x, self.tile_y, dir)
        bias = force
        if move:
            if (new_x, new_y) in cell_map.keys():
                cell = cell_map[new_x, new_y]
                if "trash" in cell.get_side((dir+2+new_dir)%4):
                    suicide_flag = True
                    killer_cell = (new_x, new_y, new_dir, a, b)
                if "forker" in cell.get_side((dir+2+new_dir)%4):
                    suicide_flag = True


                if "enemy" in cell.get_side(b+2):
                    if not self.mexican_standoff(cell):
                        return
            
        if incr[:2] in cell_map.keys():
            if cell_map[incr[:2]].get_side((dir+1+incr[2])%4) == "wall":
                fail = True
            if cell_map[incr[:2]].get_side((dir+1+incr[2])%4) == "trash":
                trash_flag = True

            if "forker" in cell_map[incr[:2]].get_side((dir+1)%4):
                trash_flag = True
                

        if incr[:2] in cell_map.keys():
            cell = cell_map[incr[:2]]
            if cell.ccwgrabs and (cell.dir-1)%4 == incr[4]:
                bias+=1
            if cell.cwgrabs and (cell.dir+1)%4 == incr[4]:
                bias -= 1
            if cell.get_side((incr[4]+2)%4) == "cwgrapulse":
                bias+=1
            if cell.get_side((incr[4]+2)%4) == "ccwgrapulse":
                bias-=1
            if cell.get_side((incr[4])%4) == "cwgrapulse":
                bias-=1
            if cell.get_side((incr[4])%4) == "ccwgrapulse":
                bias+=1
            cell.on_force(dir, self, force_type=1)

        if bias <= 0:
            return False

        if fail:
            return False


        if move:
            del cell_map[(self.tile_x, self.tile_y)]
        if incr[:2] in cell_map.keys():
            #if (new_x, new_y) != (self.tile_x, self.tile_y):
            if not trash_flag:
                try:
                    if not cell_map[incr[:2]].ccw_grab((incr[4]+1)%4, True, force=bias, speed=speed):
                        cell_map[(self.tile_x, self.tile_y)] = self
                        pass
                        #return False
                except RecursionError:
                    return False

        if move:
            self.suppressed = True
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
                cell_map[killer_cell[:2]].on_force(dir, self, force_type=3)
                if (self.tile_x, self.tile_y) in cell_map.keys():
                    del cell_map[(self.tile_x, self.tile_y)]
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                self.rot(new_dir)
                if suicide_flag:
                    if "forker" not in cell_map[killer_cell[:2]].get_side((dir+new_dir+2)%4):  
                        delete_map.append(self)

            if self.pushes or self.pulls or self.cwgrabs or self.ccwgrabs:
                if self.dir == (incr[4])%4:
                    self.suppressed = True

            

        return True

    


    def grab(self, dir: int, move: bool, force: int = 0, test: bool = False) -> bool:
        from main import cell_map
        incr_cw = increment_with_divergers(self.tile_x, self.tile_y, (dir+1)%4, 1)
        if incr_cw[:2] in cell_map.keys():
            
            if cell_map[incr_cw[:2]].get_side((dir+1+incr_cw[2])) == "wall":
                return False


        incr_ccw = increment_with_divergers(self.tile_x, self.tile_y, (dir+3)%4, 3)
        if incr_ccw[:2] in cell_map.keys():
            if cell_map[incr_ccw[:2]].get_side((dir+3+incr_ccw[2])) == "wall":
                return False
        
        if move:
            if not self.nudge(dir, not test, force):
                return False
        if incr_cw[:2] in cell_map.keys():
            cell_map[incr_cw[:2]].cw_grab(dir, True)
        if incr_ccw[:2] in cell_map.keys():
            cell_map[incr_ccw[:2]].ccw_grab(dir, True)

    def nudge(self, dir: int, move: bool, force: int = 0, hp: int = 1, active=True):
        from main import cell_map, delete_map
        suicide_flag = False
        trash_flag = False
        fail = False
        #incr = increment_with_divergers(self.tile_x, self.tile_y, (dir+3)%4)
        new_x, new_y, new_dir, a, b = increment_with_divergers(self.tile_x, self.tile_y, dir, displace=True)
        bias = force
        print("n")
        if move:
            if (new_x, new_y) in cell_map.keys():
                if "trash" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                    suicide_flag = True
                    killer_cell = (new_x, new_y, new_dir, a, b)
                if "forker" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                    suicide_flag = True
                    killer_cell = (new_x, new_y, new_dir, a, b)
                

        if (new_x, new_y) in cell_map.keys():
                if "enemy" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                    cell = cell_map[new_x, new_y]
                    if not self.mexican_standoff(cell):
                        return

                    if self.hp == 0:
                        return False

        if not suicide_flag:               
            if (new_x, new_y) in cell_map.keys():
                cell_map[(self.tile_x, self.tile_y)] = self
                print("fial")
                return False


        if move:
            if (self.tile_x, self.tile_y) in cell_map.keys():
                del cell_map[(self.tile_x, self.tile_y)]
            self.suppressed = True
            if suicide_flag:
                
            
                cell_map[killer_cell[:2]].on_force(dir, self)
                if (self.tile_x, self.tile_y) in cell_map.keys():
                    del cell_map[(self.tile_x, self.tile_y)]
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                self.rot(new_dir)
                if suicide_flag:
                    if "trash" in cell_map[killer_cell[:2]].get_side((dir+new_dir+2)%4):  
                        delete_map.append(self)
            else:
                cell_map[new_x, new_y] = self
                self.tile_x = new_x
                self.tile_y = new_y
                self.rot(new_dir)



            

        return True


    def do_grab(self, dir):
        if self.frozen or self.suppressed:
            return False
        if self.dir == dir:
            if self.cwgrabs or self.ccwgrabs:

                if self.cwgrabs:
                    if self.ccwgrabs:

                        self.grab(dir, False)
                    else:
                        self.cw_grab(dir, False)
                elif self.ccwgrabs:
                    self.ccw_grab(dir, False)

                if self.pushes:
                    self.push(dir, True)
                else:
                    self.nudge(dir, True)


                self.suppressed = True

    def do_nudge(self, dir):
        if self.frozen or self.suppressed:
            return False
        if self.dir == dir:
            if self.nudges:
                self.nudge(dir, True)

                self.suppressed = True

    def check_hp(self):
        from main import cell_map
        if self.hp == 1 and self.id == 24:
            self.set_id(13)
        elif self.hp == 2 and self.id == 13:
            self.set_id(24)
        elif self.hp == 0:
            trash_sound.play()
            del cell_map[self.tile_x, self.tile_y]
        



























































