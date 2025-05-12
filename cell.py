import math
import random

import pygame
from side import Side

from typing import Self

pygame.init()


cell_names: dict[str | int, str] = {
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
    80: "octomirror",
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
    99: "divider",
    100: "tridivider",
    101: "cwdivider",
    102: "ccwdivider",
    103: "conditional",
    104: "antiweight",
    105: "transmitter",
    106: "shifter",
    107: "crossshifter",
    108: "minigear_cw",
    109: "minigear_ccw",
    110: "cwcloner",
    111: "ccwcloner",
    112: "locker",
    113: "redirectgenerator",
    114: "nudger",
    115: "slicer",
    116: "marker",
    117: "marker_x",
    118: "marker_warn",
    119: "marker_check",
    120: "marker_question",
    121: "marker_arrow",
    122: "marker_darrow",
    123: "crimson",
    124: "warped",
    125: "corruption",
    126: "hallow",
    127: "cancer",
    128: "bacteria",
    129: "bioweapon",
    130: "prion",
    131: "greygoo",
    132: "virus",
    133: "tumor",
    134: "infection",
    135: "pathogen",
    136: "pushclamper",
    137: "pullclamper",
    138: "grabclamper",
    139: "swapclamper",
    140: "toughtwodirectional",
    141: "megademolisher",
    142: "resistance",
    143: "tentative",
    144: "restrictor",
    145: "megashield",
    146: "timewarper",
    147: "timegenerator",
    148: "crosstimewarper",
    149: "life",
    150: "spinnercw",
    151: "spinnerccw",
    152: "spinner180",
    153: "key",
    154: "door",
    155: "crossintaker",
    156: "magnet",
    157: "toughonedirectional",
    158: "toughthreedirectional",
    159: "toughpush",
    208: "diodediverger",

    #231: "silicon", # bro i am not coding this
    1201: "dextroanlevogenerator",
    "bob": "bob",
    "nonexistant": "nonexistant",
    "bgvoid": "bgvoid"
}

cell_cats_new = [
    # Categories of cells in the UI
    [], # Tools
    [[1, 41], # Walls
     [4, 5, 6, 7, 8, 69, 140, 157, 158, 159], # Pushables
     [52, 53, 54], # Oppositions
     [22, 42, 103, 104, 142, 143, 144], # Weight 
     [116, 117, 118, 119, 120, 121, 122]], #Decorative] # Basic

    [[2, 28, 59, 60, 72, 74, 76, 78], # Pushers
     [14, 28, 60, 61, 73, 74, 77, 78], # Pullers
     [71, 72, 73, 74, 75, 76, 77, 78], # Grabbers
     [58, 59, 60, 61, 75, 76, 77, 78], # Drillers
     [114, "bob", 115] # Other
    ], # Movers

    [[3, 23, 26, 27, 40, 110, 111, 113, 147, 1201], # Generators
     [55], # Super Generators
     [45, 46], # Replicators
     [32, 33, 34, 35, 36, 37] # Gates
    ], # Generators

    [[9, 10, 11, 66, 67, 68, 57, 70, 150, 151, 152], # Rotators
     [18, 19], # Gears
     [17, 62, 63, 64, 65], # Redirectors
     [30, 89, 90] # Flippers
    ], # Rotators

    [[21, 50], [29], [81, 82], [15, 56, 80], [18, 19, 108, 109], [44, 155], [106, 107], [156]], # Forcers
    [[16, 31, 38, 39, 83, 84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 96, 208], [48, 49, 97, 98, 99, 100, 101, 102], [79], ], # Divergers
    [[12], [51, 141], [13, 24], [44]], # Destroyers
    [[146, 148]], # Transformers
    [[20], [47, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 149], [25, 43, 105, 112, 136, 137, 138, 139, 145], [153, 154], ["placeable", "bgvoid"], ] # Misc
]

flip_guide = [
    # Guide for flipping cells
    [2, 0, 2, 0],
    [1, -1, 1, -1],
    [0, 2, 0, 2],
    [-1, 1, -1, 1]
]



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    import os, sys   
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

cell_images_raw = [] # The raw images of the cells

for cell_id in cell_names.keys(): # Iterate through the cell names
    cell_images_raw.append((cell_id, pygame.image.load(resource_path(f"textures/{cell_names[cell_id]}.png")))) # Load the image of the cell and add it to the list

cell_images = dict(cell_images_raw); # Convert the list to a dictionary

move_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/move.ogg")) # Load the move sound
rot_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/rotate.ogg")) # Load the rotate sound
trash_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/destroy.ogg")) # Load the destroy sound

def lerp(a, b, factor):
    '''Linear interpolation function'''
    return a + (b-a)*factor

def get_row(game, coord: tuple[int, int], dir: int, force_type: int = 0) -> tuple[list[tuple[int, int, int, tuple[int, int], int]], list[tuple[int, int]], list[int], bool]:
    '''Get a row of cells in a direction'''
    cell_map = game.cell_map
    test: tuple[int, int, int, tuple[int, int], int] = (coord[0], coord[1], int(0), (0, 0), dir) # Initialize the test case
    temp: Cell # Initialize the temporary cell
    incr: tuple[int, int, int, tuple[int, int], int] # Initialize the incremented case
    result: list[tuple[int, int, int, tuple[int, int], int]] = [] # Initialize the result
    deltas: list[tuple[int, int]] = [] # Initialize the deltas
    delt_dirs: list[int] = [] # Initialize the delta directions
    fail = False # Initialize the fail flag
    current_dir: int = dir # Initialize the current direction
    while True:
        deltas.append(increment_with_divergers(game, test[0], test[1], current_dir, force_type)[3]) # Append the delta
        delt_dirs.append(increment_with_divergers(game, test[0], test[1], current_dir, force_type)[2]) # Append the delta direction
        if test[:2] not in cell_map.keys(): # If the cell is not in the cell map, break
            break
        temp = cell_map[test[:2]] # Get the cell

        incr = increment_with_divergers(game, test[0], test[1], test[4], force_type) # Increment the cell
        
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
                #fail = True # Set the fail flag
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

def swap_cells(game, a: tuple[int, int], b: tuple[int, int]):
    '''Swaps two cells in the cell map.'''
    cell_map = game.cell_map
    a_flag, b_flag = False, False # Initialize the flags
    first: Cell = Cell(game, 0, 0, 0, 0) # Initialize the first cell
    second: Cell = Cell(game, 0, 0, 0, 0) # Initialize the second cell
    if a in cell_map.keys(): # If a is in the cell map,
        first = cell_map[a] # Set the first cell to the cell at a
        first.tile_x, first.tile_y = b[0], b[1] # Set the tile x and y of the first cell to b
        a_flag = True # Set the a flag to True
    if b in cell_map.keys(): # If b is in the cell map,
        second = cell_map[b] # Set the second cell to the cell at b
        second.tile_x, second.tile_y = a[0], a[1] # Set the tile x and y of the second cell to a
        b_flag = True # Set the b flag to True
    if not a_flag and not b_flag: # If neither a nor b are in the cell map,
        return
    
    if a_flag: # If a is in the cell map,
         cell_map[b] = first # Set the cell at b to the first cell
    else: # If a is not in the cell map,
        del cell_map[b] # Delete the cell at b
    if b_flag: # If b is in the cell map,
        cell_map[a] = second # Set the cell at a to the second cell
    else: # If b is not in the cell map,
        del cell_map[a] # Delete the cell at a
   
def increment_with_divergers(game, x, y, dir: int, force_type = 0, displace=False) -> tuple[int, int, int, tuple[int, int], int]:
    """Determine the next cell in a direction, accounting for divergers."""
    cell_map = game.cell_map
    dir %= 4
    #from main import cell_map # Import the cell map
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
        next_cell: Cell = Cell(game, current_x, current_y, 0, dir) # Set the next cell to a new cell at the current x and y with the id 0 and direction dir
    while True: # Loop forever
        dx, dy = get_deltas(current_dir) # Get the delta values of the current direction
        cwdx, cwdy = get_deltas(current_dir+1)
        ccwdx, ccwdy = get_deltas(current_dir - 1)
        if not stop_flag:
            current_x += dx # Increment the current x by dx
            current_y += dy # Increment the current y by dy
        if (current_x, current_y) == (x, y):
            break

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
        
        
        
        ##print(.+?)cell_map[current_x+cwdx, current_y+cwdy])
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
                ##print(.+?)"eeee")
                current_x += ccwdx
                current_y += ccwdy # Rotate CW
                stop_flag = True
                continue
            elif next_cell.get_side((current_dir+2)) == "displacer": # If the next cell is a CCW diverger,
                ##print(.+?)"eeee")
                stop_flag = True
                continue


        
    
        break # Break the loop



    return current_x, current_y, (current_dir - dir), (current_x-x, current_y-y), current_dir # Return the current x, current y, the difference between the current direction and the input direction, the delta x and y, and the current direction




def rot_center(image: pygame.Surface, rect: pygame.Rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image.convert_alpha(), angle).convert_alpha() # Rotate the image
    rot_rect = rot_image.get_rect(center=rect.center) # Get the rect of the rotated image
    return rot_image,rot_rect # Return the rotated image and rect

nonexistant = pygame.image.load(resource_path("textures/nonexistant.png")) # Load the nonexistant image

class Cell():
    '''A class to represent a cell. Also contains most cell-related functions.'''
    def __init__(self, game, x: int, y: int, id: int | str, dir: int, layer=None) -> None:
        '''Initialize the cell.'''
        # Initialize the sprite
        #super().__init__()

        self.game = game

        # Cell variables
        self.tile_x: int = x # Set the tile x to x
        self.tile_y: int = y # Set the tile y to y
        self.old_x: int = x # Set the old x to x
        self.old_y: int = y # Set the old y to y
        self.old_dir: int = dir # Set the old direction to dir
        self.id: int | str = id


        self.name = cell_names.get(self.id, "nonexistant") # Set the name to the name of the cell
        self.dir: int = dir # Set the direction to dir
        self.actual_dir: int = dir*-90 # Set the actual direction to dir times -90
        self.img_cache = {}
        if layer is None:
            self.layer = self.game.cell_map
        else:
            self.layer = layer

        self.chirality = [-1, 0, 1, 2] # Set the chirality to -1, 0, 1, 2

        self.delta_dir = 0 # Set the delta direction to 0

        self.die_flag = False # Set the die flag to False

        # Image variables
        self.image: pygame.Surface = cell_images.get(self.id, nonexistant) # Set the image to the image of the cell
        self.rect: pygame.Rect = self.image.get_rect() # Set the rect to the rect of the image

        # Effect variables
        self.frozen: bool = False # Set the frozen flag to False
        self.protected: bool = False # Set the protected flag to False
        self.locked: bool = False
        self.pushclamped: bool = False
        self.pullclamped: bool = False
        self.grabclamped: bool = False
        self.swapclamped: bool = False

        # Sides
        self.left: Side = Side(["pushable"]) # Set the left side to pushable
        self.right: Side = Side(["pushable"]) # Set the right side to pushable
        self.top: Side = Side(["pushable"]) # Set the top side to pushable
        self.bottom: Side = Side(["pushable"]) # Set the bottom side to pushable

        self.br = "pushable"
        self.bl = "pushable"
        self.tl = "pushable"
        self.tr = "pushable"

        # Other cell variables
        self.hp: int = 1 # Set the hp to 1
        self.generation: str | int = "normal" # Set the generation to normal
        self.weight = 1 # Set the weight to 1
        self.rotatable = True

        # Push/pull variables
        self.pushes = False # Set the pushes flag to False
        self.pulls = False # Set the pulls flag to False
        self.drills = False
        self.cwgrabs = False
        self.ccwgrabs = False
        self.slices = False
        #self.swaps = [] # Set the swaps flag to False
        self.gears = 0 # Set the gears flag to False
        self.minigears = 0
        self.skewgears = 0
        #self.demolishes = ""
        self.nudges = False
        self.mirrors = []
        self.bobs = False
        self.lifes = False
        self.infects = ("", "", 0)

        # Flags
        self.suppressed = False # Set the suppressed flag to False
        self.eat_left = False # Set the eat left flag to False
        self.eat_right = False # Set the eat right flag to False
        self.eat_top = False # Set the eat top flag to False
        self.eat_bottom = False # Set the eat bottom flag to False

        self.tags = {"enemy": False, "ally": False, "neutral": False, "fiend": False}

        self.extra_properties = {}

        

        

        # Set cell-specific variables
        self.set_id(self.id) # Set the id of the cell

    def __repr__(self) -> str:
        '''Represent the cell as a string.'''
        return f"{self.name.title()} at {self.tile_x}, {self.tile_y}, id {self.id}, direction {self.dir}"
    
    def copy(self) -> Self:
        '''Copy constructor'''
        return Cell(self.game, self.tile_x, self.tile_y, self.id, self.dir, layer=self.layer) # type: ignore

    def update(self):
        '''Update the cell, once per frame'''
        #from main import cam_x, cam_y, TILE_SIZE, cell_map, update_timer, step_speed
        factor = self.game.update_timer/self.game.step_speed if self.game.step_speed != 0 else 1
        self.rect.centerx = int(lerp(int(self.tile_x*self.game.tile_size-self.game.cam_x), int(self.old_x*self.game.tile_size-self.game.cam_x), factor)+self.game.tile_size/2)
        self.rect.centery = int(lerp(int(self.tile_y*self.game.tile_size-self.game.cam_y), int(self.old_y*self.game.tile_size-self.game.cam_y), factor)+self.game.tile_size/2)
        self.actual_dir = int(lerp(self.dir*-90, (self.dir-self.delta_dir)*-90, factor))

    def draw(self):
        '''Draw the cell on the screen'''
        #from main import window, TILE_SIZE, freeze_image, WINDOW_HEIGHT, WINDOW_WIDTH, protect_image, cell_map, delete_map, below, above
        if ((self not in self.game.cell_map.values() and self not in self.game.below.values() and self not in self.game.above.values()) and self not in self.game.delete_map) or self.id == "bgvoid":
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        img = self.loadscale(self.game.tile_size)
        rect = img.get_rect()
        true_img, true_rect = rot_center(img, self.rect, self.actual_dir)
        if true_rect.y+self.game.tile_size < 0:
            return
        if true_rect.y > self.game.window_height:
            return
        if true_rect.x+self.game.tile_size < 0:
            return 
        if true_rect.x > self.game.window_width:
            return
        
        if self.game.selected_cell is self:
            true_rect.center = (mouse_x, mouse_y)
        # old_rect = self.rect.copy()
        

        if (self.tile_x, self.tile_y) in self.game.below.keys() and self.game.tick_number == 0 and self.game.paused and self.game.selected_cell is not self:
            if self.game.below[self.tile_x, self.tile_y] is not self and self.game.below[self.tile_x, self.tile_y].id == "placeable":

                true_img.blit(pygame.transform.scale(self.game.placeable_overlay, (self.game.tile_size, self.game.tile_size)), (0, 0))
        if self.frozen:
            true_img.blit(pygame.transform.scale(self.game.freeze_image, (self.game.tile_size, self.game.tile_size)), (0, 0))

        if self.protected:
            true_img.blit(pygame.transform.scale(self.game.protect_image, (self.game.tile_size, self.game.tile_size)), (0, 0))
        if self.locked:
            true_img.blit(pygame.transform.scale(self.game.lock_image, (self.game.tile_size, self.game.tile_size)), (0, 0))

        if self.pushclamped:
            true_img.blit(pygame.transform.scale(self.game.pushclamp_image, (self.game.tile_size, self.game.tile_size)), (0, 0))
        if self.pullclamped:
            true_img.blit(pygame.transform.scale(self.game.pullclamp_image, (self.game.tile_size, self.game.tile_size)), (0, 0))
        if self.grabclamped:
            true_img.blit(pygame.transform.scale(self.game.grabclamp_image, (self.game.tile_size, self.game.tile_size)), (0, 0))
        if self.swapclamped:
            true_img.blit(pygame.transform.scale(self.game.swapclamp_image, (self.game.tile_size, self.game.tile_size)), (0, 0))

        self.game.window.blit(true_img, true_rect)

    def loadscale(self, size):
        '''Load the image of the cell, from the cache if possible'''
        if size in self.img_cache.keys():
            return self.img_cache[size]
        img: pygame.Surface = pygame.transform.scale(self.image, (size, size))
        self.img_cache[size] = img
        return img

    
    def on_force(self, dir, origin: Self, suppress: bool = True, force_type = "push"):
        '''Things cells do when a force is applied.'''
        cell_map = self.game.cell_map
        dir %= 4
        print("onforce"+force_type)
        if self.get_side((dir+2)) == "cwspinner" and force_type == "nudge":
            print("FF")
            origin.rot(1)
        if self.get_side((dir+2)) == "ccwspinner" and force_type == "nudge":
            print("FF")
            origin.rot(-1)
        if self.get_side((dir+2)) == "180spinner" and force_type == "nudge":
            print("FF")
            origin.rot(2)
        
        if self.extra_properties.get("door"):
            if origin.extra_properties.get("key"):
                del cell_map[self.tile_x, self.tile_y]
                del cell_map[origin.tile_x, origin.tile_y]

            

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
            origin.set_id(self.id)

        if self.get_side((dir+2)) in ["cwforker", "ccwforker", "triforker"]:
            new_cell_3: Cell = origin.copy()
            temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir, 0)
            dx3, dy3 = temp[3]
            ddir = temp[2]
            new_cell_3.rot(ddir)
            new_cell_3.tile_x = self.tile_x+dx3
            new_cell_3.tile_y = self.tile_y+dy3
            if force_type == "push":
                self.push((dir), False, force=1)
            if (self.tile_x+dx3, self.tile_y+dy3) not in cell_map.keys():
                if origin.id:
                    cell_map[self.tile_x+dx3, self.tile_y+dy3] = new_cell_3
                new_cell_3.suppressed = suppress
                foo = increment_with_divergers(self.game, temp[0], temp[1], temp[4])
                if (foo[0], foo[1]) in cell_map.keys():
                    cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_3)
            elif "forker" in cell_map[self.tile_x+dx3, self.tile_y+dy3].get_side((dir+2+ddir)):
                cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir), new_cell_3, suppress=suppress, force_type=force_type)
                del new_cell_3
            else:
                cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir), new_cell_3, suppress=suppress)

        if self.get_side((dir+2)) in ["forker", "cwforker", "triforker"]:
            if force_type == "push" and dir == self.dir:
                self.push((dir+1), False, force=1)
            elif force_type == "nudge" and dir == self.dir:
                # Fork CW
                new_cell_1: Cell = origin.copy()
                temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+1), 0)
                dx1, dy1 = temp[3]
                ddir = temp[2]
                new_cell_1.tile_x = self.tile_x+dx1
                new_cell_1.tile_y = self.tile_y+dy1
                new_cell_1.rot(1+ddir)

                if (self.tile_x+dx1, self.tile_y+dy1) not in cell_map.keys():
                    if origin.id:
                        cell_map[self.tile_x+dx1, self.tile_y+dy1] = new_cell_1
                    new_cell_1.suppressed = suppress
                    foo = increment_with_divergers(self.game, temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_1)
                elif "forker" in cell_map[self.tile_x+dx1, self.tile_y+dy1].get_side((dir+3+ddir)):
                    cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+1+ddir)%4, new_cell_1, suppress=suppress, force_type=force_type)
                    del new_cell_1
                else:
                    cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+1+ddir), new_cell_1)

        if self.get_side((dir+2)) in ["forker", "ccwforker", "triforker"]:
            # Fork CCW
            if force_type == "push" and dir == self.dir:
                self.push((dir-1)%4, False, force=1)
            elif force_type == "nudge" and dir == self.dir:
                new_cell_2: Cell = origin.copy()
                temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-1)%4, 0)
                dx2, dy2 = temp[3]
                ddir = temp[2]
                new_cell_2.tile_x = self.tile_x+dx2
                new_cell_2.tile_y = self.tile_y+dy2
                new_cell_2.rot(-1+ddir)

                if (self.tile_x+dx2, self.tile_y+dy2) not in cell_map.keys():
                    if origin.id:
                        cell_map[self.tile_x+dx2, self.tile_y+dy2] = new_cell_2
                    new_cell_2.suppressed = suppress
                    foo = increment_with_divergers(self.game, temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_2)
                elif "forker" in cell_map[self.tile_x+dx2, self.tile_y+dy2].get_side((dir+1+ddir)%4):
                    cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+3+ddir)%4, new_cell_2, suppress=suppress, force_type=force_type)
                    del new_cell_2
                else:
                    cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+3+ddir)%4, new_cell_2)

        

        if self.get_side((dir+2)) in ["cwdivider", "ccwdivider", "tridivider"]:
            if force_type == "push" and self.dir == dir:
                self.push((dir), False, force=1)
            elif force_type == "nudge" and self.dir == dir:
                new_cell_3: Cell = origin.copy()
                temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir, 0)
                dx3, dy3 = temp[3]
                ddir = temp[2]
                new_cell_3.rot(ddir)
                new_cell_3.tile_x = self.tile_x+dx3
                new_cell_3.tile_y = self.tile_y+dy3
                    
                if (self.tile_x+dx3, self.tile_y+dy3) not in cell_map.keys():
                    cell_map[self.tile_x+dx3, self.tile_y+dy3] = new_cell_3
                    new_cell_3.suppressed = suppress
                    foo = increment_with_divergers(self.game, temp[0], temp[1], temp[4])
                    if (foo[0], foo[1]) in cell_map.keys():
                        cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_3)
                elif "divider" in cell_map[self.tile_x+dx3, self.tile_y+dy3].get_side((dir+2+ddir)):
                    cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir), new_cell_3, suppress=suppress, force_type=force_type)
                    del new_cell_3
                else:
                    cell_map[self.tile_x+dx3, self.tile_y+dy3].on_force((dir+ddir), new_cell_3, suppress=suppress)

        if self.get_side((dir+2)) in ["divider", "cwdivider", "tridivider"]:

            # Fork CW
            new_cell_1: Cell = origin.copy()
            temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+1), 0)
            dx1, dy1 = temp[3]
            ddir = temp[2]
            new_cell_1.tile_x = self.tile_x+dx1
            new_cell_1.tile_y = self.tile_y+dy1
            #new_cell_1.rot(1+ddir)
            if force_type == 0:
                self.push((dir+1), False, force=1)
            if (self.tile_x+dx1, self.tile_y+dy1) not in cell_map.keys():
                cell_map[self.tile_x+dx1, self.tile_y+dy1] = new_cell_1
                new_cell_1.suppressed = suppress
                foo = increment_with_divergers(self.game, temp[0], temp[1], temp[4])
                if (foo[0], foo[1]) in cell_map.keys():
                    cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_1)
            elif "divider" in cell_map[self.tile_x+dx1, self.tile_y+dy1].get_side((dir+3+ddir)):
                cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+1+ddir)%4, new_cell_1, suppress=suppress, force_type=force_type)
                del new_cell_1
            else:
                cell_map[self.tile_x+dx1, self.tile_y+dy1].on_force((dir+1+ddir), new_cell_1)

        if self.get_side((dir+2)) in ["divider", "ccwdivider", "tridivider"]:
            # Fork CCW
            new_cell_2: Cell = origin.copy()
            temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-1)%4, 0)
            dx2, dy2 = temp[3]
            ddir = temp[2]
            new_cell_2.tile_x = self.tile_x+dx2
            new_cell_2.tile_y = self.tile_y+dy2
            #new_cell_2.rot(-1+ddir)
            if force_type == 0:
                self.push((dir-1)%4, False, force=1)
            if (self.tile_x+dx2, self.tile_y+dy2) not in cell_map.keys():

                cell_map[self.tile_x+dx2, self.tile_y+dy2] = new_cell_2
                new_cell_2.suppressed = suppress
                foo = increment_with_divergers(self.game, temp[0], temp[1], temp[4])
                if (foo[0], foo[1]) in cell_map.keys():
                    cell_map[foo[0], foo[1]].on_force(foo[4], new_cell_2)
            elif "divider" in cell_map[self.tile_x+dx2, self.tile_y+dy2].get_side((dir+1+ddir)%4):
                cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+3+ddir)%4, new_cell_2, suppress=suppress, force_type=force_type)
                del new_cell_2
            else:
                cell_map[self.tile_x+dx2, self.tile_y+dy2].on_force((dir+3+ddir)%4, new_cell_2)
            

        match self.extra_properties.get("demolishes"):
            case "ortho":
                for i in range(4):
                    dx, dy = get_deltas(i)
                    if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
                        temp_cell: Cell = cell_map[self.tile_x + dx, self.tile_y + dy]
                        if temp_cell.get_side_by_delta(dx, dy) not in ["wall", "trash"]:
                            if dir != (i+2)%4:
                                del cell_map[self.tile_x + dx, self.tile_y + dy] 
            case "mega":
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if (self.tile_x + i, self.tile_y + j) in cell_map.keys():
                            temp_cell: Cell = cell_map[self.tile_x + i, self.tile_y + j]
                            if temp_cell.get_side_by_delta(i, j) not in ["wall", "trash"]:
                                del cell_map[self.tile_x + i, self.tile_y + j]

    def on_effect(self, effect):
        if self.extra_properties.get("transmitter"):
            for i in range(4):
                dx, dy = get_deltas(i)
                if (self.tile_x + dx, self.tile_y + dy) in self.game.cell_map.keys():
                    temp_cell: Cell = self.game.cell_map[self.tile_x + dx, self.tile_y + dy]
                    self.apply_effect(dx, dy, effect)
        if self.infects[0] != "":
            del self.game.cell_map[self.tile_x, self.tile_y]


    def on_rot(self, dir):
        if self.extra_properties.get("transmitter") and not self.suppressed:
            for i in range(4):
                dx, dy = get_deltas(i)
                if (self.tile_x + dx, self.tile_y + dy) in self.game.cell_map.keys():
                    temp_cell: Cell = self.game.cell_map[self.tile_x + dx, self.tile_y + dy]
                    if self.extra_properties.get("transmitter"):
                        self.suppressed = True
                    temp_cell.rot(dir)

            

    def set_id(self, id: int | str) -> None:
        '''Setter to set the id, while changing the image and properties'''
        self.id = id
        self.image = cell_images[self.id]
        self.name = cell_names[self.id]
        self.img_cache = {}

        # Wall: self explanatory
        # Undirectional: Like wall but can be affected by swap force and can be rotated
        # Generator: Generator OUTPUT
        # Unpushable / Unpullable: cannot be forced in the OPPOSITE direection

        # Sides
        self.left: Side = Side(["pushable"]) # Set the left side to pushable
        self.right: Side = Side(["pushable"]) # Set the right side to pushable
        self.top: Side = Side(["pushable"]) # Set the top side to pushable
        self.bottom: Side = Side(["pushable"]) # Set the bottom side to pushable

        self.br = "pushable"
        self.bl = "pushable"
        self.tl = "pushable"
        self.tr = "pushable"

        # Other cell variables
        self.hp: int = 1 # Set the hp to 1
        self.generation: str | int = "normal" # Set the generation to normal
        self.weight = 1 # Set the weight to 1
        self.rotatable = True

        # Push/pull variables
        self.pushes = False # Set the pushes flag to False
        self.pulls = False # Set the pulls flag to False
        self.drills = False
        self.cwgrabs = False
        self.ccwgrabs = False
        #self.swaps = False # Set the swaps flag to False
        self.gears = 0 # Set the gears flag to False
        self.minigears = 0
        self.skewgears = 0
        self.demolishes = False
        self.nudges = False
        self.mirrors = []
        self.bobs = False
        self.lifes = False
        self.infects = ("", "", 0)

        # Flags
        self.suppressed = False # Set the suppressed flag to False
        self.eat_left = False # Set the eat left flag to False
        self.eat_right = False # Set the eat right flag to False
        self.eat_top = False # Set the eat top flag to False
        self.eat_bottom = False # Set the eat bottom flag to False

        self.tags = {"enemy": False, "ally": False, "neutral": False, "fiend": False}

        self.extra_properties = {}

        match self.id:
            case 1:
                self.left = Side(["wall"])
                self.right = Side(["wall"])
                self.top = Side(["wall"])
                self.bottom = Side(["wall"])
                self.br = "wall"
                self.bl = "wall"
                self.tl = "wall"
                self.tr = "wall"
            case 2:
                self.pushes = True
                self.chirality = [0]
            case 3:
                self.right = Side(["generator"])
                self.chirality = [0]
            case 4:
                pass  # just a pushable
            case 5:
                self.top = Side(["undirectional"])
                self.bottom = Side(["undirectional"])
                self.chirality = [0, 2]
            case 6:
                self.top = Side(["undirectional"])
                self.bottom = Side(["undirectional"])
                self.left = Side(["undirectional"])
                self.chirality = [0]
            case 7:
                self.bottom = Side(["undirectional"])
                self.left = Side(["undirectional"])
                self.chirality = [-1]
            case 8:
                self.left = Side(["undirectional"])
                self.chirality = [0]
            case 9:
                self.top = Side(["cwrotator"])
                self.right = Side(["cwrotator"])
                self.bottom = Side(["cwrotator"])
                self.left = Side(["cwrotator"])
            case 10:
                self.top = Side(["ccwrotator"])
                self.right = Side(["ccwrotator"])
                self.bottom = Side(["ccwrotator"])
                self.left = Side(["ccwrotator"])
            case 11:
                self.top = Side(["180rotator"])
                self.right = Side(["180rotator"])
                self.bottom = Side(["180rotator"])
                self.left = Side(["180rotator"])
            case 12:
                self.left = Side(["trash"])
                self.right = Side(["trash"])
                self.top = Side(["trash"])
                self.bottom = Side(["trash"])
            case 13:
                self.left = Side(["enemy"])
                self.right = Side(["enemy"])
                self.top = Side(["enemy"])
                self.bottom = Side(["enemy"])
                self.tags["enemy"] = True
            case 14:
                self.pulls = True
                self.chirality = [0]
            case 15:
                self.chirality = [0, 2]
                self.mirrors = [(0, 4)]
            case 16:
                self.right = Side(["ccwdiverger"])
                self.bottom = Side(["cwdiverger"])
                self.chirality = [-1]
            case 17:
                self.right = Side(["redirector"])
                self.bottom = Side(["redirector"])
                self.top = Side(["redirector"])
                self.left = Side(["redirector"])
                self.chirality = [0]
            case 18:
                self.gears = 1
            case 19:
                self.gears = -1
            case 20:
                self.generation = 0
            case 21:
                self.left = Side(["repulse"])
                self.right = Side(["repulse"])
                self.top = Side(["repulse"])
                self.bottom = Side(["repulse"])
            case 22:
                self.left = Side(["weight"])
                self.right = Side(["weight"])
                self.top = Side(["weight"])
                self.bottom = Side(["weight"])
            case 23:
                self.right = Side(["generator"])
                self.top = Side(["generator"])
                self.chirality = [1]
            case 24:
                self.left = Side(["enemy"])
                self.right = Side(["enemy"])
                self.top = Side(["enemy"])
                self.bottom = Side(["enemy"])
                self.hp = 2
                self.tags["enemy"] = True
            case 25:
                self.right = Side(["freezer"])
                self.top = Side(["freezer"])
                self.left = Side(["freezer"])
                self.bottom = Side(["freezer"])
            case 26:
                self.right = Side(["cwgenerator"])
                self.chirality = [0]
            case 27:
                self.right = Side(["ccwgenerator"])
                self.chirality = [0]
            case 28:
                self.pushes = True
                self.pulls = True
                self.chirality = [0]
            case 29:
                self.right = Side(["impulse"])
                self.top = Side(["impulse"])
                self.left = Side(["impulse"])
                self.bottom = Side(["impulse"])
            case 30:
                self.right = Side(["flipper"])
                self.top = Side(["flipper"])
                self.left = Side(["flipper"])
                self.bottom = Side(["flipper"])
                self.chirality = [0, 2]
            case 31:
                self.right = Side(["ccwdiverger"])
                self.bottom = Side(["cwdiverger"])
                self.top = Side(["cwdiverger"])
                self.left = Side(["ccwdiverger"])
                self.chirality = [1]
            case 32 | 33 | 34 | 35 | 36 | 37:
                self.left = Side(["undirectional"])
                self.right = Side(["undirectional"])
                self.top = Side(["trash"])
                self.bottom = Side(["trash"])
                self.chirality = [0]
            case 38:
                self.right = Side(["diverger"])
                self.left = Side(["diverger"])
                self.chirality = [0, 2]
            case 39:
                self.right = Side(["diverger"])
                self.bottom = Side(["diverger"])
                self.left = Side(["diverger"])
                self.top = Side(["diverger"])
            case 40:
                self.right = Side(["generator", "twistgenerator"])
                self.chirality = [0]
            case 41:
                self.left = Side(["wall"])
                self.right = Side(["wall"])
                self.top = Side(["wall"])
                self.bottom = Side(["wall"])
                self.br = "wall"
                self.bl = "wall"
                self.tl = "wall"
                self.tr = "wall"
                self.generation = ["ghost"]
            case 42:
                self.left = Side(["antiweight"])
                self.right = Side(["weight"])
                self.chirality = [0]
            case 43:
                self.extra_properties["shield"] = (1, "moore")
            case 44:
                self.right = Side(["intaker", "trash"])
                self.chirality = [0]
            case 45:
                self.right = Side(["replicator"])
                self.chirality = [0]
            case 46:
                self.right = Side(["replicator"])
                self.top = Side(["replicator"])
                self.chirality = [1]
            case 47:
                self.right = Side(["fungal"])
                self.top = Side(["fungal"])
                self.left = Side(["fungal"])
                self.bottom = Side(["fungal"])
            case 48:
                self.left = Side(["forker"])
                self.chirality = [0]
            case 49:
                self.left = Side(["triforker"])
                self.chirality = [0]
            case 50:
                self.left = Side(["superrepulse"])
                self.right = Side(["superrepulse"])
                self.top = Side(["superrepulse"])
                self.bottom = Side(["superrepulse"])
            case 51:
                self.left = Side(["trash"])
                self.right = Side(["trash"])
                self.top = Side(["trash"])
                self.bottom = Side(["trash"])
                self.extra_properties["demolishes"] = "ortho"
            case 52:
                self.left = Side(["unpushable", "ungrabbable"])
                self.right = Side(["unpullable", "ungrabbable"])
                self.top = Side(["unpushable", "unpullable"])
                self.bottom = Side(["unpushable", "unpullable"])
                self.chirality = [0]
            case 53:
                self.left = Side(["unpushable"])
                self.right = Side(["unpullable"])
                self.bottom = Side(["unpushable"])
                self.top = Side(["unpullable"])
                self.chirality = [1]
            case 54:
                self.left = Side(["unpushable"])
                self.right = Side(["unpullable"])
                self.chirality = [0]
            case 55:
                self.right = Side(["supergenerator"])
                self.chirality = [0]
            case 56:
                self.mirrors = [(0, 4), (2, 6)]
                self.chirality = [0, 1, 2, 3]
            case 57:
                self.right = Side(["cwrotator"])
                self.bottom = Side(["cwrotator"])
                self.left = Side(["ccwrotator"])
                self.top = Side(["ccwrotator"])
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
                self.right = Side(["outdirector"])
                self.bottom = Side(["outdirector"])
                self.left = Side(["outdirector"])
                self.top = Side(["outdirector"])
            case 63:
                self.right = Side(["indirector"])
                self.bottom = Side(["indirector"])
                self.left = Side(["indirector"])
                self.top = Side(["indirector"])
            case 64:
                self.right = Side(["cwdirector"])
                self.bottom = Side(["cwdirector"])
                self.left = Side(["cwdirector"])
                self.top = Side(["cwdirector"])
            case 65:
                self.right = Side(["ccwdirector"])
                self.bottom = Side(["ccwdirector"])
                self.left = Side(["ccwdirector"])
                self.top = Side(["ccwdirector"])
            case 66:
                self.left = Side(["cwrotator"])
                self.right = Side(["cwrotator"])
            case 67:
                self.left = Side(["ccwrotator"])
                self.right = Side(["ccwrotator"])
            case 68:
                self.left = Side(["180rotator"])
                self.right = Side(["180rotator"])
            case 69:
                self.top = Side(["wall"])
                self.bottom = Side(["wall"])
                self.br = "wall"
                self.bl = "wall"
                self.tl = "wall"
                self.tr = "wall"
                self.chirality = [0, 2]
            case 70:
                self.right = Side(["cwrotator"])
                self.left = Side(["cwrotator"])
                self.bottom = Side(["ccwrotator"])
                self.top = Side(["ccwrotator"])
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
                self.left = Side(["ice"])
                self.top = Side(["ice"])
                self.right = Side(["ice"])
                self.bottom = Side(["ice"])
            case 80:
                self.mirrors = [(0, 4), (1, 5), (2, 6), (3, 7)]
            case 81:
                self.top = Side(["cwgrapulse"])
                self.right = Side(["cwgrapulse"])
                self.bottom = Side(["cwgrapulse"])
                self.left = Side(["cwgrapulse"])
            case 82: 
                self.top = Side(["ccwgrapulse"])
                self.right = Side(["ccwgrapulse"])
                self.bottom = Side(["ccwgrapulse"])
                self.left = Side(["ccwgrapulse"])
            case 83: 
                self.top = Side(["ccwdiverger"])
                self.left = Side(["diverger"])
                self.bottom = Side(["cwdiverger"])
            case 84:
                self.left = Side(["diverger"])
                self.right = Side(["diverger"])
                self.top = Side(["cwdiverger"])
                self.bottom = Side(["cwdiverger"])
            case 85:
                self.left = Side(["diverger"])
                self.right = Side(["diverger"])
                self.bottom = Side(["ccwdiverger"])
                self.top = Side(["ccwdiverger"])
            case 86: 
                self.left = Side(["displacer"])
                self.right = Side(["displacer"])
                self.top = Side(["ccwdisplacer"])
                self.bottom = Side(["cwdisplacer"])
            case 87:
                self.left = Side(["displacer"])
                self.right = Side(["displacer"])
                self.top = Side(["cwdisplacer"])
                self.bottom = Side(["cwdisplacer"])
            case 88:
                self.left = Side(["displacer"])
                self.right = Side(["displacer"])
                self.bottom = Side(["ccwdisplacer"])
                self.top = Side(["ccwdisplacer"])
            case 89:
                self.left = Side(["flipper"])
                self.right = Side(["flipper"])
            case 90:
                self.top = Side(["flipper"])
                self.right = Side(["flipper"])
            case 91:
                self.bottom = Side(["cwdisplacer"])
                self.right = Side(["ccwdisplacer"])
            case 92:
                self.bottom = Side(["cwdisplacer"])
                self.right = Side(["ccwdisplacer"])
                self.top = Side(["cwdisplacer"])
                self.left = Side(["ccwdisplacer"])
            case 93:
                self.left = Side(["diverger"])
                self.bottom = Side(["cwdiverger"])
            case 94:
                self.left = Side(["diverger"])
                self.top = Side(["ccwdiverger"])
            case 95:
                self.left = Side(["displacer"])
                self.bottom = Side(["cwdisplacer"])
            case 96:
                self.left = Side(["displacer"])
                self.top = Side(["ccwdisplacer"])
            case 97:
                self.left = Side(["cwforker"])
            case 98:
                self.left = Side(["ccwforker"])
            case 99:
                self.left = Side(["divider"])
            case 100:
                self.left = Side(["tridivider"])
            case 101:
                self.left = Side(["cwdivider"])
            case 102:
                self.left = Side(["ccwdivider"])
            case 103:
                self.extra_properties["conditional"] = True
            case 104:
                self.left = Side(["antiweight"])
                self.right = Side(["antiweight"])
                self.top = Side(["antiweight"])
                self.bottom = Side(["antiweight"])
            case 105:
                self.extra_properties["transmitter"] = True
            case 106:
                self.right = Side(["shifter"])
            case 107:
                self.right = Side(["shifter"])
                self.top = Side(["shifter"])
            case 108:
                self.minigears = 1
            case 109:
                self.minigears = -1
            case 110:
                self.right = Side(["cwgenerator", "cloner"])
            case 111:
                self.right = Side(["ccwgenerator", "cloner"])
            case 112:
                pass
            case 113:
                self.right = Side(["generator", "redirectgenerator"])
            case 114:
                self.nudges = True
            case 115:
                self.slices = True
            case 116 | 117 | 118 | 119 | 120 | 121 | 122:
                self.hp = 0
                self.left = Side(["enemy"])
                self.right = Side(["enemy"])
                self.top = Side(["enemy"])
                self.bottom = Side(["enemy"])
                self.generation = "ghost"
                self.rotatable = False
            case 123:
                self.infects = ("adj", "cells", 1)
            case 124:
                self.infects = ("skw", "cells", 1)
            case 125:
                self.infects = ("sur", "cells", 1)
            case 126:
                self.right = Side(["fungal", "wall"])
                self.left = Side(["fungal", "wall"])
                self.top = Side(["fungal", "wall"])
                self.bottom = Side(["fungal", "wall"])
                self.br = "wall"
                self.bl = "wall"
                self.tl = "wall"
                self.tr = "wall"
            case 127:
                self.infects = ("adj", "all", 1)
            case 128:
                self.infects = ("adj", "air", 1)
            case 129:
                self.infects = ("skw", "all", 1)
            case 130:
                self.infects = ("skw", "air", 1)
            case 131:
                self.infects = ("sur", "all", 1)
            case 132:
                self.infects = ("sur", "air", 1)
            case 133:
                self.infects = ("adj", "air", 0.5)
            case 134:
                self.infects = ("adj", "cells", 0.5)
            case 135:
                self.infects = ("adj", "all", 0.5)
            case 136:
                self.left = Side(["pushclamper"])
                self.right = Side(["pushclamper"])
                self.top = Side(["pushclamper"])
                self.bottom = Side(["pushclamper"])
            case 137:
                self.left = Side(["pullclamper"])
                self.right = Side(["pullclamper"])
                self.top = Side(["pullclamper"])
                self.bottom = Side(["pullclamper"])
            case 138:
                self.left = Side(["grabclamper"])
                self.right = Side(["grabclamper"])
                self.top = Side(["grabclamper"])
                self.bottom = Side(["grabclamper"])
            case 139:
                self.left = Side(["swapclamper"])
                self.right = Side(["swapclamper"])
                self.top = Side(["swapclamper"])
                self.bottom = Side(["swapclamper"])
            case 140:
                self.right = Side(["wall"])
                self.top = Side(["wall"])
                self.bl, self.tl, self.br, self.tr = "wall", "wall", "wall", "wall"
            case 141:
                self.left, self.right, self.top, self.bottom = "trash", "trash", "trash", "trash"
                self.extra_properties["demolishes"] = "mega"
            case 142:
                self.extra_properties["resistance"] = 1
            case 143:
                self.extra_properties["resistance"] = 1
                self.extra_properties["tentative"] = True
            case 144:
                self.extra_properties["restrictance"] = 1
            case 145:
                self.extra_properties["shield"] = (2, "moore")
            case 146:
                self.right = Side(["timewarper"])
            case 147:
                self.right = Side(["timegenerator"])
            case 148:
                self.right = Side(["timewarper"])
                self.top = Side(["timewarper"])
            case 149:
                self.lifes = True
            case 150:
                self.right = Side(["wall", "cwspinner"])
                self.left = Side(["wall", "cwspinner"])
                self.bottom = Side(["wall", "cwspinner"])
                self.top = Side(["wall", "cwspinner"])
            case 151:
                self.right = Side(["wall", "ccwspinner"])
                self.left = Side(["wall", "ccwspinner"])
                self.bottom = Side(["wall", "ccwspinner"])
                self.top = Side(["wall", "ccwspinner"])
            case 152:
                self.right = Side(["wall", "180spinner"])
                self.left = Side(["wall", "180spinner"])
                self.bottom = Side(["wall", "180spinner"])
                self.top = Side(["wall", "180spinner"])
            case 153:
                self.extra_properties["key"] = True
            case 154:
                self.extra_properties["door"] = True
                self.left = Side(["wall"])
                self.right = Side(["wall"])
                self.top = Side(["wall"])
                self.bottom = Side(["wall"])
            case 155:
                self.top = Side(["intaker", "trash"])
                self.right = Side(["intaker", "trash"])
            case 156:
                self.right = Side(["mag_s"])
                self.left = Side(["mag_n"])
            case 157:
                self.right = Side(["wall"])
                self.top = Side(["wall"])
                self.bottom = Side(["wall"])
                self.bl = self.tl = self.br = self.tr = "wall"
            case 158:
                self.right = Side(["wall"])
                self.bl = self.tl = self.br = self.tr = "wall"
            case 159:
                self.bl = self.tl = self.br = self.tr = "wall"
            case 208:
                self.left = Side(["diverger"])
                self.chirality = [0]
            case 231:
                self.left = Side(["silicon"])
                self.top = Side(["silicon"])
                self.right = Side(["silicon"])
                self.bottom = Side(["silicon"])
            case 269:
                self.pushes = True
                self.slices = True
            case 270:
                self.pulls = True
                self.slices = True
            case 272:
                self.grabs = True
                self.slices = True
            case 276:
                self.drills = True
                self.slices = True
            case 1201:
                self.right = Side(["dextroanlevogenerator"])
            case "bob":
                self.bobs = True
            case _:
                pass

        if self.pushes or self.pulls or self.drills or self.cwgrabs or self.ccwgrabs or self.nudges:
            self.moves = True
        else:
            self.moves = False

    def mexican_standoff(self, cell: Self, destroy=True):
        '''Resolves a standoff between two cells. Returns False if the caller is destroyed'''
        if self.protected or cell.protected:
            return True
        dec_hp = min(self.hp, cell.hp)
        if destroy:
            self.hp -= dec_hp
            cell.hp -= dec_hp

            self.check_hp()
            cell.check_hp()
            self.game.play_destroy_sound = True

        if self.hp <= (0 if destroy else cell.hp):
            return False
        return True
    
    def shift(self, dir: int) -> bool:
        self.test_gen(dir, 0, endo=True)
        self.test_intake((dir+2)%4)

    def do_shift(self, dir: int) -> bool:
        if self.get_side(dir) == "shifter":
            self.shift(dir)


    def push(self, dir: int, move: bool, hp: int = 1, force: int = 0, speed: int = 1, test: bool = False, active=True, bypass_bias = False) -> bool | int:
        '''Tests a push, and returns False if failed'''
        cell_map = self.game.cell_map
        if self not in cell_map.values():
            return False
        if speed == 1 or not move:
            dx: int
            dy: int
            dx, dy = get_deltas(dir)
            bias: int = force
            row, deltas, ddirs, fail = get_row(self.game, (self.tile_x, self.tile_y), dir, 0)
            trash_flag = False
            suicide_flag = False
            enemy_flag = False
            killer_cell = None
            killer_cell_hp = 0
            affected_cells = [row[0]]
            old_x: int = self.tile_x
            old_y: int = self.tile_y

            if not move:
                bias += 0
            if self.get_side(dir+2) == "repulse":
                print("supple")
                bias += 1


            fx, fy, fdir, _, ppp = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)   

            if self.dir == dir and self.pushes:
                self.suppressed = True                    

            if (fx, fy) in cell_map.keys():
                cell = cell_map[fx, fy]
                if cell.get_side((dir+fdir)) in ["undirectional", "unpushable"]:
                    cell_map[fx, fy].on_force(fdir, self)
                    fail = True
                if cell.get_side((dir+2)) in ["forker", "triforker", "cwforker", "ccwforker", "trash", "divider", "tridivider", "cwdivider", "ccwdivider"]:
                    trash_flag = True
                elif cell.get_side((dir+2)) in ["wall"]:
                    cell_map[fx, fy].on_force(fdir, self)
                    fail = True
                if "enemy" in cell.get_side((dir+fdir+2)) and not cell.protected:
                    enemy_flag = True
            x = fx
            y = fy
            cell = self
            
            bias = (math.inf if bypass_bias else self.get_push_bias(dir, bias))




            if bias <= 0:
                print(bias)
                fail = True
            
            row = affected_cells[:]

            
            temp: list[Cell] = []
            for x, y, _, _, _ in row[1:]:
                temp.append(cell_map[(x, y)])

            if (fx, fy) in cell_map.keys():
                cell_map[fx, fy].on_force(fdir, self, force_type="push")

            if (fx, fy) in cell_map.keys() and not trash_flag and not enemy_flag and not cell_map[fx, fy].pushclamped and not fail:

                try:
                    result = cell_map[fx, fy].push(dir+fdir, True, force=math.inf, speed=speed, test=test, active=False, bypass_bias=True)
                    if result == (-1,):
                        qir = True

                except RecursionError:
                    print("E")
                    return False


            if move and not test:
                if not self.nudge(dir, True):
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
    
    def slice(self, dir: int, move: bool, force: int = 1) -> bool:
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir, 0)
        fdir = incr[4]
        if not self.nudge(dir, move):
            if (self.tile_x, self.tile_y) not in self.game.cell_map.keys():
                print("ee")
                return False
            front_cell: Cell = self.game.cell_map[incr[:2]]
            if front_cell.get_side(fdir) in ["unpushable", "undirectional"] or front_cell.get_side((fdir+2)%4) in ["wall", "trash"] or front_cell.pushclamped:
                return
            if not front_cell.push((dir+1)%4, True, force=force):
                if not front_cell.push((dir-1)%4, True, force=force):
                    return False
            self.nudge(dir, move)   

        return True
                
    
        

    
    def pull(self, dir: int, move: bool, force: int = 0, test: bool = False, bypass_bias = False) -> bool:
        '''Tests a pull, and returns False if failed. Uses the deprecated get_row method.'''
        cell_map = self.game.cell_map
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
            incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+2)%4, 2)
            back_cell_coord = incr[:2]
            #row, deltas, ddirs, fail = get_row(self.game, (self.tile_x, self.tile_y), (dir+2)%4, 2)
        else:
            incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+2)%4, 2)
            back_cell_coord = incr[:2]
            starting_x, starting_y, dir_e, _, b = increment_with_divergers(self.game, back_cell_coord[0], back_cell_coord[1], (incr[4])%4, 2)
            ##print(.+?)incr)
            ##print(.+?)starting_x, starting_y)
            
            #row, deltas, ddirs, fail = get_row(self.game, (starting_x, starting_y), (dir+2)%4, 2)
        
        #row_cells = [cell_map[item[:2]] for item in row
            
        suicide_flag = False
        enemy_flag = False
        row_interrupt_flag = False

        new_x, new_y, new_dir, delta, _ = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir, 0)
        bias = force
        total_bias = force


        
        if move:
            if (new_x, new_y) in cell_map.keys():
                front_cell = cell_map[new_x, new_y]

        if self.get_side(dir+2) == "impulse":
                print("supple")
                bias += 1



        if increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+2)%4, 2)[:2] in cell_map.keys():
            if not move:
                return False
            
        total_bias = math.inf if bypass_bias else self.get_pull_bias(dir, bias)
        #print(.+?)total_bias)

        if total_bias <= 0:
            #print(.+?)"t")
            return False

        



        

                #return False

        if self.moves and self.dir == dir:
            self.suppressed = True
        if move:
            if not self.nudge(dir, True):
                pass
        
        temp: list[Cell] = []




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
                if incr[:2] in cell_map.keys():
                    
                    if move:
                        if cell_map[incr[:2]].get_side((dir)%4) not in ["wall", "trash", "enemy"] and cell_map[incr[:2]].get_side((dir)%4) not in ["unpullable", "undirectional"] and not cell_map[incr[:2]].pullclamped:
                            cell_map[incr[:2]].pull((incr[4]+2)%4, True, force=bias, bypass_bias=True)
            else:
                if (starting_x, starting_y) in cell_map.keys():
                    if cell_map[starting_x, starting_y].get_side((dir)%4) not in ["wall", "trash", "enemy"] and cell_map[starting_x, starting_y].get_side((dir)%4) not in ["unpullable", "undirectional"]:
                        if incr[2] not in cell_map.keys() or not cell_map[incr[:2]].pullclamped:
                            cell_map[starting_x, starting_y].pull((b+2)%4, True, force=bias, bypass_bias = True)


        return True
    
    def get_weight(self, dir):
        pass
    
    def get_pull_bias(self, dir: int, force: int, times: int = -1, suppress: bool = True) -> int:
        cell_map = self.game.cell_map
        if times == 0:
            return force
        flag = False
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+2)%4, force_type=0, displace=True)
        if cell.pulls and (cell.dir)%4 == (dir)%4:
            bias+=1
        if cell.pulls and (cell.dir)%4 == (dir+2)%4:
            bias -= 1

        if cell.get_side((incr[4]+2)%4) == "impulse":
            bias-=1
        
        bias = self.handle_weights(bias, dir)

        if self.pulls and self.dir == dir:
            cell.suppressed |= False



        if incr[:2] not in cell_map.keys():
            # Things that happen when the row breaks
 
            return bias
        bias = cell_map[incr[:2]].get_pull_bias((dir)%4, force=bias, times = times-1, suppress=suppress)
        
        return bias
    
    def test_swap(self, dx1, dy1, dx2, dy2) -> bool:
        '''0: horizontal, 1: neg-diag, 2: vertical, 3: pos-diag'''
        cell_map = self.game.cell_map

        if (self.tile_x + dx1, self.tile_y + dy1) in cell_map.keys():
            if cell_map[(self.tile_x + dx1, self.tile_y + dy1)].get_side_by_delta(dx1, dy1) in ["wall", "trash", "enemy"] or cell_map[(self.tile_x + dx1, self.tile_y + dy1)].mirrors or cell_map[(self.tile_x + dx1, self.tile_y + dy1)].swapclamped:
                return False
        if (self.tile_x + dx2, self.tile_y + dy2) in cell_map.keys():
            if cell_map[(self.tile_x + dx2, self.tile_y + dy2)].get_side_by_delta(dx2, dy2) in ["wall", "trash", "enemy"] or cell_map[(self.tile_x + dx2, self.tile_y + dy2)].mirrors or cell_map[(self.tile_x + dx2, self.tile_y + dy2)].swapclamped:
                return False
        
        swap_cells(self.game, (self.tile_x + dx1, self.tile_y + dy1), (self.tile_x + dx2, self.tile_y + dy2))

        return True

    def test_rot(self, dir: int, rot: int) -> bool:
        cell_map = self.game.cell_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) in cell_map.keys():
            target_cell: Cell = cell_map[(self.tile_x+dx, self.tile_y+dy)]
        else:
            return False
        if target_cell.get_side((dir+2)%4) == "wall":
            return False
        
        #rot_sound.play()
        target_cell.rot(rot)
        return True
    
    def test_redirect(self, dir: int, rot: int) -> bool:
        cell_map = self.game.cell_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) in cell_map.keys():
            target_cell: Cell = cell_map[(self.tile_x+dx, self.tile_y+dy)]
        else:
            return False
        if target_cell.get_side((dir+2)%4) == "wall":
            return False
        
        #rot_sound.play()
        target_cell.rot((-target_cell.dir+rot+1)%4-1)
        return True
    
    def redirect(self, dir) -> bool:
        self.rot((-self.dir+dir+1)%4-1)
        

    def gen(self, dir, cell: Self, endo: bool = False) -> Self:
        cell_map = self.game.cell_map
        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir)%4)[3]
        out_dir = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir)%4)[4]
        generated_cell: Cell = cell
        if generated_cell.generation == "ghost":
            return False
        # Cells have already been pushed
        # Just create new cells if you have to
        # Cells have already been pushed
        # Just create new cells if you have to
        if not (hp := self.push(dir, False, hp = generated_cell.hp, force=1)):
            return
        if (self.tile_x + dx, self.tile_y + dy) not in cell_map.keys():
            generated_cell.hp = 1
            generated_cell.old_x = self.tile_x
            generated_cell.old_y = self.tile_y
            generated_cell.hp = hp
            generated_cell.check_hp()


            #generated_cell.check_generation()

            #print(.+?)"eee")
            if generated_cell.id:
                cell_map[(self.tile_x + dx, self.tile_y + dy)] = generated_cell
            return generated_cell
        else:
            if cell_map[generated_cell.tile_x, generated_cell.tile_y].get_side(dir+2) in ["trash", "forker", "triforker", "cwforker", "ccwforker"]: 
                self.game.play_destroy_flag = True
                generated_cell.old_x = self.tile_x
                generated_cell.old_y = self.tile_y
                self.game.delete_map.append(generated_cell)
                cell_map[generated_cell.tile_x, generated_cell.tile_y].on_force(out_dir, generated_cell)
                return generated_cell

            return None
        
    def check_generation(self):
        cell_map = self.game.cell_map
        if type(self.generation) != int:
            return
        if self.generation < 0:
            if self in cell_map.values():
                del cell_map[self.tile_x, self.tile_y]
            self.set_id(0)


    
    def test_gen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False, endo: bool = False, redirect: bool = False) -> bool:
        cell_map = self.game.cell_map

        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-angle+2)%4)[3]
        oddir, (odx, ody) = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)[2:4]
        enemy_flag = False
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():

            behind_cell: Cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
        else:
            return False
        generated_cell: Cell = Cell(self.game, self.tile_x+odx, self.tile_y+ody, behind_cell.id, (behind_cell.dir+angle)%4)
        if twist:
            generated_cell.flip((dir*2+2)%4)
        if redirect:
            generated_cell.redirect(dir)
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
        if not endo:
            try:
                generated_cell.generation -= 1
            except TypeError:
                pass
        generated_cell.check_generation()
        temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-angle)%4)
        new_cell = self.gen(dir, generated_cell, endo=endo)




            

    
    def test_supergen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False) -> bool:
        cell_map = self.game.cell_map

        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-angle+2)%4)[3]
        oddir, (odx, ody) = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)[2:4]
        row, _, ddirs, _ = get_row(self.game, (self.tile_x, self.tile_y), (dir+2)%4, force_type=2)
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
        cell_map = self.game.cell_map
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
                if cell_map[coord].gears or cell_map[coord].minigears:
                    return False
        for i in range(7):
            swap_cells(self.game, surrounding_cells[i], surrounding_cells[i+1])
        for i in range(1, 8, 2):
            if surrounding_cells[i] in cell_map.keys():
                cell_map[surrounding_cells[i]].rot(rot)
                cell_map[surrounding_cells[i]].dir %= 4
        self.game.play_gear_sound = True

        return True

    def test_minigear(self, rot: int) -> bool:
        cell_map = self.game.cell_map
        if rot == 0:
            return False
        surrounding_cells = [(self.tile_x + 1, self.tile_y),
                             (self.tile_x, self.tile_y + 1),
                             (self.tile_x - 1, self.tile_y),
                             (self.tile_x, self.tile_y - 1),]
        if rot > 0:
            surrounding_cells.reverse()
        for i, coord in enumerate(surrounding_cells):
            if coord in cell_map.keys():
                if cell_map[coord].get_side(i//2) == "wall":
                    return False
                if cell_map[coord].gears:
                    return False
        for i in range(3):
            swap_cells(self.game, surrounding_cells[i], surrounding_cells[i+1])
        for i in range(4):
            coord = surrounding_cells[i]
            if coord in cell_map.keys():
                if cell_map[coord].gears or cell_map[coord].minigears:
                    return False
                cell_map[surrounding_cells[i]].rot(rot)
                cell_map[surrounding_cells[i]].dir %= 4
        self.game.play_gear_sound = True

        return True
            
    def test_freeze(self, dir: int) -> bool:
        cell_map = self.game.cell_map
        dx, dy = get_deltas(dir)
        if ((self.tile_x + dx, self.tile_y + dy)) in cell_map.keys():
            target_cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
            if target_cell.get_side(dir) == "wall" or target_cell.id == 25:
                return False
            self.apply_effect(dx, dy, "freeze")
        return True
    
    def test_protect(self, dx: int, dy: int) -> bool:
        cell_map = self.game.cell_map
        #dx, dy = get_deltas(dir)
        if ((self.tile_x + dx, self.tile_y + dy)) in cell_map.keys():
            target_cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
            self.apply_effect(dx, dy, "protect")
        return True
    
    def apply_effect(self, dx, dy, effect):
        cell_map = self.game.cell_map
        #dx, dy = get_deltas(dir)
        print("applying effect")
        if ((self.tile_x + dx, self.tile_y + dy)) in cell_map.keys():

            target_cell: Cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
            match effect:
                case "freeze":
                    if target_cell.frozen:
                        return False
                    target_cell.frozen = True
                case "protect":
                    if target_cell.protected:
                        return False
                    target_cell.protected = True
                case "lock":
                    if target_cell.locked:
                        return False
                    target_cell.locked = True
                case "pushclamp":
                    if target_cell.pushclamped:
                        return False
                    target_cell.pushclamped = True
                case "pullclamp":
                    if target_cell.pullclamped:
                        return False
                    target_cell.pullclamped = True
                case "grabclamp":
                    if target_cell.grabclamped:
                        return False
                    target_cell.grabclamped = True
                case "swapclamp":
                    if target_cell.swapclamped:
                        return False
                    target_cell.swapclamped = True
            target_cell.on_effect(effect)
        return True
    
    def revoke_effect(self, dx, dy, effect):
        cell_map = self.game.cell_map
        #dx, dy = get_deltas(dir)
        if ((self.tile_x + dx, self.tile_y + dy)) in cell_map.keys():
            target_cell = cell_map[(self.tile_x + dx, self.tile_y + dy)]
            match effect:
                case "freeze":
                    target_cell.frozen = True
                case "protect":
                    target_cell.protected = True
        return True
    
    def test_intake(self, dir: int):
        cell_map = self.game.cell_map
        deleted = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir, 2)
        if deleted[:2] not in cell_map.keys():
            return False
        deleted_cell = cell_map[deleted[:2]]
        if deleted_cell.get_side(dir%4) in ["wall"] or deleted_cell.get_side(dir+2) in ["undirectional", "unpullable"]:
            return False
        del cell_map[deleted[:2]]
        if not self.pull((dir+2)%4, False, force=1):
            #print(.+?)"e")
            return False
        ##trash_sound.play()
        self.game.delete_map.append(deleted_cell)
        deleted_cell.tile_x = self.tile_x
        deleted_cell.tile_y = self.tile_y

    
    def rot(self, rot: int):
        #rot %= 4
        if self.rotatable and not self.locked:
            self.dir += rot
            self.delta_dir += rot
            self.dir %= 4
            if rot % 4:
                self.game.play_rotate_sound = True

            self.on_rot(rot)

    
    def flip(self, rot: int):
        target_cell = self
        cell_symmetry = (self.chirality[0] + 2*self.dir)%4
        self.rot(flip_guide[(rot-cell_symmetry)%4][0])
        if "ccw" in target_cell.name:
            target_cell.set_id(target_cell.id-1)
        elif "cw" in target_cell.name:
            target_cell.set_id(target_cell.id+1)

    def test_flip(self, dir: int, rot: int) ->  bool:
        cell_map = self.game.cell_map
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) not in cell_map.keys():
            return False

        target_cell = cell_map[self.tile_x+dx, self.tile_y+dy]
        if target_cell.get_side((dir+2)%4) != "wall":
            target_cell.flip(rot)

        return True

        


    def do_push(self, dir):
        if self.suppressed or self.frozen or self.dir != dir:
            return

        if (self.pushes) and self.dir == dir:
            if not self.push(dir, True):  
                if self.slices:
                    if not self.slice(dir, True):
                        return
            
            self.suppressed = True

    def do_slice(self, dir):
        if self.frozen or self.suppressed or self.dir != dir:
            return
        if self.slices:
            if not self.slice(dir, True):
                return

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
            self.pull(dir, False, force=1)

    def do_grapulse(self, dir: int):
        if self.frozen:
            return
        if self.get_side(dir) == "cwgrapulse":
            self.ccw_grab(dir, False)
        elif self.get_side(dir) == "ccwgrapulse":
            self.cw_grab(dir, False)

    def do_pull(self, dir):
        if self.frozen or self.suppressed or not self.pulls or not self.dir == dir:
            return
        pull_bias = self.get_pull_bias(dir, 0, suppress=False)
        if pull_bias <= 0:
            return False
        if not self.pushes:
            if not self.nudge(dir, False):
                ##print(.+?)"le")
                return
            
        else:
            if self.slices:
                if not self.slice(dir, False):
                    if self.pushes:
                        if not self.push(self.dir, False):
                            return
            elif self.pushes:
                if self.push(self.dir, False) is False:
                    return


        if self.cwgrabs or self.ccwgrabs:
            if self.cwgrabs:
                if self.ccwgrabs:
                    if self.grab(self.dir, False):
                        self.suppressed = True
                else:
                    if self.cw_grab(self.dir, False):
                        self.suppressed = True
            elif self.ccwgrabs:
                if self.ccw_grab(self.dir, False):
                    self.suppressed = True


        if self.pull(self.dir, True):
            self.suppressed = True
        #self.suppressed = True

    def drill(self, dir, move: bool = True):
        self.suppressed = True
        cell_map = self.game.cell_map
        dx, dy = get_deltas(dir)
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys() and cell_map[(self.tile_x + dx, self.tile_y + dy)].get_side((dir+2)%4) != "trash":
            if cell_map[(self.tile_x + dx, self.tile_y + dy)].get_side((dir+2)%4) == "wall":
                return False

            if move:
                self.test_swap(0, 0, dx, dy)
        else:
            if move:
                self.nudge(dir, True)
        return True
    def do_drill(self, dir):
        if self.frozen or self.suppressed:
            return
        if not self.drills:
            return
        if self.dir != dir:
            return

        ##print(.+?))

        if self.pushes:
            if not self.drill(self.dir, False):
                self.suppressed = True
                return 
        else:
            if not self.drill(self.dir, False):
                self.suppressed = True
                return 

        if self.cwgrabs or self.ccwgrabs:
            if self.cwgrabs:
                if self.ccwgrabs:
                    if self.grab(self.dir, False):
                        self.suppressed = True
                else:
                    if self.cw_grab(self.dir, False):
                        self.suppressed = True
            elif self.ccwgrabs:
               if self.ccw_grab(self.dir, False):
                   self.suppressed = True

        if self.pushes:
            if not self.push(self.dir, True):
                if self.slices:
                    if not self.slice(self.dir, True):
                        if self.drill(self.dir):
                            self.suppressed = True
                else:
                    if self.drill(self.dir):
                        self.suppressed = True
        else:
            if self.slices:
                if not self.slice(self.dir, True):
                    if self.drill(self.dir):
                        self.suppressed = True
            elif self.drill(self.dir):
                self.suppressed = True
                
        if self.pulls:
            self.pull(self.dir, False)

        #self.suppressed = True
    
    def do_gen(self, dir: int):
        if self.frozen:
            return

        side = self.get_side(dir)
        if side in ["generator"]:
            self.test_gen(dir, 0, clone=(side == "cloner"), twist=(side == "twistgenerator"), redirect=(side == "redirectgenerator"))
        if side in ["cwgenerator", "dextroanlevogenerator"]:
            self.test_gen(dir, 1, clone=(side == "cloner"), twist=(side == "twistgenerator"), redirect=(side == "redirectgenerator"))
        if side in ["ccwgenerator", "dextroanlevogenerator"]:
             
            self.test_gen(dir, -1, clone=(side == "cloner"), twist=(side == "twistgenerator"), redirect=(side == "redirectgenerator"))

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

    def do_bob(self):
        if self.frozen:
            return
        if self.bobs:
            self.push(random.randint(0, 3), True, force=1)

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
        if self.minigears == dir:
            self.test_minigear(self.minigears)

    def do_freeze(self):
        if self.frozen:
            return
        for i in range(4):
            if self.get_side(i) == "freezer":
                self.test_freeze(i)

    def do_effect_giving(self):
        if self.frozen:
            return
        if self.extra_properties.get("shield"):
            if self.extra_properties.get("shield")[1] == "moore":
                dist = self.extra_properties["shield"][0]
                for i in range(-dist, dist+1):
                    for j in range(-dist, dist+1):
                        self.apply_effect(i, j, "protect")
        if self.id == 112:
            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                self.apply_effect(i, j, "lock")
        pass
        for i in range(4):
            dx, dy = get_deltas(i)
            if self.get_side(i) == "pushclamper":
                self.apply_effect(dx, dy, "pushclamp")
            if self.get_side(i) == "pullclamper":
                self.apply_effect(dx, dy, "pullclamp")
            if self.get_side(i) == "grabclamper":
                self.apply_effect(dx, dy, "grabclamp")
            if self.get_side(i) == "swapclamper":
                self.apply_effect(dx, dy, "swapclamp")

        dx, dy = 0, 0
        if self.get_side(i) == "pushclamper":
            self.apply_effect(dx, dy, "pushclamp")
        if self.get_side(i) == "pullclamper":
            self.apply_effect(dx, dy, "pullclamp")
        if self.get_side(i) == "grabclamper":
            self.apply_effect(dx, dy, "grabclamp")
        if self.get_side(i) == "swapclamper":
            self.apply_effect(dx, dy, "swapclamp")

    def do_infect(self):
        if self.frozen or self.suppressed:
            return
        self.suppressed = True
        if self.infects[0]:
            if random.random() > self.infects[2]:
                return
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (bool(i and j) and (self.infects[0] in ["sur", "skw"])) \
                    or bool(not (i and j)) and (self.infects[0] in ["sur", "adj"]):
                        if ((self.tile_x+i, self.tile_y+j) in self.game.cell_map.keys() and self.infects[1] in ["cells", "all"]) \
                        or ((self.tile_x+i, self.tile_y+j) not in self.game.cell_map.keys() and self.infects[1] in ["air", "all"]):
                            if (self.tile_x+i, self.tile_y+j) not in self.game.cell_map.keys() \
                            or (self.game.cell_map[self.tile_x+i, self.tile_y+j].infects != self.infects \
                            and self.game.cell_map[self.tile_x+i, self.tile_y+j].get_side_by_delta(i, j) not in ["wall", "trash"] \
                            and not self.game.cell_map[self.tile_x+i, self.tile_y+j].protected):
                                self.game.cell_map[self.tile_x+i, self.tile_y+j] = self.copy()
                                self.game.cell_map[self.tile_x+i, self.tile_y+j].tile_x = self.tile_x+i
                                self.game.cell_map[self.tile_x+i, self.tile_y+j].tile_y = self.tile_y+j
                                self.game.cell_map[self.tile_x+i, self.tile_y+j].suppressed = True
        else:
            if self.lifes:
                self.life()

    def infect(self, dx, dy):
        i = dx
        j = dy
        cell: Self = self.game.cell_map[self.tile_x+i, self.tile_y+j]
        if cell.get_side_by_delta(-dx, -dy) not in ["wall", "trash"]:
            self.game.cell_map[self.tile_x+i, self.tile_y+j] = self.copy()
            self.game.cell_map[self.tile_x+i, self.tile_y+j].tile_x = self.tile_x+i
            self.game.cell_map[self.tile_x+i, self.tile_y+j].tile_y = self.tile_y+j
            self.game.cell_map[self.tile_x+i, self.tile_y+j].suppressed = True

    def life(self):
        previous_map = self.game.previous_map
        cell_map = self.game.cell_map
        surrounding_cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    surrounding_cells.append((self.tile_x + i, self.tile_y + j))
        num = 0
        for coord in surrounding_cells:
            if coord in previous_map.keys():
                if previous_map[coord].lifes == True:
                    num += 1
        if num in [2, 3]:
            pass
        else:
            del cell_map[(self.tile_x, self.tile_y)]
            return False
        for coord in surrounding_cells:
            if coord not in previous_map.keys():
                num2 = 0
                blank_x, blank_y = coord
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (i, j) != (0, 0):
                            if (blank_x + i, blank_y + j) in previous_map.keys():
                                if previous_map[(blank_x + i, blank_y + j)].lifes:
                                    num2 += 1
                if num2 == 3:
                    cell_map[coord] = self.copy()
                    cell_map[coord].tile_x = blank_x
                    cell_map[coord].tile_y = blank_y
                    
            



    def timewarp(self, dir):
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)
        if incr[:2] not in self.game.cell_map.keys():
            if incr[:2] in self.game.initial_cell_map.keys():
                self.game.cell_map[incr[:2]] = self.game.initial_cell_map[incr[:2]].copy()
            return

        cell: Self = self.game.cell_map[incr[:2]]
        if not cell.get_side((dir+2)%4).is_transformable() or cell.protected:
            return
        print("time2")
        if incr[:2] not in self.game.initial_cell_map.keys():
            del self.game.cell_map[incr[:2]]
        else:
            self.game.cell_map[incr[:2]] = self.game.initial_cell_map[incr[:2]].copy()

    def timegen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False, endo: bool = False, redirect: bool = False) -> bool:
        cell_map = self.game.cell_map

        dx: int
        dy: int
        dx, dy = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-angle+2)%4)[3]
        oddir, (odx, ody) = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)[2:4]
        enemy_flag = False
        if (self.tile_x + dx, self.tile_y + dy) in self.game.initial_cell_map.keys():

            behind_cell: Cell = self.game.initial_cell_map[(self.tile_x + dx, self.tile_y + dy)]
        else:
            return False
        generated_cell: Cell = behind_cell.copy()
        generated_cell.tile_x = self.tile_x+odx
        generated_cell.tile_y = self.tile_y+ody
        if twist:
            generated_cell.flip((dir*2+2)%4)
        if redirect:
            generated_cell.redirect(dir)
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
        if not endo:
            try:
                generated_cell.generation -= 1
            except TypeError:
                pass
        generated_cell.check_generation()
        temp = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-angle)%4)
        new_cell = self.gen(dir, generated_cell, endo=endo)

    def do_timewarp(self, dir):
        if self.get_side(dir) == "timewarper":
            self.timewarp(dir)
        if self.get_side(dir) == "timegenerator":
            self.timegen(dir, 0)

                
                

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
        
        tangent = math.atan2(dy, dx)
        if tangent < math.pi/2:
            return self.get_side(3.5)
        elif tangent < math.pi:
            return self.get_side(2.5)
        elif tangent < 3*math.pi/2:
            return self.get_side(1.5)
        else:
            return self.get_side(0.5)
        
    def cw_grab(self, dir: int, move: bool, hp: int = 1, force: int = 1, speed: int = 1, bypass_bias=False) -> bool | int:
        if move:
            if not self.nudge(dir, False, is_grab=True):
                return
        cell_map = self.game.cell_map
        delete_map = self.game.delete_map
        suicide_flag = False
        trash_flag = False
        fail = False
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+1)%4)
        new_x, new_y, new_dir, a, b = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)
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
            if cell_map[incr[:2]].get_side((dir+1+incr[2])%4) == "undirectional":
                fail = True
            if cell_map[incr[:2]].get_side((dir+1+incr[2])%4) == "ungrabbable":
                fail = True
            if cell_map[incr[:2]].grabclamped:
                fail = True
            if cell_map[incr[:2]].get_side((dir+3+incr[2])%4) == "trash":
                trash_flag = True

            if "forker" in cell_map[incr[:2]].get_side((dir+3)%4):
                trash_flag = True
                
        ##print(.+?)force)
        bias = (math.inf if bypass_bias else self.get_cw_grab_bias(dir, force, times=1))
        ##print(.+?)self, bias)

        if bias <= 0:
            return False




        if move:
            del cell_map[(self.tile_x, self.tile_y)]
        if incr[:2] in cell_map.keys():
            #if (new_x, new_y) != (self.tile_x, self.tile_y):
            if not trash_flag and not fail:
                try:
                    ##print(.+?)"hiello")
                    if not cell_map[incr[:2]].cw_grab((incr[4]-1)%4, True, force=bias, speed=speed, bypass_bias=True):
                        #cell_map[(self.tile_x, self.tile_y)] = self
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
                cell_map[killer_cell[:2]].on_force(dir, self, force_type="cwgrab")
                if (self.tile_x, self.tile_y) in cell_map.keys():
                    del cell_map[(self.tile_x, self.tile_y)]
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                self.rot(new_dir)
                if suicide_flag:
                    if "forker" not in cell_map[killer_cell[:2]].get_side((dir+new_dir+2)%4):  
                        delete_map.append(self)

            if self.pushes or self.pulls or self.cwgrabs or self.ccwgrabs:
                if self.dir == (incr[4]-1)%4:
                    self.suppressed = True

            

        return True
    
    def handle_weights(self, orig_force, dir):
        bias = orig_force
        cell = self

        if cell.get_side(dir) == "weight":
            bias-=1
        if cell.get_side(dir) == "antiweight":
            bias+=1

        if temp := cell.extra_properties.get("restrictance"):
            if temp < bias:
                bias = cell.extra_properties["restrictance"]

        if cell.extra_properties.get("resistance"):
                if bias != (cell.dir+1 if cell.extra_properties.get("tentative") else 1):
                    return -math.inf
                
        return bias
    
    def get_push_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        fore_incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir)%4, force_type=0, displace=True)
        back_incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+2)%4, force_type=0, displace=True)
        if cell.pushes and (cell.dir)%4 == (dir)%4:
            bias+=1
        if cell.pushes and (cell.dir)%4 == (dir+2)%4:
            bias -= 1
        
        if cell.get_side((dir+2)%4) == "repulse":
            bias-=1

        
        

        if self.pushes and self.dir == dir:
            self.suppressed |= False

        bias = self.handle_weights(bias, dir)
        if bias == -math.inf:
            return -math.inf


        if fore_incr[:2] in cell_map.keys():
            bias = cell_map[fore_incr[:2]].get_forward_push_bias((fore_incr[4])%4, force=bias, times = times-1)
        if bias <= 0:
            return bias
        if back_incr[:2] in cell_map.keys():
            bias = cell_map[back_incr[:2]].get_reverse_push_bias((back_incr[4]+2)%4, force=bias, times = times-1)
        
        return bias

    def get_forward_push_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir)%4, force_type=0, displace=True)
        if cell.pushes and (cell.dir)%4 == (dir)%4:
            bias+=1
        if cell.pushes and (cell.dir)%4 == (dir+2)%4:
            bias -= 1

        if cell.get_side((dir+2)%4) == "repulse":
            bias-=1
        bias = self.handle_weights(bias, dir)
        

        if self.pushes and self.dir == dir:
            self.suppressed |= False

        if incr[:2] not in cell_map.keys():
            return bias
        bias = cell_map[incr[:2]].get_forward_push_bias((incr[4])%4, force=bias, times = times-1)
        return bias

    def get_reverse_push_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+2)%4, force_type=0, displace=True)
        if cell.pushes and (cell.dir)%4 == (dir)%4:
            bias+=1
        if cell.pushes and (cell.dir)%4 == (dir+2)%4:
            bias -= 1

        if cell.get_side((dir+2)%4) == "repulse":
            bias-=1
        bias = self.handle_weights(bias, dir)
        

        if self.pushes and self.dir == dir:
            self.suppressed |= False

        if incr[:2] not in cell_map.keys():
            return bias
        bias = cell_map[incr[:2]].get_reverse_push_bias((incr[4]+2)%4, force=bias, times = times-1)
        return bias
    
    def get_cw_grab_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        fore_incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+1)%4, force_type=0, displace=True)
        back_incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+3)%4, force_type=0, displace=True)
        if cell.ccwgrabs and (cell.dir+1)%4 == (dir+1)%4:
            bias+=1
        if cell.cwgrabs and (cell.dir-1)%4 == (dir+1)%4:
            bias -= 1
        if cell.get_side((dir+2)%4) == "cwgrapulse":
            bias+=1
        if cell.get_side((dir+2)%4) == "ccwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "cwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "ccwgrapulse":
            bias+=1
        self.handle_weights(bias, dir)
        #cell.on_force(dir, self, force_type=1)
        if self.cwgrabs and self.dir == dir:
            cell.suppressed |= False
        if fore_incr[:2] in cell_map.keys():
            bias = cell_map[fore_incr[:2]].get_forward_cw_grab_bias((fore_incr[4]-1)%4, force=bias, times = times-1)
        if bias <= 0:
            return bias
        if back_incr[:2] in cell_map.keys():
            bias = cell_map[back_incr[:2]].get_reverse_cw_grab_bias((back_incr[4]+1)%4, force=bias, times = times-1)
        


        return bias
    
    def get_forward_cw_grab_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+1)%4, force_type=1, displace=True)
        if cell.ccwgrabs and (cell.dir+1)%4 == (dir+1)%4:
            bias+=1
        if cell.cwgrabs and (cell.dir-1)%4 == (dir+1)%4:
            bias -= 1
        if cell.get_side((incr[4]+2)%4) == "cwgrapulse":
            bias+=1
        if cell.get_side((incr[4]+2)%4) == "ccwgrapulse":
            bias-=1
        if cell.get_side((incr[4])%4) == "cwgrapulse":
            bias-=1
        if cell.get_side((incr[4])%4) == "ccwgrapulse":
            bias+=1
        self.handle_weights(bias, dir)
        #cell.on_force(dir, self, force_type=1)
        if self.cwgrabs and self.dir == dir:
            cell.suppressed |= False
        if incr[:2] in cell_map.keys():
             # Things that happen when the row breaks
            bias = cell_map[incr[:2]].get_forward_cw_grab_bias((incr[4]-1)%4, force=bias, times = times-1)
        return bias
    
    def get_reverse_cw_grab_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+3)%4, force_type=1, displace=True)
        if cell.ccwgrabs and (cell.dir+1)%4 == (dir+1)%4:
            bias+=1
        if cell.cwgrabs and (cell.dir-1)%4 == (dir+1)%4:
            bias -= 1
        if cell.get_side((dir+2)%4) == "cwgrapulse":
            bias+=1
        if cell.get_side((dir+2)%4) == "ccwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "cwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "ccwgrapulse":
            bias+=1
        self.handle_weights(bias, dir)
        #cell.on_force(dir, self, force_type=1)
        if self.cwgrabs and self.dir == dir:
            cell.suppressed |= False
        if incr[:2] not in cell_map.keys():
             # Things that happen when the row breaks

            return bias
        bias = cell_map[incr[:2]].get_reverse_cw_grab_bias((incr[4]+1)%4, force=bias, times = times-1)
        return bias
    

    def get_ccw_grab_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        fore_incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-1)%4, force_type=3, displace=True)
        back_incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-3)%4, force_type=3, displace=True)
        cell = self
        if cell.ccwgrabs and (cell.dir-1)%4 == (dir-1)%4:
            bias+=1
        if cell.cwgrabs and (cell.dir+1)%4 == (dir-1)%4:
            bias -= 1
        if cell.get_side((dir+2)%4) == "cwgrapulse":
            bias+=1
        if cell.get_side((dir+2)%4) == "ccwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "cwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "ccwgrapulse":
            bias+=1
        self.handle_weights(bias, dir)
        if self.ccwgrabs and self.dir == dir:
            cell.suppressed |= False
        if fore_incr[:2] in cell_map.keys():
            bias = cell_map[fore_incr[:2]].get_forward_ccw_grab_bias((fore_incr[4])%4, force=bias, times = times-1)
        if bias <= 0:
            return bias
        if back_incr[:2] in cell_map.keys():
            bias = cell_map[back_incr[:2]].get_reverse_ccw_grab_bias((back_incr[4]+2)%4, force=bias, times = times-1)
        

        return bias
    
    def get_forward_ccw_grab_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-1)%4, force_type=3, displace=True)
        cell = self
        if cell.ccwgrabs and (cell.dir-1)%4 == (dir-1)%4:
            bias+=1
        if cell.cwgrabs and (cell.dir+1)%4 == (dir-1)%4:
            bias -= 1
        if cell.get_side((dir+2)%4) == "cwgrapulse":
            bias+=1
        if cell.get_side((dir+2)%4) == "ccwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "cwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "ccwgrapulse":
            bias+=1
        self.handle_weights(bias, dir)

        if self.ccwgrabs and self.dir == dir:
            cell.suppressed |= False
        

        if incr[:2] not in cell_map.keys():
             # Things that happen when the row breaks

            return bias

        bias = cell_map[incr[:2]].get_ccw_grab_bias((incr[4])%4, force=bias, times=times-1)
        return bias
    
    def get_reverse_ccw_grab_bias(self, dir, force=0, times=-1, suppress=True):
        cell_map = self.game.cell_map
        if times == 0:
            return force
        bias = force
        cell = self
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir-3)%4, force_type=3, displace=True)
        cell = self
        if cell.ccwgrabs and (cell.dir-1)%4 == (dir-1)%4:
            bias+=1
        if cell.cwgrabs and (cell.dir+1)%4 == (dir-1)%4:
            bias -= 1
        if cell.get_side((dir+2)%4) == "cwgrapulse":
            bias+=1
        if cell.get_side((dir+2)%4) == "ccwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "cwgrapulse":
            bias-=1
        if cell.get_side((dir)%4) == "ccwgrapulse":
            bias+=1
        self.handle_weights(bias, dir)
        if self.ccwgrabs and self.dir == dir:
            cell.suppressed |= False
        

        if incr[:2] not in cell_map.keys():
             # Things that happen when the row breaks

            return bias

        bias = cell_map[incr[:2]].get_ccw_grab_bias((incr[4]+2)%4, force=bias, times=times-1)
        return bias
        
    
    def ccw_grab(self, dir: int, move: bool, hp: int = 1, force: int = 1, speed: int = 1) -> bool | int:
        cell_map = self.game.cell_map
        if move:
            if not self.nudge(dir, False, is_grab=True):
                return
        suicide_flag = False
        trash_flag = False
        fail = False
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+3)%4)
        new_x, new_y, new_dir, a, b = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)
        bias = force
        cell = self
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
            if cell_map[incr[:2]].get_side((dir+3+incr[2])%4) == "undirectional":
                fail = True
            if cell_map[incr[:2]].get_side((dir+3+incr[2])%4) == "ungrabbable":
                fail = True
            if cell_map[incr[:2]].grabclamped:
                fail = True
            if cell_map[incr[:2]].get_side((dir+1+incr[2])%4) == "trash":
                trash_flag = True

            if "forker" in cell_map[incr[:2]].get_side((dir+1)%4):
                trash_flag = True
                

        bias += self.get_ccw_grab_bias(dir, 1, times=1)
        cell.on_force(dir, self, force_type=1)

        if bias <= 0:
            return False



        if move:
            del cell_map[(self.tile_x, self.tile_y)]
        if incr[:2] in cell_map.keys():
            #if (new_x, new_y) != (self.tile_x, self.tile_y):
            if not trash_flag and not fail:
                try:
                    cell_map[incr[:2]].ccw_grab((incr[4]+1)%4, True, force=bias, speed=speed)
                except RecursionError:
                    return False

        if move:
            if self.dir == dir:
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
                        self.game.delete_map.append(self)

            if self.pushes or self.pulls or self.cwgrabs or self.ccwgrabs:
                if self.dir == (incr[4]+1)%4:
                    #print(.+?)"ee")
                    self.suppressed = True

            

        return True

    


    def grab(self, dir: int, move: bool, force: int = 0, test: bool = False) -> bool:
        cell_map = self.game.cell_map
        cw_fail = False
        ccw_fail = False
        incr_cw = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+1)%4, 1)
        if incr_cw[:2] in cell_map.keys():
            
            if cell_map[incr_cw[:2]].get_side((dir+2+incr_cw[2])) == "wall" \
            or "trash" in cell_map[incr_cw[:2]].get_side((dir+2+incr_cw[2])) \
            or cell_map[incr_cw[:2]].get_side((dir+incr_cw[2])) == "undirectional" \
            or cell_map[incr_cw[:2]].get_side((dir+incr_cw[2])) == "ungrabbable":
                cw_fail = True


        incr_ccw = increment_with_divergers(self.game, self.tile_x, self.tile_y, (dir+3)%4, 3)
        if incr_ccw[:2] in cell_map.keys():
            if cell_map[incr_ccw[:2]].get_side((dir+2+incr_ccw[2])) == "wall" \
            or "trash" in cell_map[incr_ccw[:2]].get_side((dir+2+incr_ccw[2])) \
            or cell_map[incr_ccw[:2]].get_side((dir+incr_ccw[2])) == "undirectional" \
            or cell_map[incr_ccw[:2]].get_side((dir+incr_ccw[2])) == "ungrabbable":
                ccw_fail = True
            
        if self.get_cw_grab_bias(dir, suppress=False) <= 0 or self.get_ccw_grab_bias(dir, suppress=False) <= 0:
            return False
        
        if move:
            if not self.nudge(dir, True, force, is_grab=True):
                return False

        if incr_cw[:2] in cell_map.keys() and not cw_fail:
            ##print(.+?)"YASS")
            if not cell_map[incr_cw[:2]].cw_grab(incr_cw[4]-1, True, force=math.inf):
                pass
                #return False
        if incr_ccw[:2] in cell_map.keys() and not ccw_fail:
            if not cell_map[incr_ccw[:2]].ccw_grab(incr_ccw[4]+1, True, force=math.inf):
                pass
                #return False


    def nudge(self, dir: int, move: bool, force: int = 0, hp: int = 1, active=True, is_grab=False):
        cell_map = self.game.cell_map
        if (self.tile_x, self.tile_y) not in cell_map.keys():
            return
        suicide_flag = False
        trash_flag = False
        enemy_flag = False
        fail = False
        #incr = increment_with_divergers(self.tile_x, self.tile_y, (dir+3)%4)
        new_x, new_y, new_dir, a, b = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir, displace=True)
        bias = force
        ##print(.+?)"n")
        if (new_x, new_y) in cell_map.keys():
            if "trash" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                suicide_flag = True
                killer_cell = (new_x, new_y, new_dir, a, b)
            if "forker" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                suicide_flag = True
                killer_cell = (new_x, new_y, new_dir, a, b)
            if "divider" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                suicide_flag = True
                killer_cell = (new_x, new_y, new_dir, a, b)
                

        if (new_x, new_y) in cell_map.keys():
                cell = cell_map[new_x, new_y]
                if "enemy" in cell.get_side((dir+2+new_dir)%4) and not cell.protected:
                    self.game.play_destroy_flag = True
                    if not self.mexican_standoff(cell, destroy=move):
                        #cell_map[new_x, new_y] = self
                        
                        self.tile_x = new_x
                        self.tile_y = new_y
                        self.rot(new_dir)

            

                    if self.hp == 0:
                        #cell_map[new_x, new_y] = self
                        self.tile_x = new_x
                        self.tile_y = new_y
                        self.rot(new_dir)
                        suicide_flag = True
                        killer_cell = (new_x, new_y, new_dir, a, b)
                        enemy_flag = True

                
                elif "trash" in cell_map[new_x, new_y].get_side((dir+2+new_dir)%4):
                    suicide_flag = True
                    killer_cell = (new_x, new_y, new_dir, a, b)

                elif cell.cwgrabs and cell.ccwgrabs and is_grab and cell.dir == dir and move:
                    cell.grab(dir, True)

        if not suicide_flag:    
                    
            if (new_x, new_y) in cell_map.keys():
                front_cell = cell_map[new_x, new_y]   
                
                cell_map[(self.tile_x, self.tile_y)] = self
                front_cell.on_force(b, self, force_type="nudge")
                print("yar")
                ##print(.+?)self)
                return False


        if move:
            if (self.tile_x, self.tile_y) in cell_map.keys() and not enemy_flag:
                del cell_map[(self.tile_x, self.tile_y)]
            if (self.dir)%4 == (dir)%4:
                self.suppressed = True

            if suicide_flag:
                ##print(.+?)"eee")
                
                if not enemy_flag:
                    cell_map[killer_cell[:2]].on_force(b, self, force_type="nudge")
                    if (self.tile_x, self.tile_y) in cell_map.keys():
                        del cell_map[(self.tile_x, self.tile_y)]
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                self.rot(new_dir)
                if suicide_flag and not enemy_flag:
                    if "trash" in cell_map[killer_cell[:2]].get_side((dir+new_dir+2)%4):  
                        self.game.play_destroy_flag = True
                        self.game.delete_map.append(self)

            else:
                cell_map[new_x, new_y] = self
                self.tile_x = new_x
                self.tile_y = new_y
                self.rot(new_dir)



        self.game.play_move_sound = True

        return True


    def do_grab(self, dir):
        if self.frozen or self.suppressed:
            return False
        if self.dir == dir:
            if self.cwgrabs or self.ccwgrabs:

                if self.slices:
                    if not self.slice(dir, False):
                        if self.pushes:
                            self.push(dir, False)
                else:
                    if self.pushes:
                        self.push(dir, False)

                if self.cwgrabs:
                    if self.ccwgrabs:

                        if self.grab(dir, True):
                            self.suppressed = True
                    else:
                        if self.cw_grab(dir, True):
                            self.suppressed = True
                elif self.ccwgrabs:
                    if self.ccw_grab(dir, True):
                        self.suppressed = True



                
    def do_nudge(self, dir):
        if self.frozen or self.suppressed:
            return False
        if self.dir == dir:
            if self.nudges:
                if not self.nudge(dir, True):
                    self.suppressed = True

    def do_magnet(self, dir):
        if self.get_side(dir) not in ["mag_n", "mag_s"]:
            return
        incr = increment_with_divergers(self.game, self.tile_x, self.tile_y, dir)
        if incr[:2] in self.game.cell_map.keys():
            cell = self.game.cell_map[incr[:2]]
            if cell.get_side((incr[4]+2)%4) == self.get_side(dir):
                cell.push(incr[4], True, force=1)

        incr2 = increment_with_divergers(self.game, incr[0], incr[1], incr[4]%4)
        if incr2[:2] in self.game.cell_map.keys():
            cell = self.game.cell_map[incr2[:2]]
            if cell.get_side((incr2[4]+2)%4) != self.get_side(dir) and cell.get_side((incr2[4]+2)%4) in ["mag_n", "mag_s"]:
                cell.pull((incr2[4]+2)%4, True, force=1)

        

    def check_hp(self):
        cell_map = self.game.cell_map
        if self.hp == 1 and self.id == 24:
            self.set_id(13)
        elif self.hp == 2 and self.id == 13:
            self.set_id(24)
        elif self.hp == 0:
            #trash_sound.play()
            del cell_map[self.tile_x, self.tile_y]

    def as_dict(self):
        return {}
    
    def set_vars(self, vars):
        pass

        
        
