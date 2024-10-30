import pygame

pygame.init()

# Forward declaration
class Cell: # type: ignore
    pass

cell_names: dict[int|str, str] = {
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
    #48: "forker", #
    #49: "triforker", #
}



cell_cats: list[list[int]] = [
    [],
    [1, 4, 5, 6, 7, 8, 22, 41, 42],
    [2, 14, 28],
    [3, 23, 26, 27, 32, 33, 34, 35, 36, 37, 40, 45, 46],
    [9, 10, 11, 17, 18, 19, 30],
    [21, 29, 15, 18, 19, 44],
    [16, 31, 38, 39],
    [12, 13, 24, 44],
    [],
    [20, 25, 43, 47]
]

chirality: dict[int|str, list[int]|int] = {
    "placeable": [0, 1, 2, 3],
    1: [0, 1, 2, 3],
    2: [2],
    3: [0],
    4: [0, 1, 2, 3],
    5: [0, 2],
    6: [0],
    7: [1],
    8: [0],
    9: [0, 1, 2, 3],
    10: [0, 1, 2, 3],
    11: [0, 1, 2, 3],
    12: [0, 1, 2, 3],
    13: [0, 1, 2, 3],
    14: [0],
    15: [0, 2],
    16: [3],
    17: [0],
    18: [0, 1, 2, 3],
    19: [0, 1, 2, 3],
    20: [0, 1, 2, 3],
    21: [0, 1, 2, 3],
    22: [0, 1, 2, 3],
    23: [1],
    24: [0, 1, 2, 3],
    25: [0, 1, 2, 3],
    26: [2],
    27: [2],
    28: [0],
    29: [0, 1, 2, 3],
    30: [0, 2],
    39: [0, 1, 2, 3]

}

counterparts: dict[int | str, int] = {
    9: 10,
    10: 9,
    18: 19,
    19: 18,
    26: 27,
    27: 26

}

flip_guide: list[list[int]] = [
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

cell_images_raw: list[tuple[int | str, pygame.Surface]] = []
cell_id: int | str
for cell_id in cell_names.keys():
    cell_images_raw.append((cell_id, pygame.image.load(resource_path(f"textures/{cell_names[cell_id]}.png"))))

cell_images: dict[int | str, pygame.Surface] = dict(cell_images_raw)

move_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/move.ogg"))
rot_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/rotate.ogg"))
trash_sound: pygame.mixer.Sound = pygame.mixer.Sound(resource_path("audio/destroy.ogg"))

def lerp(a, b, factor):
    return a + (b-a)*factor

def get_row(coord: tuple[int, int], dir: int, force_dir: int) -> tuple[list[tuple[int, int, int, tuple[int, int], int]], list[tuple[int, int]], list[int], bool]:
    '''Gets a row from a cell in a direction.'''
    from main import cell_map
    #dx, dy = get_deltas(dir)
    test: tuple[int, int, int, tuple[int, int], int] = (coord[0], coord[1], int(0), (0, 0), dir)
    temp: Cell
    incr: tuple[int, int, int, tuple[int, int], int]
    result: list[tuple[int, int, int, tuple[int, int], int]] = []
    deltas: list[tuple[int, int]] = []
    delt_dirs: list[int] = []
    fail = False
    current_dir: int = dir
    while True:
        deltas.append(increment_with_divergers(test[0], test[1], current_dir)[3])
        delt_dirs.append(increment_with_divergers(test[0], test[1], current_dir)[2])
        if test[:2] not in cell_map.keys():
            break
        temp = cell_map[test[:2]]

        incr = increment_with_divergers(test[0], test[1], test[4])
        
        if (temp.tile_x, temp.tile_y) in [i[:2] for i in result]:
            fail = True
            break
            pass
        result.append(test)
        if temp.get_side((current_dir+2+dir-force_dir)%4) in ["wall", "unpushable"]:
            if temp.tile_x != coord[0] or temp.tile_y != coord[1]:
                fail = True
                break


        current_dir += incr[2]
        current_dir %= 4

        
        test = incr
        test = (test[0], test[1], current_dir, test[3], test[4])
        
        
    #deltas = [i[3] for i in result]
    return result, deltas, delt_dirs, fail

def get_deltas(dir: int) -> tuple[int, int]:
    '''Gets the delta values of a direction.'''
    dx: int = 0
    dy: int = 0
    match dir%4:
        case 0:
            dx = 1
            dy = 0
        case 1:
            dx = 0
            dy = 1
        case 2:
            dx = -1
            dy = 0
        case 3:
            dx = 0
            dy = -1

    return dx, dy

def swap_cells(a: tuple[int, int], b: tuple[int, int]):
    '''Swaps two cells in the cell map.'''
    import main
    a_flag, b_flag = False, False
    first: Cell = Cell(0, 0, 0, 0)
    second: Cell = Cell(0, 0, 0, 0)
    if a in main.cell_map.keys():
        first = main.cell_map[a]
        first.tile_x, first.tile_y = b[0], b[1]
        a_flag = True
    if b in main.cell_map.keys():
        second = main.cell_map[b]    
        second.tile_x, second.tile_y = a[0], a[1]
        b_flag = True
    if not a_flag and not b_flag:
        return
    
    if a_flag:
         main.cell_map[b] = first
    else:
        del main.cell_map[b]
    if b_flag:
        main.cell_map[a] = second
    else:
        del main.cell_map[a]
   
def increment_with_divergers(x, y, dir: int) -> tuple[int, int, int, tuple[int, int], int]:
    from main import cell_map
    dx: int
    dy: int
    dx, dy = get_deltas(dir)
    current_x: int = x #+ dx
    current_y: int = y #+ dy
    current_dir: int = dir
    
    if (current_x, current_y) in cell_map.keys():
        next_cell: Cell = cell_map[(current_x, current_y)]
    else:
        next_cell: Cell = Cell(current_x, current_y, 0, dir)
    while True:

        
        

        dx, dy = get_deltas(current_dir)
        current_x += dx
        current_y += dy
        if (current_x, current_y) in cell_map.keys():
            next_cell = cell_map[(current_x, current_y)]
        else:
            break

        if next_cell.get_side((current_dir+2)%4) == "cwdiverger":
            current_dir = (current_dir+1)
        elif next_cell.get_side((current_dir+2)%4) == "ccwdiverger":
            current_dir = (current_dir-1)
        elif next_cell.get_side((current_dir+2)%4) == "diverger":
            pass
        else:
            break

    return current_x, current_y, (current_dir - dir), (current_x-x, current_y-y), current_dir

def rot_center(image: pygame.Surface, rect: pygame.Rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

class Cell(pygame.sprite.Sprite):
    '''A class to represent a cell.'''
    def __init__(self, x: int, y: int, id: int | str, dir: int):
        '''Initialize the cell.'''
        # Initialize the sprite
        super().__init__()

        # Cell variables
        self.tile_x: int = x
        self.tile_y: int = y
        self.old_x: int = x
        self.old_y: int = y
        self.old_dir: int = dir
        self.id: int | str = id
        self.name = cell_names[self.id]
        self.dir: int = dir
        self.actual_dir: int = dir*-90

        self.delta_dir = 0

        self.die_flag = False

        # Image variables
        self.image: pygame.Surface = cell_images[self.id]
        self.rect: pygame.Rect = self.image.get_rect()

        # Effect variables
        self.frozen: bool = False
        self.protected: bool = False

        # Sides
        self.left: str = "pushable"
        self.right: str = "pushable"
        self.top: str = "pushable"
        self.bottom: str = "pushable"

        # Other cell variables
        self.hp: int = 1
        self.generation: str | int = "normal"
        self.weight = 1

        # Push/pull variables
        self.pushes = False
        self.pulls = False
        self.swaps = False
        self.gears = False

        # Flags
        self.suppressed = False
        self.eat_left = False
        self.eat_right = False
        self.eat_top = False
        self.eat_bottom = False

        # Set cell-specific variables
        self.set_id(self.id)

    def __repr__(self) -> str:
        '''Represent the cell as a string.'''
        return f"Cell at {self.tile_x}, {self.tile_y}, id {self.id}, direction {self.dir}"
    
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
        self.do_freeze(dir)  
        self.do_protect()
        self.do_swap()
        self.do_intake(dir)
        self.do_gen(dir)
        self.do_replicate(dir)
        self.do_flip()
        self.do_rot()
        self.do_gear()
        self.do_redirect()
        self.do_impulse(dir)
        self.do_repulse(dir)
        self.do_pull()
        self.do_push()
        return True
    
    def on_force(self, dir, cell: Cell):
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

        if self.id in [47]:
            if self.get_side((dir+2)%4) == "fungal":
                print(cell.id)
                cell.set_id(47)

        if self.id in [48, 49]:
            if "forker" in self.get_side((dir+2)%4):
                self.gen((dir-1)%4, 3, cell.id, suppress=True)
                #cell_map[new_cell_1.tile_x, new_cell_1.tile_y] = new_cell_1
                #new_cell_1.suppressed = True

                '''new_cell_2: Cell = cell.copy()
                dx2, dy2 = get_deltas((dir+1)%4)
                new_cell_2.tile_x = self.tile_x+dx2
                new_cell_2.tile_y = self.tile_y+dy2
                new_cell_2.rot(1)
                self.test_push((dir+1)%4, False)
                cell_map[self.tile_x+dx2, self.tile_y+dy2] = new_cell_2
                new_cell_2.suppressed = True

                if self.get_side((dir+2)%4) == "triforker":
                    new_cell_3: Cell = cell.copy()
                    dx3, dy3 = get_deltas((dir)%4)
                    new_cell_3.tile_x = self.tile_x+dx3
                    new_cell_3.tile_y = self.tile_y+dy3
                    self.test_push((dir)%4, False)
                    cell_map[self.tile_x+dx3, self.tile_y+dy3] = new_cell_3
                    new_cell_3.suppressed = True'''

    def set_id(self, id: int):
        '''Setter to set the id, while changing the image'''
        self.id = id
        self.image = cell_images[self.id]
        match self.id:
            case 1:
                self.left = "wall"
                self.right = "wall"
                self.top = "wall"
                self.bottom = "wall"
            case 2:
                self.pushes = True
            case 3:
                self.left = "generator"
            case 5:
                self.top = "unpushable"
                self.bottom = "unpushable"
            case 6:
                self.top = "unpushable"
                self.bottom = "unpushable"
                self.right = "unpushable"
            case 7:
                self.top = "unpushable"
                self.right = "unpushable"
            case 8:
                self.right = "unpushable"
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
            case 15:
                self.swaps = True
            case 16:
                self.right = "ccwdiverger"
                self.bottom = "cwdiverger"
            case 17:
                self.right = "redirector"
                self.bottom = "redirector"
                self.top = "redirector"
                self.left = "redirector"
            case 18:
                self.gears = True
            case 19:
                self.gears = True
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
            case 27:
                self.right = "ccwgenerator"
            case 28:
                self.pushes = True
                self.pulls = True
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
            case 31:
                self.right = "ccwdiverger"
                self.bottom = "cwdiverger"
                self.top = "cwdiverger"
                self.left = "ccwdiverger"
            case 32 | 33 | 34 | 35 | 36 | 37:
                self.left = "unpushable"
                self.right = "unpushable"
                self.top = "trash"
                self.bottom = "trash"
            case 38:
                self.right = "diverger"
                self.left = "diverger"
            case 39:
                self.right = "diverger"
                self.bottom = "diverger"
                self.left = "diverger"
                self.top = "diverger"
            case 40:
                self.right = "twistgenerator"
            case 41:
                self.left = "wall"
                self.right = "wall"
                self.top = "wall"
                self.bottom = "wall"
                self.generation = "ghost"
            case 42:
                self.left = "antiweight"
                self.right = "weight"
            case 43:
                self.right = "shield"
                self.top = "shield"
                self.left = "shield"
                self.bottom = "shield"
            case 44:
                self.right = "intaker"
            case 45:
                self.right = "replicator"
            case 46:
                self.right = "replicator"
                self.top = "replicator"
            case 47:
                self.right = "fungal"
                self.top = "fungal"
                self.left = "fungal"
                self.bottom = "fungal"
            case 48:
                self.left = "forker"
            case 49:
                self.left = "triforker"

    def test_push(self, dir: int, move: bool, hp: int = 1) -> bool | int:
        '''Tests a push, and returns False if failed'''
        from main import cell_map, delete_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir)
        bias: int = 1
        row, deltas, ddirs, fail = get_row((self.tile_x, self.tile_y), dir, dir)
        trash_flag = False
        suicide_flag = False
        enemy_flag = False
        killer_cell = None
        killer_cell_hp = 0
        affected_cells = [row[0]]
        new_x: int = 0
        new_y: int = 0
        new_dir: int = 0

        if move:
            new_x, new_y, new_dir, _, _ = increment_with_divergers(self.tile_x, self.tile_y, dir)
        for x, y, _, __, con_dir in row[1:]:
            affected_cells.append((x, y, _, __, con_dir))
            cell = cell_map[x, y]
            if cell.get_side((con_dir+2)%4) == "wall" or cell.get_side((con_dir+2)%4) == "unpushable":
                cell.on_force(con_dir, cell_map[affected_cells[-2][:2]])
                return False
            if  ("trash" in cell.get_side((dir+2)%4)) or ("forker" in cell.get_side((dir+2)%4)):
                trash_flag = True
                break
            if "enemy" in cell.get_side((dir+2)%4):
                if not cell_map[affected_cells[-2][:2]].protected and not cell.protected:
                    enemy_flag = True
                    break
            if (cell.pushes, cell.dir) == (True, con_dir):
                bias += 1
            if (cell.pushes, cell.dir) == (True, (con_dir+2)%4) and not cell.frozen:
                bias -= 1
            if cell.get_side((dir+2)%4) == "repulse":
                bias -= 1
            if cell.get_side((dir+2)%4) == "weight":
                bias -= cell_map[x, y].weight
            if cell.get_side((dir+2)%4) == "antiweight":
                bias += cell_map[x, y].weight
            if cell.pushes and cell.dir == con_dir:
                cell.suppressed = True


        if bias <= 0:
            return False
        if fail and len(row) > 1:
            return False
        
        row = affected_cells[:]

        if trash_flag:
            killer_cell = row[-1]
            if move or len(row) > 2:
                if "trash" in cell_map[killer_cell[:2]].get_side((dir+2)%4):             
                    trash_sound.play()
                cell_map[row[-2][:2]].die_flag = True

                cell_map[killer_cell[:2]].on_force(killer_cell[4], cell_map[row[-2][:2]])
            if cell_map[row[-2][:2]] == self:
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
        for cell in temp:
            if (cell.tile_x, cell.tile_y) in cell_map.keys():
                del cell_map[cell.tile_x, cell.tile_y]

        if move:
            if len(temp) > 0:
                temp[0].on_force((self.dir+new_dir)%4, self)
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
     
        if move:
            del cell_map[(self.tile_x, self.tile_y)]
            if not suicide_flag:

                cell_map[new_x, new_y] = self
                self.tile_x = new_x
                self.tile_y = new_y
                self.rot(new_dir)
            else:
                self.tile_x = killer_cell[0]
                self.tile_y = killer_cell[1]
                self.rot(new_dir)
                if trash_flag:
                    if "forker" not in cell_map[killer_cell[:2]].get_side((dir+2)%4):  
                        delete_map.append(self)
        if self.pushes:
            self.suppressed = True
        if killer_cell is not None:
            return hp-killer_cell_hp
        else:
            return hp

    
    def test_pull(self, dir: int, move: bool) -> bool:
        '''Tests a pull, and returns False if failed'''
        from main import cell_map, delete_map
        dx, dy = get_deltas(dir)
        push_flag = False
        new_x: int = 0
        new_y: int = 0
        new_dir: int = 0
        killer_cell: tuple[int, int] = (0, 0)

        if move:
            row, deltas, ddirs, fail = get_row((self.tile_x, self.tile_y), (dir+2)%4, dir)
        else:
            back_cell_coord = increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4)[:2]
            starting_x, starting_y = increment_with_divergers(back_cell_coord[0], back_cell_coord[1], (dir+2)%4)[:2]
            
            row, deltas, ddirs, fail = get_row((starting_x, starting_y), (dir+2)%4, dir)
        
        row_cells = [cell_map[item[:2]] for item in row]
            
        suicide_flag = False
        enemy_flag = False
        row_interrupt_flag = False
        if move:
            new_x, new_y, new_dir, delta, _ = increment_with_divergers(self.tile_x, self.tile_y, dir)

            bias = 0
        else:
            bias = 1
        for cell in row_cells:
            if cell.pushes:
                push_flag = True
        if move:
            if (new_x, new_y) in cell_map.keys():
                front_cell = cell_map[new_x, new_y]
                if front_cell.pushes:
                    push_flag = True
                if front_cell.get_side(dir) in ["trash", "enemy"]:
                    killer_cell = (new_x, new_y)
                    if move:
                        suicide_flag = True
                        if cell_map[killer_cell].id in [13, 24]:
                            if not self.protected:
                                enemy_flag = True
                        cell_map[killer_cell].on_force(self.dir + new_dir, self)
                else:
                    if move:
                        if (not (push_flag or front_cell.pushes)):
                            return False
        if increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4)[:2] in cell_map.keys():
            if not move:
                return False
        for x, y, ddir, _, con_dir in row:
            cell = cell_map[x, y]

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

            if cell.get_side((con_dir)%4) in ["enemy", "wall", "unpushable", "trash"]:
                row_interrupt_flag = True
            if cell.id in [2, 14] and cell.dir == self.dir:
                if cell.id in [2]:
                    push_flag = True
                cell.suppressed = True

        if row_interrupt_flag:
            return False

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
            if not self.test_push(dir, False):
                return False
        move_sound.play()

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
                if not enemy_flag:
                    delete_map.append(self)
        
        temp: list[Cell] = []
        affected_cells = row[:]
        if move:
            if affected_cells:
                del affected_cells[0]
        for item in affected_cells:
            temp.append(cell_map[item[:2]])
            del cell_map[item[:2]]

        if move:
            pulled_cells = row[1:]
        else:
            pulled_cells = row

        if move:
            if len(temp) > 0:
                temp[0].on_force((self.dir+new_dir)%4, self)
        for i, item in enumerate(pulled_cells):
            
            dx, dy = deltas[i]
            cell_map[(item[0]-dx, item[1]-dy)] = temp[i]
            temp[i].tile_x -= dx
            temp[i].tile_y -= dy
            temp[i].rot(-ddirs[i])
            temp[i].on_force(item[4], temp[i-1])


        return True
    
    def test_swap(self, dir: int) -> bool:
        '''0: horizontal, 1: neg-diag, 2: vertical, 3: pos-diag'''
        from main import cell_map
        dx1: int = 0
        dy1: int = 0
        dx2: int = 0
        dy2: int = 0
        match dir:
            case 0:
                dx1, dy1, dx2, dy2 = 1, 0, -1, 0
            case 1:
                dx1, dy1, dx2, dy2 = 1, 1, -1, -1
            case 2:
                dx1, dy1, dx2, dy2 = 0, 1, 0, -1
            case 3:
                dx1, dy1, dx2, dy2 = 1, -1, -1, 1

        if (self.tile_x + dx1, self.tile_y + dy1) in cell_map.keys():
            if cell_map[(self.tile_x + dx1, self.tile_y + dy1)].get_side(int(dir/2)) in ["wall", "trash", "enemy"] or cell_map[(self.tile_x + dx1, self.tile_y + dy1)].swaps:
                return False
        if (self.tile_x + dx2, self.tile_y + dy2) in cell_map.keys():
            if cell_map[(self.tile_x + dx2, self.tile_y + dy2)].get_side(int(dir/2 + 2)) in ["wall", "trash", "enemy"] or cell_map[(self.tile_x + dx2, self.tile_y + dy2)].swaps:
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
    
    def test_gen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False) -> bool:
        from main import cell_map

        dx: int
        dy: int
        dx, dy = get_deltas(dir-angle)
        odx, ody = get_deltas(dir)
        enemy_flag = False
        if (self.tile_x - dx, self.tile_y - dy) in cell_map.keys():
            behind_cell: Cell = cell_map[(self.tile_x - dx, self.tile_y - dy)]
            generated_cell: Cell = Cell(self.tile_x+odx, self.tile_y+ody, behind_cell.id, (behind_cell.dir+angle)%4)
            if clone:
                generated_cell.dir = behind_cell.dir
        else: 
            return False
        
        if behind_cell.generation == "ghost":
            return False
        behind_hp = self.test_push(dir, False, behind_cell.hp)
        print(behind_hp)
        if not behind_hp:
            return False
        print("gen")
        # Cells have already been pushed
        # Just create new cells if you have to
        if (self.tile_x + odx, self.tile_y + ody) not in cell_map.keys():
            generated_cell.hp = behind_hp
            generated_cell.old_x = self.tile_x
            generated_cell.old_y = self.tile_y
            if generated_cell.hp == 1 and generated_cell.id == 24:
                generated_cell.set_id(13)
            if generated_cell.hp == 0:
                return True
            if behind_cell.generation != 'normal':
                return False
            if twist:
                generated_cell.flip((dir*2+2)%4)
            if suppress:
                generated_cell.suppressed = True
            cell_map[(self.tile_x + odx, self.tile_y + ody)] = generated_cell
            return True
        else:
            return False
        
    def gen(self, dir, angle, cell, suppress=False, twist=False):
        from main import cell_map
        generated_cell = Cell(self.tile_x, self.tile_y, cell, (dir+angle)%4)
        behind_hp = self.test_push(dir, False, generated_cell.hp)
        dx, dy = get_deltas(dir-angle)
        odx, ody = get_deltas(dir)
        print(behind_hp)
        if not behind_hp:
            return False
        print("gen")
        # Cells have already been pushed
        # Just create new cells if you have to
        if (self.tile_x + odx, self.tile_y + ody) not in cell_map.keys():
            generated_cell.hp = behind_hp
            generated_cell.tile_x = self.tile_x+odx
            generated_cell.tile_y = self.tile_y+ody
            if generated_cell.hp == 1 and generated_cell.id == 24:
                generated_cell.set_id(13)
            if generated_cell.hp == 0:
                return True
            if generated_cell.generation != 'normal':
                return False
            if twist:
                generated_cell.flip((dir*2+2)%4)
            if suppress:
                generated_cell.suppressed = True
            cell_map[(self.tile_x + odx, self.tile_y + ody)] = generated_cell
            return True
        else:
            return False

        
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
        deleted = increment_with_divergers(self.tile_x, self.tile_y, dir)
        if deleted[:2] not in cell_map.keys():
            return False
        deleted_cell = cell_map[deleted[:2]]
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
        cell_symmetry = chirality[target_cell.id]
        self.rot(flip_guide[rot][target_cell.dir])
        if target_cell.id in counterparts.keys():
            target_cell.set_id(counterparts[target_cell.id])

    def test_flip(self, dir: int, rot: int) ->  bool:
        from main import cell_map
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) not in cell_map.keys():
            return False

        target_cell = cell_map[self.tile_x+dx, self.tile_y+dy]
        target_cell.flip(rot)

        return True

        


    def do_push(self):
        if self.pushes:
            self.test_push(self.dir, True)

    def do_repulse(self, dir: int):
        if self.id == 21:
            self.test_push(dir, False)

    def do_impulse(self, dir: int):
        if self.id == 29:
            self.test_pull(dir, False)

    def do_pull(self):
        if self.pulls:
            self.test_pull(self.dir, True)
    
    def do_gen(self, dir: int):
        if self.id == 3:
            if self.dir == dir:
                self.test_gen(dir, 0)
        if self.id == 23:
            if self.dir in [dir, (dir+1)%4]:
                self.test_gen(dir, 0)
        if self.id == 26:
            if self.dir == dir:
                self.test_gen(dir, 1)
        if self.id == 27:
            if self.dir == dir:
                self.test_gen(dir, -1)

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
        if self.get_side(dir) == "replicator":
            self.test_replicate(dir)

    def do_intake(self, dir: int):
        if self.get_side(dir) == "intaker":
            if self.dir == dir:
                self.test_intake(dir)

    def do_rot(self):
        if self.id == 9:
            for i in range(4):
                self.test_rot(i, 1)
        if self.id == 10:
            for i in range(4):
                self.test_rot(i, -1)
        if self.id == 11:
            for i in range(4):
                self.test_rot(i, 2)

    def do_flip(self):
        if self.id == 30:
            if self.dir in [0, 2]:
                for i in range(4):
                    self.test_flip(i, 0)
            if self.dir in [1, 3]:
                for i in range(4):
                    self.test_flip(i, 2)

    def do_swap(self):
        if self.id == 15:
            if self.dir in [0, 2]:
                self.test_swap(0)
            if self.dir in [1, 3]:
                self.test_swap(2)

    def do_redirect(self):
        for i in range(4):
            if self.get_side(i) == "redirector":
                self.test_redirect(i, self.dir)
    
    def do_gear(self):
        if self.id == 18:
            self.test_gear(1)
        if self.id == 19:
            self.test_gear(-1)

    def do_freeze(self, dir):
        if self.get_side(dir) == "freezer":
            self.test_freeze(dir)

    def do_protect(self):
        if self.id == 43:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.test_protect(i, j)

    def get_side(self, dir: int) -> str:
        match self.dir:
            case 0:
                return [self.right, self.bottom, self.left, self.top][dir]
            case 1:
                return [self.top, self.right, self.bottom, self.left][dir]
            case 2:
                return [self.left, self.top, self.right, self.bottom][dir]
            case 3:
                return [self.bottom, self.left, self.top, self.right][dir]
        return "error"




        
        
        
