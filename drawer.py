from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple
import pygame
from board import BoardSpace, Board



def _make_goboard(
    img_path: str,
    tiles_x: int,
    tiles_y: int,
    margin: int
) -> Tuple[pygame.Surface, float, float, float, float, int]:
    """
    Create a Go board texture using a wood background and straight black grid lines.
    Returns:
        (surface, first_x, first_y, cell_w, cell_h, line_thickness)
    """

    wood = pygame.image.load(img_path).convert_alpha()
    width, height = wood.get_size()

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.blit(wood, (0, 0))

    first_x = float(margin)
    first_y = float(margin)

    inner_w = width - 2 * margin
    inner_h = height - 2 * margin

    cell_w = inner_w / (tiles_x - 1)
    cell_h = inner_h / (tiles_y - 1)

    line_color = (0, 0, 0)
    line_thickness = 2

    # Vertical lines
    for x in range(tiles_x):
        px = int(first_x + x * cell_w)
        pygame.draw.line(surface, line_color, (px, first_y), (px, height - first_y), line_thickness)

    # Horizontal lines
    for y in range(tiles_y):
        py = int(first_y + y * cell_h)
        pygame.draw.line(surface, line_color, (first_x, py), (width - first_x, py), line_thickness)

    return surface, first_x, first_y, cell_w, cell_h, line_thickness

@dataclass
class Drawer:
    board_width: int
    board_height: int
    stone_scale: float = 1
    margin: int = 40

    board_texture: pygame.Surface = field(init=False)
    first_x: float = field(init=False)
    first_y: float = field(init=False)
    cell_w: float = field(init=False)
    cell_h: float = field(init=False)
    line_thickness: int = field(init=False)

    white_stone: pygame.Surface = field(
        default_factory=lambda: pygame.image.load("resources/imgs/white.png").convert_alpha(),
        init=False
    )
    black_stone: pygame.Surface = field(
        default_factory=lambda: pygame.image.load("resources/imgs/black.png").convert_alpha(),
        init=False
    )

    def __post_init__(self) -> None:
        (self.board_texture,
         self.first_x,
         self.first_y,
         self.cell_w,
         self.cell_h,
         self.line_thickness) = _make_goboard(
            "resources/imgs/wood.png",
            self.board_width,
            self.board_height,
            self.margin
        )

    @property
    def rect(self) -> Tuple[int, int]:
        return (self.board_width, self.board_height)

    def board_to_global(self, row: int, col: int) -> Tuple[float, float]:
        """
        Convert board coordinates (row, col) to global screen coordinates.
        """
        line_offset = self.line_thickness / 2
        x_global = self.first_x + col * self.cell_w + line_offset
        y_global = self.first_y + row * self.cell_h + line_offset
        return x_global, y_global

    def global_to_board(self, x_global: float, y_global: float) -> Tuple[int, int]:
        """
        Convert global screen coordinates to board coordinates (row, col).
        Returns the nearest board position.
        """
        line_offset = self.line_thickness / 2
        col = round((x_global - self.first_x - line_offset) / self.cell_w)
        row = round((y_global - self.first_y - line_offset) / self.cell_h)
        return row, col

    def draw(
        self,
        board: Board,
        rect: Tuple[int, int],
        pos: Tuple[int, int],
        screen: pygame.Surface
    ) -> None:

        board_state = board.board_tiles
        out_w, out_h = rect

        tex_w = self.board_texture.get_width()
        tex_h = self.board_texture.get_height()

        temp_surface = pygame.Surface((tex_w, tex_h), pygame.SRCALPHA)
        temp_surface.blit(self.board_texture, (0, 0))

        # Stone size in native space
        stone_w = int(self.cell_w * self.stone_scale)
        stone_h = int(self.cell_h * self.stone_scale)

        stone_black = pygame.transform.smoothscale(self.black_stone, (stone_w, stone_h))
        stone_white = pygame.transform.smoothscale(self.white_stone, (stone_w, stone_h))

        # Draw stones
        for row in range(self.board_height):
            for col in range(self.board_width):
                space = board_state[row][col]
                if space == BoardSpace.EMPTY:
                    continue

                px, py = self.board_to_global(row, col)

                draw_x = px - stone_w / 2
                draw_y = py - stone_h / 2

                if space == BoardSpace.BLACK:
                    temp_surface.blit(stone_black, (draw_x, draw_y))
                else:
                    temp_surface.blit(stone_white, (draw_x, draw_y))

        scaled = pygame.transform.smoothscale(temp_surface, (out_w, out_h))
        screen.blit(scaled, pos)



if __name__ == "__main__":
    from gameSettings import GameSettings
    import random
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Board Test")

    s = 19
    board = Board(GameSettings(s))

    for i in range(s):
        for j in range(s):
            board.board_tiles[i][j] = random.choice([BoardSpace.BLACK,BoardSpace.WHITE])

    drawer = Drawer(
        board_width=s,
        board_height=s
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((50, 50, 50))

        drawer.draw(
            board=board,
            rect=(WIDTH - 40, HEIGHT - 40),
            pos=(20, 20),
            screen=screen
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
