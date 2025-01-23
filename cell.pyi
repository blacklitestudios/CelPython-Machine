import pygame
#from math import atan2, pi

cell_names: dict[int|str, str]
cell_cats_new: list[list[list[int|str]]]
flip_guide: list[list[int]] 

def resource_path(relative_path: str) -> str: ...

cell_images_new: list[tuple[int | str, pygame.Surface]]
cell_id: int | str
cell_images: dict[int | str, pygame.Surface]

move_sound: pygame.mixer.Sound
rot_sound: pygame.mixer.Sound
trash_sound: pygame.mixer.Sound

def lerp(a: float, b: float, factor: float) -> float: ...

def get_row(coord: tuple[int, int], dir: int, force_type: int = 0) -> tuple[list[tuple[int, int, int, tuple[int, int], int]], list[tuple[int, int]], list[int], bool]: ...

def get_cell_id(cell_name: str) -> int: ...

class Cell: 
    tile_x: int
    tile_y: int
    old_x: int
    old_y: int
    old_dir: int
    id: int|str
    name: str
    dir: int
    actual_dir: int
    img_cache: dict[int, pygame.Surface]
    chirality: list[int]
    delta_dir: int
    die_flag: bool

    image: pygame.Surface
    rect: pygame.Rect
    frozen: bool
    protected: bool


    def __init__(self: Cell, x: int, y: int, id: int|str, dir: int) -> None: ...
    def __repr__(self: Cell) -> str: ...
    def copy(self: Cell) -> Cell: ...
    def update(self: Cell) -> None: ...
    def draw(self: Cell) -> None: ...
    def loadscale(self: Cell, size: int) -> pygame.Surface: ...
    def on_force(self: Cell, dir: int, origin: Cell, suppress: bool, force_type: int) -> None: ...
    def set_id(self, id: int|str) -> None: ...
    def mexican_standoff(self, cell: Cell) -> bool: ...
    def push(self, dir: int, move: bool, hp: int = 1, force: int = 0, speed: int = 1, test: bool = False, active: bool=True) -> bool | int: ...
    def pull(self, dir: int, move: bool, force: int = 0, test: bool = False) -> bool: ...
    def test_swap(self, dx1, dy1, dx2, dy2) -> bool: ...
    def test_rot(self, dir: int, rot: int) -> bool: ...
    def test_redirect(self, dir: int, rot: int) -> bool: ...
    def redirect(self, dir) -> bool: ...
    def gen(self, dir, cell: Cell) -> Cell: ...
    def check_generation(self): ...
    def test_gen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False) -> bool: ...
    def test_supergen(self, dir: int, angle: int, twist: bool = False, clone: bool = False, suppress: bool = False) -> bool: ...
    def test_replicate(self, dir: int) -> bool: ...
    def test_gear(self, rot: int) -> bool: ...
    def test_freeze(self, dir: int) -> bool: ...
    def test_protect(self, dx: int, dy: int) -> bool: ...
    def test_intake(self, dir: int): ...
    def rot(self, rot: int): ...
    def flip(self, rot: int): ...
    def test_flip(self, dir: int, rot: int) ->  bool: ...
    def do_push(self, dir: int): ...
    def do_repulse(self, dir: int): ...
    def do_super_repulse(self, dir: int): ...
    def do_impulse(self, dir: int): ...
    def do_grapulse(self, dir: int): ...
    def do_pull(self, dir): ...
    def drill(self, dir, test: bool = False): ...
    def do_drill(self, dir): ...
    def do_gen(self, dir: int): ...
    def do_super_gen(self, dir: int): ...
    def do_gate(self, dir: int): ...
    def do_replicate(self, dir: int): ...
    def do_intake(self, dir: int): ...
    def do_rot(self): ...
    def do_flip(self): ...
    def do_mirror(self, dir1, dir2): ...
    def do_redirect(self): ...
    def do_gear(self, dir): ...
    def do_freeze(self, dir): ...
    def do_protect(self): ...
    def get_side(self, dir: int) -> str: ...
    def get_side_by_delta(self, dx, dy): ...
    def cw_grab(self, dir: int, move: bool, hp: int = 1, force: int = 1, speed: int = 1) -> bool | int: ...
    def get_cw_grab_bias(self, dir, force=0, times=-1): ...
    def get_ccw_grab_bias(self, dir, force=0, times=-1): ...
    def ccw_grab(self, dir: int, move: bool, hp: int = 1, force: int = 1, speed: int = 1) -> bool | int: ...
    def grab(self, dir: int, move: bool, force: int = 0, test: bool = False) -> bool: ...
    def nudge(self, dir: int, move: bool, force: int = 0, hp: int = 1, active=True, is_grab=False): ...
    def do_grab(self, dir): ...
    def do_nudge(self, dir): ...
    def check_hp(self): ...

