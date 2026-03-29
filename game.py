from player import Player
from board import Board
from signals import Signal


class Game:
    def __init__(self, board: Board, player1 : Player, player2 : Player, game_events: Signal[int,int]) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
