from typing import List, Tuple
from gameSettings import GameSettings as _GameSettings
from enum import Enum

class BoardSpace(Enum):
    WHITE = 1
    BLACK = 2
    EMPTY = 3

class Board:
    def __init__(self, settings : _GameSettings) -> None:
        self.settings : _GameSettings = settings

        self.board_tiles : List[List[BoardSpace]] = self.__populate_board_tiles()

        self.last_placed_stone : Tuple[BoardSpace, Tuple[int,int]] = (BoardSpace.EMPTY,(0,0))

    def __populate_board_tiles(self) -> List[List[BoardSpace]]:
        columns : List[List[BoardSpace]] = []
        for _ in range(self.settings.board_size):
            row : List[BoardSpace] = []
            for _ in range(self.settings.board_size):
                row.append(BoardSpace.EMPTY)
            columns.append(row)
        return columns

    def __out_of_bounds(self, x : int, y: int) -> bool:
        if x < 0 or x > self.settings.board_size:
            return True
        if y < 0 or y > self.settings.board_size:
            return True
        return False

    def place_stone(self, x : int, y : int, stone : BoardSpace) -> bool:
        if (self.__out_of_bounds(x, y)):
            return False
        if self.board_tiles[x][y] != BoardSpace.EMPTY:
            return False
        self.board_tiles[x][y] = stone
        self.last_placed_stone = (stone,(x,y))
        return True

    def remove_stone(self, x : int, y : int) -> bool:
        if (self.__out_of_bounds(x, y)):
            return False
        self.board_tiles[x][y] = BoardSpace.EMPTY
        return True

    def check_captures(self):...

    
# Kodegravplads

"""
    def _identify_group(self, x : int, y : int) -> List[Tuple[int, int]]:
        if (self.__out_of_bounds(x, y)):
            return [(-1, -1)]
        group : List[Tuple[int, int]] = []
        
        iterations : int = 0; _x : int = x; _y : int = y
        search : bool = True
        while (search or iterations < 100):

            # Ånde-først søgealgoritme

            group.append((_x, _y))

            iterations = iterations + 1
        return group
"""