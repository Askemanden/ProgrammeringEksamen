from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Optional, Set, List
import pygame
from Board import BoardSpace, Board



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
    rect: Tuple[int, int]
    pos: Tuple[int, int]

    stone_scale: float = 1
    territory_indicator_scale: float = 0.6
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

    def board_to_global(self, row: int, col: int) -> Tuple[float, float]:
        """
        Convert board coordinates (row, column) to global screen coordinates for stone drawing.
        Returns the top-left position for blitting the stone image on screen.
        """
        rect = self.rect
        pos = self.pos
        out_w, out_h = rect
        tex_w = self.board_texture.get_width()
        tex_h = self.board_texture.get_height()
        scale_x = out_w / tex_w
        scale_y = out_h / tex_h

        # Stone size in native space
        stone_w = self.cell_w * self.stone_scale
        stone_h = self.cell_h * self.stone_scale
        line_offset = self.line_thickness / 2
        px = self.first_x + col * self.cell_w + line_offset
        py = self.first_y + row * self.cell_h + line_offset
        native_draw_x = px - stone_w / 2
        native_draw_y = py - stone_h / 2

        # Scale to screen coordinates
        screen_draw_x = native_draw_x * scale_x + pos[0]
        screen_draw_y = native_draw_y * scale_y + pos[1]
        return screen_draw_x, screen_draw_y

    def global_to_board(self, x_global: float, y_global: float) -> Tuple[int, int]:
        """
        Convert global screen coordinates (top-left of stone) to board coordinates (row, col).
        Returns the nearest board position.
        """
        rect = self.rect
        pos = self.pos
        out_w, out_h = rect
        tex_w = self.board_texture.get_width()
        tex_h = self.board_texture.get_height()
        scale_x = out_w / tex_w
        scale_y = out_h / tex_h

        # Unscale to native coordinates
        native_x = (x_global - pos[0]) / scale_x
        native_y = (y_global - pos[1]) / scale_y

        # Adjust for stone center
        px = native_x
        py = native_y
        line_offset = self.line_thickness / 2
        col = round((px - self.first_x - line_offset) / self.cell_w)
        row = round((py - self.first_y - line_offset) / self.cell_h)
        return row, col

    def board_to_global_scaled(
        self,
        row: int,
        col: int,
        scale: float
    ) -> Tuple[float, float]:
        rect = self.rect
        pos = self.pos
        out_w, out_h = rect
        tex_w = self.board_texture.get_width()
        tex_h = self.board_texture.get_height()
        scale_x = out_w / tex_w
        scale_y = out_h / tex_h

        stone_w = self.cell_w * scale
        stone_h = self.cell_h * scale
        line_offset = self.line_thickness / 2
        px = self.first_x + col * self.cell_w + line_offset
        py = self.first_y + row * self.cell_h + line_offset
        native_draw_x = px - stone_w / 2
        native_draw_y = py - stone_h / 2

        screen_draw_x = native_draw_x * scale_x + pos[0]
        screen_draw_y = native_draw_y * scale_y + pos[1]
        return screen_draw_x, screen_draw_y

    def draw(
        self,
        board: Board,
        screen: pygame.Surface,
        hover_coords: Tuple[int,int],
        hover_color: BoardSpace,
        territory_indicator: Optional[Board] = None
    ) -> None:
        rect = self.rect
        pos = self.pos
        board_state = board.board_tiles
        out_w, out_h = rect
        territory_state = territory_indicator.board_tiles if territory_indicator is not None else None

        # Draw the scaled board background
        scaled_board = pygame.transform.smoothscale(self.board_texture, (out_w, out_h))
        screen.blit(scaled_board, pos)

        # Compute scaling factors
        tex_w = self.board_texture.get_width()
        tex_h = self.board_texture.get_height()
        scale_x = out_w / tex_w
        scale_y = out_h / tex_h

        # Stone sizes in screen space
        stone_w_native = self.cell_w * self.stone_scale
        stone_h_native = self.cell_h * self.stone_scale
        stone_w_screen = stone_w_native * scale_x
        stone_h_screen = stone_h_native * scale_y

        # Scale stone images
        stone_black_screen = pygame.transform.smoothscale(self.black_stone, (int(stone_w_screen), int(stone_h_screen)))
        stone_white_screen = pygame.transform.smoothscale(self.white_stone, (int(stone_w_screen), int(stone_h_screen)))

        # Draw stones
        for row in range(self.board_height):
            for col in range(self.board_width):
                space = board_state[row][col]
                if space == BoardSpace.EMPTY:
                    continue

                screen_draw_x, screen_draw_y = self.board_to_global(row, col)

                if space == BoardSpace.BLACK:
                    screen.blit(stone_black_screen, (screen_draw_x, screen_draw_y))
                else:
                    screen.blit(stone_white_screen, (screen_draw_x, screen_draw_y))

        # Draw territory indicator stones on top of the board stones
        if territory_state is not None:
            territory_stone_w_native = self.cell_w * self.territory_indicator_scale
            territory_stone_h_native = self.cell_h * self.territory_indicator_scale
            territory_stone_w_screen = territory_stone_w_native * scale_x
            territory_stone_h_screen = territory_stone_h_native * scale_y

            territory_black_screen = pygame.transform.smoothscale(
                self.black_stone, (int(territory_stone_w_screen), int(territory_stone_h_screen))
            )
            territory_white_screen = pygame.transform.smoothscale(
                self.white_stone, (int(territory_stone_w_screen), int(territory_stone_h_screen))
            )

            for row in range(self.board_height):
                for col in range(self.board_width):
                    space = territory_state[row][col]
                    if space == BoardSpace.EMPTY:
                        continue

                    screen_draw_x, screen_draw_y = self.board_to_global_scaled(row, col, self.territory_indicator_scale)

                    if space == BoardSpace.BLACK:
                        indicator_stone = territory_black_screen.copy()
                    else:
                        indicator_stone = territory_white_screen.copy()

                    screen.blit(indicator_stone, (screen_draw_x, screen_draw_y))

        # Draw hover stone if color is not EMPTY
        if hover_color != BoardSpace.EMPTY:
            hover_row, hover_col = hover_coords
            board_x, board_y = self.global_to_board(hover_row, hover_col)
            
            # Check if board coordinates are within bounds
            if 0 <= board_x < self.board_height and 0 <= board_y < self.board_width:
                if board.board_tiles[board_x][board_y] == BoardSpace.EMPTY:
                    screen_draw_x, screen_draw_y = self.board_to_global(board_x, board_y)
                    
                    # Create semi-transparent stone
                    if hover_color == BoardSpace.BLACK:
                        hover_stone = stone_black_screen.copy()
                    else:
                        hover_stone = stone_white_screen.copy()

                    hover_stone.set_alpha(200)
                    screen.blit(hover_stone, (screen_draw_x, screen_draw_y))
        



if __name__ == "__main__":
    from gameSettings import GameSettings
    import random
    from bouzy import BouzyAlgorithm
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Board Test")

    s = 19
    board = Board(GameSettings(s))

    occupied: Set[Tuple[int, int]] = {(4, 5), (7, 5), (10, 10), (11, 10)}


    def place_random_spread(
        color: BoardSpace,
        count: int = 8,
        min_distance: int = 3
    ) -> None:
        candidates = [
            (x, y)
            for x in range(s)
            for y in range(s)
            if (x, y) not in occupied
        ]
        random.shuffle(candidates)

        placed = 0

        for x, y in candidates:
            if placed >= count:
                break

            if all(
                abs(x - ox) + abs(y - oy) >= min_distance
                for ox, oy in occupied
            ):
                board.place_stone(x, y, color)
                occupied.add((x, y))
                placed += 1

    place_random_spread(BoardSpace.BLACK, count=20)
    place_random_spread(BoardSpace.WHITE, count=20)

    values: List[List[int]] = (
        BouzyAlgorithm.evaluate_values(
            board,
            dilations=4
        )
    )

    territory_board: Board = (
        BouzyAlgorithm.evaluate_territory_board(
            board=board,
            dilations=21,
            erosions=5
        )
    )

    drawer = Drawer(
        board_width=s,
        board_height=s,
        rect=(WIDTH - 40, HEIGHT - 40),
        pos=(20, 20),
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
            screen=screen,
            hover_coords=(0,0),
            hover_color=BoardSpace.EMPTY,
            territory_indicator=territory_board
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
