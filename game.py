from Board import Board, BoardSpace
from signals import Signal
from typing import Tuple
from drawer import Drawer
from enum import Enum

Player = BoardSpace

class States(Enum):
    HOVEVD_MUEN = 0
    SPIL_INKAKTIVT = 1
    SPIL_AKTIVIT = 2

class Game:

    def __init__(self, board: Board, drawer: Drawer, player_actions: Signal[Tuple[int,int]]) -> None:
        self.board = board
        self.drawer = drawer
        self.player_actions = player_actions

        self.current_turn : Player = Player.EMPTY
        self.last_turn : Player = Player.EMPTY

        self.player_actions.connect(lambda position: self.__on_player_action(position))

        self.current_state : States = States.HOVEVD_MUEN
    
    def __on_player_action(self, position: Tuple[int,int]) -> None:

        if (self.current_state == States.SPIL_AKTIVIT):
            if self.current_turn == Player.EMPTY:
                return

            position = self.drawer.global_to_board(position[0],position[1])

            placed = self.board.place_stone(position[0],position[1],self.current_turn)

            if not placed:
                return

            self.last_turn = self.current_turn
            self.current_turn = Player.BLACK if self.current_turn == Player.WHITE else Player.WHITE

    def pause_unpause(self) -> None:
        self.current_turn = Player.EMPTY if self.current_turn != Player.EMPTY else self.last_turn

    def start_game(self) -> None:
        self.current_state = States.SPIL_AKTIVIT
        self.current_turn = Player.BLACK
        self.last_turn = Player.WHITE