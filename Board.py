from typing import List, Tuple
from gameSettings import GameSettings as _GameSettings
from enum import Enum

class BoardSpace(Enum):
    WHITE = 1
    BLACK = 2
    EMPTY = 3

class Group:
    def __init__(self, colour : BoardSpace, members : List[Tuple[int, int]]):
        self.colour = colour
        self.members : List[Tuple[int, int]] = members

class Board:
    def __init__(self, settings : _GameSettings, premade_board_pos : List[List[BoardSpace]] = []) -> None:
        self.settings : _GameSettings = settings

        if (len(premade_board_pos) != self.settings.board_size):
            self.board_tiles : List[List[BoardSpace]] = self.__populate_board_tiles()
            print("standardbræt oprettet")
        else:
                # Det korrekte antal kolonner er til stede.
            self.succes = True
            for i in range(len(premade_board_pos)):
                if(len(premade_board_pos[i]) != self.settings.board_size):
                    self.succes = False
                    break
            if (self.succes):
                self.board_tiles : List[List[BoardSpace]] = premade_board_pos
                print("Specielt bræt oprettet")
            else:
                self.board_tiles : List[List[BoardSpace]] = self.__populate_board_tiles()
                print("Bræt givet af forkert størrelse | Standardbræt oprettet")

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
        if x < 0 or x > self.settings.board_size - 1:
            return True
        if y < 0 or y > self.settings.board_size - 1:
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
    
    def find_groups(self):
        
        first_stone = True

        found_groups : List[Group] = []

        for _y in range(self.settings.board_size):
            for _x in range(self.settings.board_size):
                if (first_stone):
                    if (self.board_tiles[_x][_y] == BoardSpace.EMPTY):
                        continue
                    start_group = Group(self.board_tiles[_x][_y], [(_x, _y)])
                    found_groups.append(start_group)

                    # Tjek nabo
                if (self.board_tiles[_x - 1][_y] == self.board_tiles[_x][_y]):
                        # Nabo i x retningen er ens farve.
                    pass

specielt_bræt = [
    [BoardSpace.BLACK, BoardSpace.BLACK, BoardSpace.BLACK, BoardSpace.EMPTY, BoardSpace.EMPTY],
    [BoardSpace.EMPTY, BoardSpace.BLACK, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY],
    [BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY],
    [BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY],
    [BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY, BoardSpace.EMPTY]
]

"""
class BoardPosition:    # En klasse til at sørge for at alle koordinater er gyldige
    def __init__(self, x : int, y : int, board_class_ptr : Board):

        if (x < board_class_ptr.settings.board_size and x >= 0):
            self.x = x
        else:
            self.x = 0
        if (y < board_class_ptr.settings.board_size and y >= 0):
            self.y = y
        else:
            self.y = 0
"""

if __name__ == "__main__":
    size = _GameSettings(5)

    bræt = Board(size, specielt_bræt)
