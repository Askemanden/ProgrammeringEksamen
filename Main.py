import windowPartitioner
import pygame as pg
from signals import Signal
from typing import Tuple
from drawer import Drawer
from board import Board
from gameSettings import GameSettings
from game import Game


if __name__ == "__main__":

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800



    screen = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pg.RESIZABLE)
    pg.display.set_caption("Tingeling")
    clock = pg.time.Clock()
    board_size = 19
    settings = GameSettings(board_size)
    drawer = Drawer(board_size,board_size,(WINDOW_HEIGHT-100,WINDOW_HEIGHT-100),(50,50), margin=50)
    board = Board(settings)

    player_action: Signal[Tuple[int,int]] = Signal[Tuple[int,int]]()

    game = Game(board,drawer,player_action)

    game.start_game()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.VIDEORESIZE:
                # Update screen size when resized
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 = Left click, 2 = Middle, 3 = Right
                    player_action.emit(event.pos)
            #elif spiller-klasse
        mouse_pos = pg.mouse.get_pos()


        drawer.draw(board,screen, mouse_pos,game.current_turn)

        pg.display.flip()
        clock.tick(20)

    pg.quit()