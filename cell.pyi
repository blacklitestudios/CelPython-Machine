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

