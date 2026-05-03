from typing import Final, List, Optional, Set, Tuple
from copy import deepcopy

from Board import Board, BoardSpace
from gameSettings import GameSettings
import random


class BouzyAlgorithm:
    """
    Implementation of Bruno Bouzy's territory recognition algorithm.
    Based on https://helios2.mi.parisdescartes.fr/~bouzy/publications/MyBouzy-IJPRAI.pdf
    """

    BLACK_VALUE: Final[int] = 64
    WHITE_VALUE: Final[int] = -64

    @staticmethod
    def evaluate_values(
        board: Board,
        dilations: int = 5,
        erosions: Optional[int] = None
    ) -> List[List[int]]:
        """
        Run the Bouzy algorithm and return evaluated values.
        """

        if erosions is None:
            erosions = dilations * (dilations - 1) + 1

        values: List[List[int]] = (
            BouzyAlgorithm.__initialize_values(board)
        )

        for _ in range(dilations):
            values = BouzyAlgorithm.__dilate_z(values)

        for _ in range(erosions):
            values = BouzyAlgorithm.__erase_z(values)

        return values

    @staticmethod
    def evaluate_territory_board(
        board: Board,
        dilations: int = 5,
        erosions: Optional[int] = None
    ) -> Board:
        """
        Return a new board containing evaluated territories.
        """

        values: List[List[int]] = (
            BouzyAlgorithm.evaluate_values(
                board,
                dilations,
                erosions
            )
        )

        territory_board: Board = deepcopy(board)

        size: int = board.settings.board_size

        for x in range(size):
            for y in range(size):

                if board.board_tiles[x][y] != BoardSpace.EMPTY:
                    continue

                value: int = values[x][y]

                if value > 0:
                    territory_board.board_tiles[x][y] = (
                        BoardSpace.BLACK
                    )

                elif value < 0:
                    territory_board.board_tiles[x][y] = (
                        BoardSpace.WHITE
                    )

                else:
                    territory_board.board_tiles[x][y] = (
                        BoardSpace.EMPTY
                    )

        return territory_board

    @staticmethod
    def print_values(values: List[List[int]]) -> None:
        """
        Print Bouzy numerical values.
        """

        size: int = len(values)

        for y in range(size):

            row: List[str] = []

            for x in range(size):

                value: int = values[x][y]

                if value >= 0:
                    row.append(f"+{value:02}")

                else:
                    row.append(f"{value:03}")

            print(" ".join(row))

    @staticmethod
    def __initialize_values(board: Board) -> List[List[int]]:
        """
        Convert board state into Bouzy values.
        """

        size: int = board.settings.board_size

        values: List[List[int]] = []

        for x in range(size):

            column: List[int] = []

            for y in range(size):

                tile: BoardSpace = board.board_tiles[x][y]

                if tile == BoardSpace.BLACK:
                    column.append(BouzyAlgorithm.BLACK_VALUE)

                elif tile == BoardSpace.WHITE:
                    column.append(BouzyAlgorithm.WHITE_VALUE)

                else:
                    column.append(0)

            values.append(column)

        return values

    @staticmethod
    def __dilate_z(values: List[List[int]]) -> List[List[int]]:
        """
        Perform one Bouzy dilation step.
        """

        size: int = len(values)

        result: List[List[int]] = deepcopy(values)

        for x in range(size):
            for y in range(size):

                current: int = values[x][y]

                neighbours: List[int] = (
                    BouzyAlgorithm.__get_neighbour_values(
                        values,
                        x,
                        y
                    )
                )

                neighbour_signs: Set[int] = set()

                for neighbour in neighbours:

                    if neighbour > 0:
                        neighbour_signs.add(1)

                    elif neighbour < 0:
                        neighbour_signs.add(-1)

                if len(neighbour_signs) > 1:
                    continue

                if len(neighbour_signs) == 0:
                    continue

                sign: int = neighbour_signs.pop()

                if current != 0:

                    if (
                        (current > 0 and sign < 0)
                        or
                        (current < 0 and sign > 0)
                    ):
                        continue

                supporting_neighbours: int = 0

                for neighbour in neighbours:

                    if sign > 0 and neighbour > 0:
                        supporting_neighbours += 1

                    elif sign < 0 and neighbour < 0:
                        supporting_neighbours += 1

                if current == 0:

                    result[x][y] = BouzyAlgorithm.__clamp(
                        supporting_neighbours
                        if sign > 0
                        else -supporting_neighbours
                    )

                else:

                    magnitude: int = (
                        abs(current)
                        + supporting_neighbours
                    )
                    result[x][y] = BouzyAlgorithm.__clamp(
                        magnitude
                        if current > 0
                        else -magnitude
                    )

        return result

    @staticmethod
    def __erase_z(values: List[List[int]]) -> List[List[int]]:
        """
        Perform one Bouzy erosion step.
        """

        size: int = len(values)

        result: List[List[int]] = deepcopy(values)

        for x in range(size):
            for y in range(size):

                current: int = values[x][y]

                if current == 0:
                    continue

                sign: int = 1 if current > 0 else -1

                magnitude: int = abs(current)

                neighbours: List[int] = (
                    BouzyAlgorithm.__get_neighbour_values(
                        values,
                        x,
                        y
                    )
                )

                erosion: int = 0

                for neighbour in neighbours:

                    if neighbour == 0:
                        erosion += 1
                        continue

                    neighbour_sign: int = (
                        1 if neighbour > 0 else -1
                    )

                    if neighbour_sign != sign:
                        erosion += 1

                magnitude -= erosion

                if magnitude <= 0:
                    result[x][y] = 0

                else:

                    result[x][y] = BouzyAlgorithm.__clamp(
                        magnitude
                        if current > 0
                        else -magnitude
                    )

        return result

    @staticmethod
    def __get_neighbour_values(
        values: List[List[int]],
        x: int,
        y: int
    ) -> List[int]:
        """
        Get orthogonal neighbour values.
        """

        size: int = len(values)

        neighbours: List[int] = []

        directions: List[Tuple[int, int]] = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dx, dy in directions:

            nx: int = x + dx
            ny: int = y + dy

            if 0 <= nx < size and 0 <= ny < size:
                neighbours.append(values[nx][ny])

        return neighbours
    
    @staticmethod
    def __clamp(value: int) -> int:
        """
        Clamp Bouzy values to the valid range.
        """

        if value > 64:
            return 64

        if value < -64:
            return -64

        return value


if __name__ == "__main__":

    settings: GameSettings = GameSettings(19)

    board: Board = Board(settings)

    size: int = board.settings.board_size
    occupied: Set[Tuple[int, int]] = {(4, 5), (7, 5), (10, 10), (11, 10)}

    def place_random_spread(
        color: BoardSpace,
        count: int = 8,
        min_distance: int = 3
    ) -> None:
        candidates = [
            (x, y)
            for x in range(size)
            for y in range(size)
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
            dilations=21
        )
    )

    territory_board: Board = (
        BouzyAlgorithm.evaluate_territory_board(
            board=board,
            dilations=21
        )
    )

    print("ORIGINAL BOARD")
    print()

    size: int = board.settings.board_size

    for y in range(size):

        row: List[str] = []

        for x in range(size):

            tile: BoardSpace = (
                board.board_tiles[x][y]
            )

            if tile == BoardSpace.BLACK:
                row.append("B")

            elif tile == BoardSpace.WHITE:
                row.append("W")

            else:
                row.append(".")

        print(" ".join(row))

    print()
    print("BOUZY VALUES")
    print()

    BouzyAlgorithm.print_values(values)

    print()
    print("EVALUATED TERRITORY BOARD")
    print()

    for y in range(size):

        row: List[str] = []

        for x in range(size):

            tile: BoardSpace = (
                territory_board.board_tiles[x][y]
            )

            if tile == BoardSpace.BLACK:
                row.append("B")

            elif tile == BoardSpace.WHITE:
                row.append("W")

            else:
                row.append(".")

        print(" ".join(row))