from typing import List, Tuple, Set, Optional
from gameSettings import GameSettings as _GameSettings
from enum import Enum
from copy import deepcopy


class BoardSpace(Enum):
    WHITE = 1
    BLACK = 2
    EMPTY = 3


class Group:
    def __init__(
        self,
        colour: BoardSpace,
        members: List[Tuple[int, int]]
    ) -> None:

        self.colour: BoardSpace = colour
        self.members: List[Tuple[int, int]] = members


class Board:
    def __init__(
        self,
        settings: _GameSettings,
        premade_board_pos: Optional[List[List[BoardSpace]]] = None
    ) -> None:

        self.settings: _GameSettings = settings

        self.board_tiles: List[List[BoardSpace]]

        self.previous_board_state: List[List[BoardSpace]]

        self.white_captures = 0
        self.black_captures = 0

        if premade_board_pos is None:
            premade_board_pos = []

        if len(premade_board_pos) != self.settings.board_size:

            self.board_tiles = self.__populate_board_tiles()

            print("standardbræt oprettet")

        else:
            success: bool = True

            for row in premade_board_pos:

                if len(row) != self.settings.board_size:
                    success = False
                    break

            if success:

                self.board_tiles = deepcopy(premade_board_pos)

                print("Specielt bræt oprettet")

            else:

                self.board_tiles = self.__populate_board_tiles()

                print(
                    "Bræt givet af forkert størrelse "
                    "| Standardbræt oprettet"
                )

        self.previous_board_state = deepcopy(self.board_tiles)


    def __populate_board_tiles(self) -> List[List[BoardSpace]]:

        columns: List[List[BoardSpace]] = []

        for _ in range(self.settings.board_size):

            row: List[BoardSpace] = []

            for _ in range(self.settings.board_size):
                row.append(BoardSpace.EMPTY)

            columns.append(row)

        return columns

    def __out_of_bounds(
        self,
        x: int,
        y: int
    ) -> bool:

        if x < 0 or x >= self.settings.board_size:
            return True

        if y < 0 or y >= self.settings.board_size:
            return True

        return False

    def __get_adjacent_positions(
        self,
        x: int,
        y: int
    ) -> List[Tuple[int, int]]:

        positions: List[Tuple[int, int]] = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]

        valid_positions: List[Tuple[int, int]] = []

        for px, py in positions:

            if not self.__out_of_bounds(px, py):
                valid_positions.append((px, py))

        return valid_positions

    def __get_group(
        self,
        x: int,
        y: int
    ) -> Group:

        colour: BoardSpace = self.board_tiles[x][y]

        visited: Set[Tuple[int, int]] = set()

        stack: List[Tuple[int, int]] = [(x, y)]

        while len(stack) > 0:

            cx: int
            cy: int

            cx, cy = stack.pop()

            if (cx, cy) in visited:
                continue

            visited.add((cx, cy))

            neighbours: List[Tuple[int, int]]
            neighbours = self.__get_adjacent_positions(cx, cy)

            for nx, ny in neighbours:

                if self.board_tiles[nx][ny] == colour:
                    stack.append((nx, ny))

        return Group(colour, list(visited))

    def __group_has_liberties(
        self,
        group: Group
    ) -> bool:

        for x, y in group.members:

            neighbours: List[Tuple[int, int]]
            neighbours = self.__get_adjacent_positions(x, y)

            for nx, ny in neighbours:

                if self.board_tiles[nx][ny] == BoardSpace.EMPTY:
                    return True

        return False

    def __remove_group(
        self,
        group: Group
    ) -> None:
        if group.colour == BoardSpace.WHITE:
            self.black_captures += len(group.members)
        else:
            self.white_captures += len(group.members)
        for x, y in group.members:
            self.board_tiles[x][y] = BoardSpace.EMPTY

    def __board_equals(
        self,
        board_a: List[List[BoardSpace]],
        board_b: List[List[BoardSpace]]
    ) -> bool:

        for x in range(self.settings.board_size):

            for y in range(self.settings.board_size):

                if board_a[x][y] != board_b[x][y]:
                    return False

        return True

    def __get_opposite_colour(
        self,
        stone: BoardSpace
    ) -> BoardSpace:

        if stone == BoardSpace.BLACK:
            return BoardSpace.WHITE

        if stone == BoardSpace.WHITE:
            return BoardSpace.BLACK

        return BoardSpace.EMPTY

    def place_stone(
        self,
        x: int,
        y: int,
        stone: BoardSpace
    ) -> bool:

        # Move must be inside the board.
        if self.__out_of_bounds(x, y):
            return False

        # Position must be empty.
        if self.board_tiles[x][y] != BoardSpace.EMPTY:
            return False

        # Save old board for undo (not implemented) and ko check.
        old_board: List[List[BoardSpace]]
        old_board = deepcopy(self.board_tiles)

        # Place stone temporarily.
        self.board_tiles[x][y] = stone

        opponent_colour: BoardSpace
        opponent_colour = self.__get_opposite_colour(stone)

        checked_positions: Set[Tuple[int, int]] = set()

        neighbours: List[Tuple[int, int]]
        neighbours = self.__get_adjacent_positions(x, y)

        # Check neighbouring enemy groups.
        for nx, ny in neighbours:

            if self.board_tiles[nx][ny] != opponent_colour:
                continue

            if (nx, ny) in checked_positions:
                continue

            enemy_group: Group
            enemy_group = self.__get_group(nx, ny)

            for member in enemy_group.members:
                checked_positions.add(member)

            # Capture enemy group if no liberties remain.
            if not self.__group_has_liberties(enemy_group):
                self.__remove_group(enemy_group)

        # Suicide check.
        own_group: Group
        own_group = self.__get_group(x, y)

        if not self.__group_has_liberties(own_group):

            self.board_tiles = old_board

            return False

        # Ko check.
        if self.__board_equals(
            self.board_tiles,
            self.previous_board_state
        ):

            self.board_tiles = old_board

            return False

        # Legal move.
        self.previous_board_state = old_board

        return True

    def remove_stone(
        self,
        x: int,
        y: int
    ) -> bool:

        if self.__out_of_bounds(x, y):
            return False

        self.board_tiles[x][y] = BoardSpace.EMPTY

        return True

    def print_board(self) -> None:

        symbols: dict[BoardSpace, str] = {
            BoardSpace.BLACK: "B",
            BoardSpace.WHITE: "W",
            BoardSpace.EMPTY: "."
        }

        for y in range(self.settings.board_size):

            row: str = ""

            for x in range(self.settings.board_size):

                row += symbols[self.board_tiles[x][y]]
                row += " "

            print(row)

        print()

def calculate_score(
    original_board: Board,
    territory_board: Board
) -> Tuple[int, int]:

    black_score: int = 0

    white_score: int = 0

    x: int
    y: int

    for x in range(original_board.settings.board_size):

        for y in range(original_board.settings.board_size):

            original_space: BoardSpace = (
                original_board.board_tiles[x][y]
            )

            territory_space: BoardSpace = (
                territory_board.board_tiles[x][y]
            )

            # Ignore spaces already occupied by stones.
            # We only count territory.
            if original_space != BoardSpace.EMPTY:
                continue

            if territory_space == BoardSpace.BLACK:
                black_score += 1

            elif territory_space == BoardSpace.WHITE:
                white_score += 1

    white_score += original_board.white_captures
    black_score += original_board.black_captures

    return (black_score, white_score)



specielt_bræt: List[List[BoardSpace]] = [
    [
        BoardSpace.BLACK,
        BoardSpace.BLACK,
        BoardSpace.BLACK,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY
    ],
    [
        BoardSpace.EMPTY,
        BoardSpace.BLACK,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY
    ],
    [
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY
    ],
    [
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY
    ],
    [
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY,
        BoardSpace.EMPTY
    ]
]


if __name__ == "__main__":

    size: _GameSettings = _GameSettings(5)

    board: Board = Board(size)

    board.place_stone(1, 0, BoardSpace.BLACK)
    board.place_stone(0, 1, BoardSpace.BLACK)
    board.place_stone(2, 1, BoardSpace.BLACK)
    board.place_stone(1, 2, BoardSpace.BLACK)

    board.place_stone(1, 1, BoardSpace.WHITE)

    board.print_board()