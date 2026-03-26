from typing import List
from GameSettings import GameSettings as _GameSettings
from enum import Enum

class BoardSpace(Enum):
    WHITE = 1
    BLACK = 2
    EMPTY = 3


class Board:
    def __init__(self, settings : _GameSettings) -> None:
        self.settings : _GameSettings = settings

        self.board_tiles : List[List[int]] = []

    def _populate_board_tiles(self):
        self.board_tiles


