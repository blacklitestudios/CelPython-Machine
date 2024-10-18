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
    38: "straightdiverger", #
    39: "crossdiverger", #
    41: "ghost", #
}

cell_cats: list[list[int]] = [
    [],
    [1, 4, 5, 6, 7, 8, 22],
    [2, 14, 28],
    [3, 23, 26, 27],
    [9, 10, 11, 17, 18, 19, 30],
    [21, 29, 15, 18, 19],
    [16, 31, 38, 39],
    [12, 13, 24],
    [],
    [20, 25]
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

cell_images_raw: list[tuple[int | str, pygame.Surface]] = []
cell_id: int | str
for cell_id in cell_names.keys():
    cell_images_raw.append((cell_id, pygame.image.load(f"textures/{cell_names[cell_id]}.png")))

cell_images: dict[int | str, pygame.Surface] = dict(cell_images_raw)

move_sound: pygame.mixer.Sound = pygame.mixer.Sound("audio/move.ogg")
rot_sound: pygame.mixer.Sound = pygame.mixer.Sound("audio/rotate.ogg")
trash_sound: pygame.mixer.Sound = pygame.mixer.Sound("audio/destroy.ogg")

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
            #fail = True
            #break
            pass
        result.append(test)
        if temp.get_side((current_dir+2+dir-force_dir)%4) in ["trash", "wall", "enemy", "unpushable"]:
            if temp.get_side((current_dir+2+dir-force_dir)%4) in ["wall", "unpushable"]:
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
            current_dir = (current_dir+1)%4
        elif next_cell.get_side((current_dir+2)%4) == "ccwdiverger":
            current_dir = (current_dir-1)%4
        elif next_cell.get_side((current_dir+2)%4) == "diverger":
            pass
        else:
            break

    return current_x, current_y, (current_dir - dir), (current_x-x, current_y-y), current_dir

class Cell(pygame.sprite.Sprite):
    '''A class to represent a cell.'''
    def __init__(self, x: int, y: int, id: int | str, dir: int):
        '''Initialize the cell.'''
        # Initialize the sprite
        super().__init__()

        # Cell variables
        self.tile_x: int = x
        self.tile_y: int = y
        self.id: int | str = id
        self.name = cell_names[self.id]
        self.dir: int = dir

        # Image variables
        self.image: pygame.Surface = cell_images[self.id]
        self.rect: pygame.Rect = self.image.get_rect()

        # Effect variables
        self.frozen: bool = False

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

        # Set cell-specific variables

        # wall
        if self.id == 1:
            self.left = "wall"
            self.right = "wall"
            self.top = "wall"
            self.bottom = "wall"

        # ghost
        if self.id == 41:
            self.left = "wall"
            self.right = "wall"
            self.top = "wall"
            self.bottom = "wall"
            self.generation = "ghost"

        # pushers
        if self.id in [2, 28]:
            self.pushes = True
        
        # pullers
        if self.id in [14, 28]:
            self.pulls = True

        # mirrors
        if self.id in [15]:
            self.swaps = True

        if self.id in [18, 19]:
            self.gears = True

        # repulsors
        if self.id == 21:
            self.left = "repulse"
            self.right = "repulse"
            self.top = "repulse"
            self.bottom = "repulse"

        # impulsors
        if self.id == 29:
            self.left = "impulse"
            self.right = "impulse"
            self.top = "impulse"
            self.bottom = "impulse"

        # slider
        if self.id == 5:
            self.top = "unpushable"
            self.bottom = "unpushable"

        # one-directional
        if self.id == 6:
            self.top = "unpushable"
            self.bottom = "unpushable"
            self.right = "unpushable"

        # two-dirctional
        if self.id == 7:
            self.top = "unpushable"
            self.right = "unpushable"
        
        # three-directional
        if self.id == 8:
            self.right = "unpushable"
        
        # ungeneratable
        if self.id == 20:
            self.generation = 0

        # trash
        if self.id == 12:
            self.left = "trash"
            self.right = "trash"
            self.top = "trash"
            self.bottom = "trash"

        # enemy + strong enemy
        if self.id in [13, 24]:
            self.left = "enemy"
            self.right = "enemy"
            self.top = "enemy"
            self.bottom = "enemy"
            if self.id == 24:
                self.hp = 2

        if self.id in [22]:
            self.left = "weight"
            self.right = "weight"
            self.top = "weight"
            self.bottom = "weight"

        if self.id == 16:
            self.right = "ccwdiverger"
            self.bottom = "cwdiverger"
        
        if self.id == 31:
            self.right = "ccwdiverger"
            self.bottom = "cwdiverger"
            self.top = "cwdiverger"
            self.left = "ccwdiverger"

        if self.id == 38:
            self.left = "diverger"
            self.right = "diverger"
        
        if self.id == 39:
            self.right = "diverger"
            self.bottom = "diverger"
            self.top = "diverger"
            self.left = "diverger"

    def __repr__(self) -> str:
        '''Represent the cell as a string.'''
        return f"Cell at {self.tile_x}, {self.tile_y}, id {self.id}, direction {self.dir}"
    
    def copy(self) -> Cell:
        '''Copy constructor'''
        return Cell(self.tile_x, self.tile_y, self.id, self.dir) # type: ignore

    def update(self):
        '''Update the cell, once per frame'''
        from main import cam_x, cam_y, TILE_SIZE, cell_map
        self.rect.x = int(self.tile_x*TILE_SIZE-cam_x)
        self.rect.y = int(self.tile_y*TILE_SIZE-cam_y)

    def draw(self):
        '''Draw the cell on the screen'''
        from main import window, TILE_SIZE, freeze_image, WINDOW_HEIGHT, WINDOW_WIDTH
        if self.rect.y+TILE_SIZE < 0:
            return
        if self.rect.y > WINDOW_HEIGHT:
            return
        if self.rect.x+TILE_SIZE < 0:
            return 
        if self.rect.x > WINDOW_WIDTH:
            return
        img: pygame.Surface = pygame.transform.rotate(pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE)), -self.dir*90)
        window.blit(img, self.rect)
        if self.frozen:
            window.blit(pygame.transform.scale(freeze_image, (TILE_SIZE, TILE_SIZE)), self.rect)

    def tick(self, dir: int):
        '''Tick the cell, once per tick'''
        self.push_extended = False
        self.pull_extended = False
        if (self.suppressed or self.frozen):
            return False
        self.do_freeze(dir)  
        self.do_swap()
        self.do_gen(dir)
        self.do_flip()
        self.do_rot()
        self.do_gear()
        self.do_redirect()
        self.do_impulse(dir)
        self.do_repulse(dir)
        if self.pulls:
            self.do_pull()
        elif self.pushes:
            self.do_push()
        return True


    def set_id(self, id: int):
        '''Setter to set the id, while changing the image'''
        self.id = id
        self.image = cell_images[self.id]

    def test_push(self, dir: int, move: bool, hp: int = 1) -> bool | int:
        '''Tests a push, and returns False if failed'''
        from main import cell_map
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
        new_x: int = 0
        new_y: int = 0
        new_dir: int = 0

        if move:
            new_x, new_y, new_dir, _, _ = increment_with_divergers(self.tile_x, self.tile_y, dir)
        for x, y, _, _, con_dir in row[1:]:
            cell = cell_map[x, y]
            if cell.get_side((con_dir+2)%4) == "wall" or cell.get_side((con_dir+2)%4) == "unpushable":
                 return False
            if  "trash" in cell.get_side((self.dir)%4) :
                trash_flag = True
            if "enemy" in cell.get_side((self.dir)%4):
                enemy_flag = True
            if (cell.pushes, cell.dir) == (True, con_dir):
                bias += 1
            if (cell.pushes, cell.dir) == (True, (con_dir+2)%4):
                bias -= 1
            if cell.get_side((dir+2)%4) == "repulse":
                bias -= 1
            if cell.get_side((dir+2)%4) == "weight":
                bias -= cell_map[x, y].weight
            if cell.id in [2] and cell.dir == con_dir:
                cell.suppressed = True


        if bias <= 0:
            return False
        if fail and len(row) > 1:
            return False
        
        if trash_flag:
            killer_cell = row[-1]
            trash_sound.play()
            if cell_map[row[-2][:2]] == self:
                suicide_flag = True
            else:
                del cell_map[row[-2][:2]]
            del row[-2]
            del row[-1]
        if enemy_flag:
            killer_cell = row[-1][:2]
            trash_sound.play()
            if cell_map[row[-2][:2]] == self:
                suicide_flag = True
            else:
                del cell_map[row[-2][:2]]
                del row[2]
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
            if cell_map[(x, y)] is not self:
                temp.append(cell_map[(x, y)].copy())
            else:
                temp.append(cell_map[(x, y)])
        for cell in temp:
            if (cell.tile_x, cell.tile_y) in cell_map.keys():
                del cell_map[cell.tile_x, cell.tile_y]

        for i, item in enumerate(row[1:]):
            
            dx, dy = deltas[i+1]
            ddir = ddirs[i+1]
            cell_map[(item[0]+dx, item[1]+dy)] = temp[i]
            #if temp[i].dir == dir - 
            temp[i].tile_x += dx
            temp[i].tile_y += dy
            temp[i].dir += ddirs[i+1]
            temp[i].dir %= 4
        
        if move:
            del cell_map[(self.tile_x, self.tile_y)]
            if not suicide_flag:

                cell_map[new_x, new_y] = self
                self.tile_x = new_x
                self.tile_y = new_y
                self.dir += new_dir
                self.dir %= 4
        self.suppressed = True
        if killer_cell is not None:
            return hp-killer_cell_hp
        else:
            return hp

    
    def test_pull(self, dir: int, move: bool) -> bool:
        '''Tests a pull, and returns False if failed'''
        from main import cell_map
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
                if front_cell.id in [12, 13, 24]:
                    killer_cell = (new_x, new_y)
                    if move:
                        suicide_flag = True
                        if cell_map[killer_cell].id in [13, 24]:
                            enemy_flag = True
                else:
                    if move:
                        if (not (push_flag or front_cell.pushes)) or front_cell.pulls:
                            return False
        if increment_with_divergers(self.tile_x, self.tile_y, (dir+2)%4)[:2] in cell_map.keys():
            if not move:
                return False
        for x, y, ddir, _, con_dir in row:
            cell = cell_map[x, y]

            if (cell.pulls, cell.dir) == (True, (con_dir+2)%4):
                bias += 1
            if (cell.pulls, cell.dir) == (True, con_dir):
                bias -= 1
            if cell.get_side((con_dir+2)%4) == "impulse":
                bias -= 1
            if cell.get_side((con_dir+2)%4) == "weight":
                bias -= cell.weight

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
            print(row)
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
                self.dir += new_dir
                self.dir %= 4
        
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
        for i, item in enumerate(pulled_cells):
            
            dx, dy = deltas[i]
            cell_map[(item[0]-dx, item[1]-dy)] = temp[i]
            temp[i].tile_x -= dx
            temp[i].tile_y -= dy
            temp[i].dir -= ddirs[i]
            temp[i].dir %= 4


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
        target_cell.dir += rot
        target_cell.dir %= 4
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
        target_cell.dir = rot
        target_cell.dir %= 4
        return True
    
    def test_gen(self, dir: int, angle: int) -> bool:
        from main import cell_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir-angle)
        odx, ody = get_deltas(dir)
        enemy_flag = False
        if (self.tile_x - dx, self.tile_y - dy) in cell_map.keys():
            behind_cell: Cell = cell_map[(self.tile_x - dx, self.tile_y - dy)]
            generated_cell: Cell = Cell(self.tile_x+odx, self.tile_y+ody, behind_cell.id, (behind_cell.dir+angle)%4)
        else: 
            return False
        
        if behind_cell.generation == "ghost":
            return False
        behind_hp = self.test_push(dir, False, behind_cell.hp)
        if not self.test_push(dir, False, behind_cell.hp):
            return False
        # Cells have already been pushed
        # Just create new cells if you have to
        if (self.tile_x + odx, self.tile_y + ody) not in cell_map.keys():
            generated_cell.hp = behind_hp
            if generated_cell.hp == 1 and generated_cell.id == 24:
                generated_cell.set_id(13)
            if generated_cell.hp == 0:
                return True
            if behind_cell.generation != 'normal':
                return False
            cell_map[(self.tile_x + odx, self.tile_y + ody)] = generated_cell
            return True
        else:
            return False
    
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
            if target_cell.get_side(dir) == "wall":
                return False
            target_cell.frozen = True
        return True

    def test_flip(self, dir: int, rot: int) ->  bool:
        from main import cell_map
        dx, dy = get_deltas(dir)
        if (self.tile_x+dx, self.tile_y+dy) not in cell_map.keys():
            return False

        target_cell = cell_map[self.tile_x+dx, self.tile_y+dy]
        cell_symmetry = chirality[target_cell.id]
        if target_cell.get_side(dir) == 'wall':
            return False
        self.test_rot(dir, flip_guide[rot][target_cell.dir])
        if target_cell.id in counterparts.keys():
            target_cell.set_id(counterparts[target_cell.id])

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
        if self.id == 17:
            for i in range(4):
                self.test_redirect(i, self.dir)
    
    def do_gear(self):
        if self.id == 18:
            self.test_gear(1)
        if self.id == 19:
            self.test_gear(-1)

    def do_freeze(self, dir):
        if self.id == 25:
            self.test_freeze(dir)

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


        
        
        
