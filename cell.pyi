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

class Cell: ...