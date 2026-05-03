import WindowPartitioner
import pygame as pg
from signals import Signal
from typing import Tuple, List
from drawer import Drawer
from Board import Board, specielt_bræt
from gameSettings import GameSettings
from game import Game
from game import States

def start_stop():
    game.running = not game.running

if __name__ == "__main__":

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800

    screen = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pg.RESIZABLE)
    pg.display.set_caption("Tingeling")
    clock = pg.time.Clock()
    board_size = 5
    settings = GameSettings(board_size)
    drawer = Drawer(board_size,board_size,(WINDOW_HEIGHT-100,WINDOW_HEIGHT-100),(50,50), margin=50)
    
    board = Board(settings, specielt_bræt)

    player_action: Signal[Tuple[int,int]] = Signal[Tuple[int,int]]()

    game = Game(board,drawer,player_action)

    game.start_game()
    game.current_state = States.HOVEVD_MUEN

    instance_active : bool = True
    while instance_active:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                instance_active = False

            elif event.type == pg.VIDEORESIZE:
                # Update screen size when resized
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 = Left click, 2 = Middle, 3 = Right
                    player_action.emit(event.pos)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    game.current_state = States.SPIL_AKTIVIT
                elif event.key == pg.K_o:
                    game.current_state = States.SPIL_INKAKTIVT
        mouse_pos = pg.mouse.get_pos()
        
        if game.current_state == States.HOVEVD_MUEN:
            # Tegn hovedmenuen.
            pass
        elif game.current_state == States.SPIL_INKAKTIVT:
            mouse_pos = (-470032, -432876234)
        elif game.current_state == States.SPIL_AKTIVIT:
            pass
        
        drawer.draw(board,screen, mouse_pos,game.current_turn)


        pg.display.flip()
        clock.tick(34)

    pg.quit()