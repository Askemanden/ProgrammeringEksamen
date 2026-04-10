from board import Board, BoardSpace
from signals import Signal
from typing import Tuple
from drawer import Drawer

Player = BoardSpace

class Game:

    def __init__(self, board: Board, drawer: Drawer, player_actions: Signal[Tuple[int,int]]) -> None:
        self.board = board
        self.drawer = drawer
        self.player_actions = player_actions

        self.current_turn : Player = Player.EMPTY
        self.last_turn : Player = Player.EMPTY

        self.player_actions.connect(lambda position: self.__on_player_action(position))
    
    def __on_player_action(self, position: Tuple[int,int]) -> None:
        
        if self.current_turn == Player.EMPTY:
            return

        position = self.drawer.global_to_board(position[0],position[1])

        placed = self.board.place_stone(position[0],position[1],self.current_turn)
        
        if not placed:
            return
        
        self.board.check_captures()
        
        self.last_turn = self.current_turn

        self.current_turn = Player.BLACK if self.current_turn == Player.WHITE else Player.WHITE



    def pause_unpause(self) -> None:
        self.current_turn = Player.EMPTY if self.current_turn != Player.EMPTY else self.last_turn
