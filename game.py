from Board import Board, BoardSpace
from signals import Signal
from typing import Tuple
from drawer import Drawer
from enum import Enum

Player = BoardSpace


class States(Enum):
    MAIN__MENU = 0
    GAME_INACTIVE = 1
    GAME_ACTIVE = 2


class Game:

    def __init__(
        self,
        board: Board,
        drawer: Drawer,
        player_actions: Signal[Tuple[int, int]]
    ) -> None:

        self.board: Board = board

        self.drawer: Drawer = drawer

        self.player_actions: Signal[Tuple[int, int]] = (
            player_actions
        )

        self.current_turn: Player = Player.EMPTY

        self.last_turn: Player = Player.EMPTY

        # Number of consecutive passes.
        # Two consecutive passes ends the game.
        self.consecutive_passes: int = 0

        self.player_actions.connect(
            lambda position: self.__on_player_action(position)
        )

        self.current_state: States = States.MAIN__MENU

    def __switch_turn(self) -> None:

        self.last_turn = self.current_turn

        self.current_turn = (
            Player.BLACK
            if self.current_turn == Player.WHITE
            else Player.WHITE
        )

    def __on_player_action(
        self,
        position: Tuple[int, int]
    ) -> None:

        if self.current_state != States.GAME_ACTIVE:
            return

        if self.current_turn == Player.EMPTY:
            return

        board_position: Tuple[int, int] = (
            self.drawer.global_to_board(
                position[0],
                position[1]
            )
        )

        placed: bool = self.board.place_stone(
            board_position[0],
            board_position[1],
            self.current_turn
        )

        if not placed:
            return

        # A legal move resets consecutive passes.
        self.consecutive_passes = 0

        self.__switch_turn()

# return whether or not the game should continue
    def pass_turn(self) -> bool:

        if self.current_state != States.GAME_ACTIVE:
            return True

        if self.current_turn == Player.EMPTY:
            return True

        self.consecutive_passes += 1

        # Two consecutive passes ends the game.
        if self.consecutive_passes >= 2:

            self.current_state = States.GAME_INACTIVE

            self.last_turn = self.current_turn

            self.current_turn = Player.EMPTY

            return False

        self.__switch_turn()

        return True

    def pause_unpause(self) -> None:

        self.current_turn = (
            Player.EMPTY
            if self.current_turn != Player.EMPTY
            else self.last_turn
        )

    def start_game(self) -> None:

        self.current_state = States.GAME_ACTIVE

        self.current_turn = Player.BLACK

        self.last_turn = Player.WHITE

        self.consecutive_passes = 0