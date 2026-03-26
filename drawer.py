from dataclasses import dataclass, field
from typing import Tuple
import pygame

def make_checkerboard(img_path1: str, img_path2: str, tiles_x: int, tiles_y: int) -> pygame.Surface:

    img1 = pygame.image.load(img_path1).convert_alpha()
    img2 = pygame.image.load(img_path2).convert_alpha()

    w1, h1 = img1.get_size()
    w2, h2 = img2.get_size()

    if (w1, h1) != (w2, h2):
        raise ValueError("Both tile images must be the same size")

    tile_w, tile_h = w1, h1

    surface = pygame.Surface((tiles_x * tile_w, tiles_y * tile_h), pygame.SRCALPHA)

    for y in range(tiles_y):
        for x in range(tiles_x):
            tile = img1 if ((x + y) % 2 == 0) else img2
            surface.blit(tile, (x * tile_w, y * tile_h))

    return surface

@dataclass
class Drawer:
    screen: pygame.Surface
    x: int
    y: int
    width: int
    height: int
    board_texture: pygame.Surface = field(default_factory=lambda : make_checkerboard("resources/imgs/dark.png","resources/imgs/light.png",tiles_x=10,tiles_y=10), init = False)

    @property
    def coordinates(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @coordinates.setter
    def coordinates(self, value: Tuple[int, int]) -> None:
        self.x, self.y = value
    
    @property
    def rect(self) -> Tuple[int, int]:
        return (self.width, self.height)

    @rect.setter
    def coordinates(self, value: Tuple[int, int]) -> None:
        self.width, self.height = value
    
    def draw(self, board_state : List[List[BoardSpace]]) -> None:
        scaled = pygame.transform.smoothscale(surface=self.board_texture, self.rect)
        screen.blit(scaled, self.coordinates)








pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

checker = 

# Desired on‑screen size
DISPLAY_SIZE = 600

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((40, 40, 40))

    # Scale the checkerboard to 600×600 for display
    scaled = pygame.transform.smoothscale(surface=checker, (DISPLAY_SIZE, DISPLAY_SIZE))

    # Center it on the screen
    x = (800 - DISPLAY_SIZE) // 2
    y = (800 - DISPLAY_SIZE) // 2

    screen.blit(scaled, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

