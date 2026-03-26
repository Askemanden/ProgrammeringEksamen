from dataclasses import dataclass, field
from typing import Tuple, List
import pygame
from Board import BoardSpace

def _make_checkerboard(img_path1: str, img_path2: str, tiles_x: int, tiles_y: int) -> pygame.Surface:

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
    stone_scale: float
    board_width: int
    board_height: int
    board_texture: pygame.Surface = field(init = False)
    white_stone: pygame.Surface = field(default_factory=lambda: pygame.image.load("resources/imgs/black.png").convert_alpha(), init=False)
    black_stone: pygame.Surface = field(default_factory=lambda: pygame.image.load("resources/imgs/white.png").convert_alpha(), init=False)

    def __post_init__(self):
        self.board_texture = _make_checkerboard(
            "resources/imgs/dark.png",
            "resources/imgs/light.png",
            self.board_width,
            self.board_height
            )
    
    @property
    def rect(self) -> Tuple[int, int]:
        return (self.board_width, self.board_height)

    @rect.setter
    def rect(self, value: Tuple[int, int]) -> None:
        self.board_width, self.board_height = value
    
    def draw(self, board_state: List[List[BoardSpace]], rect: Tuple[int,int], pos: Tuple[int,int], screen: pygame.Surface) -> None:
        width,height = rect
        if len(board_state) != self.board_height:
            print("board_state not correct height")
            return
        if len(board_state[0]) != self.board_width:
            print("board_state not correct width")
            return

        temp_surface = pygame.Surface(self.board_texture.get_size(), pygame.SRCALPHA)

        temp_surface.blit(self.board_texture, (0,0))

        tile_w = self.board_texture.get_width() // self.board_width
        tile_h = self.board_texture.get_height() // self.board_height

        stone_black = pygame.transform.smoothscale(self.black_stone, (tile_w*self.stone_scale, tile_h*self.stone_scale))
        stone_white = pygame.transform.smoothscale(self.white_stone, (tile_w*self.stone_scale, tile_h*self.stone_scale))

        for row in range(self.board_height):
            for col in range(self.board_width):
                space = board_state[row][col]

                if space == BoardSpace.EMPTY:
                    continue

                px = col * tile_w
                py = row * tile_h

                if space == BoardSpace.BLACK:
                    temp_surface.blit(stone_black, (px + (tile_w - tile_w*self.stone_scale)/2, py + (tile_h - tile_h*self.stone_scale)/2))
                elif space == BoardSpace.WHITE:
                    temp_surface.blit(stone_white, (px + (tile_w - tile_w*self.stone_scale)/2, py + (tile_h - tile_h*self.stone_scale)/2))

        scaled = pygame.transform.smoothscale(temp_surface, (width, height))

        screen.blit(scaled, pos)


if __name__ == "__main__":
    import pygame
    from Board import BoardSpace

    pygame.init()

    # Create window
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    # Create a Drawer at position (100, 100)
    drawer = Drawer(
        stone_scale=0.9,
        board_width=9,      # number of tiles horizontally
        board_height=9      # number of tiles vertically
    )

    # Example 9×9 board with some stones
    board_state = [
        [BoardSpace.EMPTY] *9 for _ in range(9)
    ]

    # Place a few stones for testing
    board_state[0][0] = BoardSpace.BLACK
    board_state[0][1] = BoardSpace.WHITE
    board_state[4][4] = BoardSpace.BLACK
    board_state[8][8] = BoardSpace.WHITE

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        # Draw board + stones
        drawer.draw(board_state, (500,500),(50,50), screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
