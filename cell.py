import pygame

pygame.init()

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
    15: "mirror",
    16: "diverger",
    17: "redirector", #
    18: "gear_cw",
    19: "gear_ccw",
    20: "ungeneratable",
    21: "repulsor",
    23: "crossgenerator",
    24: "strongenemy",
    25: "freezer",
    26: "cwgenerator", #
    27: "ccwgenerator", #
    28: "advancer", #
    29: "impulsor",
    30: "flipper",
    39: "crossdiverger",
}

cell_cats: list[list[int]] = [
    [],
    [1, 4, 5, 6, 7, 8],
    [2, 14, 28],
    [3, 23, 26, 27],
    [9, 10, 11, 17],
    [21, 29],
    [],
    [12, 13, 24]
]

cell_images_raw: list[tuple[int, pygame.Surface]] = []
for cell_id in cell_names.keys():
    cell_images_raw.append((cell_id, pygame.image.load(f"textures/{cell_names[cell_id]}.png")))

cell_images: dict[int, pygame.Surface] = dict(cell_images_raw)

move_sound = pygame.mixer.Sound("audio/move.ogg")
rot_sound = pygame.mixer.Sound("audio/rotate.ogg")
trash_sound = pygame.mixer.Sound("audio/destroy.ogg")

def get_row(coord: tuple[int, int], dir: int) -> list[tuple[int, int]]:
        from main import cell_map
        dx, dy = get_deltas(dir)
        test: list[int, int] = [coord[0], coord[1]]
        result: list[tuple[int, int]] = []
        while True:
            try:
                temp = cell_map[tuple(test)]
            except KeyError:
                break
            else:
                result.append(tuple(test))
                if temp.get_side((dir+2)%4) in ["trash", "wall", "enemy"]:
                    break
            
            test[0] += dx
            test[1] += dy

        return result

def get_deltas(dir: int) -> tuple[int, int]:
        match dir%4:
            case 0:
                dx: int = 1
                dy: int = 0
            case 1:
                dx: int = 0
                dy: int = 1
            case 2:
                dx: int = -1
                dy: int = 0
            case 3:
                dx: int = 0
                dy: int = -1

        return dx, dy

class Cell(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, id: int, dir: int):
        super().__init__()
        self.tile_x: int = x
        self.tile_y: int = y
        self.id: int | str = id
        self.name = cell_names[self.id]
        self.dir: int = dir
        self.image: pygame.Surface = cell_images[self.id]
        self.rect: pygame.Rect = self.image.get_rect()

        self.frozen: bool = False

        self.left: str = "pushable"
        self.right: str = "pushable"
        self.top: str = "pushable"
        self.bottom: str = "pushable"
        self.hp: int = 1
        self.generation: str = "normal"

        self.pushes = False
        self.pulls = False

        self.push_extended = False
        self.pull_extended = False

        self.suppressed = False

        if self.id == 1:
            self.left = "wall"
            self.right = "wall"
            self.top = "wall"
            self.bottom = "wall"
            self.generation = "ghost"
        if self.id in [2, 28]:
            self.pushes = True
        if self.id in [14, 28]:
            self.pulls = True
        if self.id == 5:
            self.top = "unpushable"
            self.bottom = "unpushable"
        if self.id == 6:
            self.top = "unpushable"
            self.bottom = "unpushable"
            self.right = "unpushable"
        if self.id == 7:
            self.top = "unpushable"
            self.right = "unpushable"
        if self.id == 8:
            self.right = "unpushable"
        if self.id == 20:
            self.generation = "ungeneratable"
        if self.id == 12:
            self.left = "trash"
            self.right = "trash"
            self.top = "trash"
            self.bottom = "trash"
        if self.id in [13, 24]:
            self.left = "enemy"
            self.right = "enemy"
            self.top = "enemy"
            self.bottom = "enemy"
            if self.id == 24:
                self.hp = 2


    def __repr__(self) -> str:
        return f"Cell at {self.tile_x}, {self.tile_y}, id {self.id}, direction {self.dir}"

    def update(self) -> None:
        from main import cam_x, cam_y, TILE_SIZE, cell_map
        self.rect.x = self.tile_x*TILE_SIZE-cam_x
        self.rect.y = self.tile_y*TILE_SIZE-cam_y


    def draw(self) -> None:
        from main import window, TILE_SIZE
        img: pygame.Surface = pygame.transform.rotate(pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE)), -self.dir*90)
        window.blit(img, self.rect)

    def tick(self, dir) -> None:
        self.push_extended = False
        self.pull_extended = False
        if not self.suppressed:
            self.do_gen(dir)
            self.do_rot()
            self.do_redirect()
            self.do_impulse(dir)
            self.do_repulse(dir)
            if self.pulls:
                self.do_pull()
            elif self.pushes:
                self.do_push()

    def set_id(self, id):
        self.id = id
        self.image = cell_images[self.id]


    def get_row(self, dir: int) -> list[tuple[int, int]]:
        from main import cell_map
        dx, dy = get_deltas(dir)
        test: list[int, int] = [self.tile_x, self.tile_y]
        result: list[tuple[int, int]] = []
        while True:
            try:
                temp = cell_map[tuple(test)]
            except KeyError:
                break
            else:
                result.append(tuple(test))
                if temp.get_side((dir+2)%4) in ["trash", "wall", "enemy"]:
                    break
            
            test[0] += dx
            test[1] += dy

        return result
    
    def test_push(self, dir: int, move: bool, hp: int = 1) -> bool:
        from main import cell_map
        dx: int
        dy: int
        dx, dy = get_deltas(dir)
        bias: int = 1
        row: tuple[int, int] = self.get_row(dir)
        trash_flag = False
        suicide_flag = False
        enemy_flag = False
        killer_cell = None
        killer_cell_hp = 0
        for item in row[1:]:
            if cell_map[item].get_side((self.dir+2)%4) == "wall" or cell_map[item].get_side((self.dir+2)%4) == "unpushable":
                return False
            if  "trash" in cell_map[item].get_side((self.dir)%4) :
                trash_flag = True
            if "enemy" in cell_map[item].get_side((self.dir)%4):
                enemy_flag = True
            if (cell_map[item].id, cell_map[item].dir) == (2, dir):
                bias += 1
            if (cell_map[item].id, cell_map[item].dir) == (2, (dir+2)%4):
                bias -= 1

        if bias <= 0:
            return False
        
        if trash_flag:
            killer_cell = row[-1]
            trash_sound.play()
            if cell_map[row[-2]] == self:
                suicide_flag = True
            else:
                del cell_map[row[-2]]
            del row[-2]
            del row[-1]
        if enemy_flag:
            killer_cell = row[-1]
            trash_sound.play()
            if cell_map[row[-2]] == self:
                suicide_flag = True
            else:
                del cell_map[row[-2]]
            killer_cell_hp = cell_map[killer_cell].hp
            cell_map[killer_cell].hp -= hp
            if cell_map[killer_cell].hp <= 0:
                del cell_map[killer_cell]
            elif cell_map[killer_cell].id == 24:
                cell_map[killer_cell].set_id(13)
            del row[-1]
        
        move_sound.play()
        temp: list[Cell] = []
        for item in row[1:]:
            temp.append(cell_map[item])
            del cell_map[item]
        for i, item in enumerate(row[1:]):
            cell_map[(item[0]+dx, item[1]+dy)] = temp[i]
            temp[i].tile_x += dx
            temp[i].tile_y += dy
            
        if move:
            del cell_map[(self.tile_x, self.tile_y)]
            if not suicide_flag:
                cell_map[(self.tile_x+dx, self.tile_y+dy)] = self
                self.tile_x += dx
                self.tile_y += dy

        if killer_cell is not None:
            return hp-killer_cell_hp
        else:
            return hp
    
    def test_pull(self, dir: int, move: bool):
        from main import cell_map
        dx, dy = get_deltas(dir)
        if move:
            row = self.get_row((dir+2)%4)
        else:
            row = get_row((self.tile_x - 2*dx, self.tile_y - 2*dy), (dir+2)%4)
        
        row_cells = [cell_map[item] for item in row]
        if self.pushes or 2 in [cell.id for cell in row_cells]:
            self.test_push(self.dir, False)

        
            
        suicide_flag = False
        enemy_flag = False
        row_interrupt_flag = False
        bias = 1
        if (self.tile_x + dx, self.tile_y + dy) in cell_map.keys():
            if cell_map[(self.tile_x + dx, self.tile_y + dy)].id in [12, 13, 24]:
                killer_cell = (cell_map[(self.tile_x + dx, self.tile_y + dy)].tile_x, cell_map[(self.tile_x + dx, self.tile_y + dy)].tile_y)
                if move:
                    suicide_flag = True
                    if cell_map[killer_cell].id in [13, 24]:
                        enemy_flag = True
            else:
                if move:
                    return False
        for cell in row_cells:
            if (cell.id, cell.dir) == (14, dir):
                bias += 1
            if (cell.id, cell.dir) == (14, (dir+2)%4):
                bias -= 1
            if cell.get_side((self.dir)) in ["enemy", "wall", "unpushable", "trash"]:
                row_interrupt_flag = True
            if cell.id == 2:
                cell.suppressed = True

        if row_interrupt_flag:
            del row[-1]

        if enemy_flag:
            if cell_map[killer_cell].id == 24:
                cell_map[killer_cell].set_id(13)
            else:
                del cell_map[killer_cell]
        if bias <= 0:
            return False
        if move:
            del cell_map[(self.tile_x, self.tile_y)]
            if not suicide_flag:
                cell_map[(self.tile_x+dx, self.tile_y+dy)] = self
                self.tile_x += dx
                self.tile_y += dy
        
        temp = []
        affected_cells = row
        if move:
            if affected_cells:
                del affected_cells[0]
        for item in affected_cells:
            temp.append(cell_map[item])
            del cell_map[item]
        for i, item in enumerate(affected_cells):
            cell_map[(item[0]+dx, item[1]+dy)] = temp[i]
            temp[i].tile_x += dx
            temp[i].tile_y += dy

        return True

    
    def do_push(self):
        if self.pushes:
            self.test_push(self.dir, True)

    def do_repulse(self, dir):
        if self.id == 21:
            self.test_push(dir, False)

    def do_impulse(self, dir):
        if self.id == 29:
            self.test_pull(dir, False)

    def do_pull(self):
        if self.pulls:
            self.test_pull(self.dir, True)
    
    def do_gen(self, dir):
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

    def do_redirect(self):
        if self.id == 17:
            for i in range(4):
                self.test_redirect(self.dir)
    
    def test_rot(self, dir, rot) -> bool:
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
    
    def test_redirect(self, dir):
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
        target_cell.dir = dir
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
        behind_hp = self.test_push(dir, False, behind_cell.hp)
        if behind_cell.generation == "ghost" or not self.test_push(dir, False, behind_cell.hp):
            return False
        # Cells have already been pushed
        # Just create new cells if you have to
        if (self.tile_x + odx, self.tile_y + ody) not in cell_map.keys():
            generated_cell.hp = behind_hp
            if generated_cell.hp == 1 and generated_cell.id == 24:
                generated_cell.set_id(13)
            cell_map[(self.tile_x + odx, self.tile_y + ody)] = generated_cell
            return True
        else:
            return False
    
    def get_side(self, dir) -> str:
        match self.dir:
            case 0:
                return [self.right, self.bottom, self.left, self.top][dir]
            case 1:
                return [self.top, self.right, self.bottom, self.left][dir]
            case 2:
                return [self.left, self.top, self.right, self.bottom][dir]
            case 3:
                return [self.bottom, self.left, self.top, self.right][dir]

        


        
        
        
