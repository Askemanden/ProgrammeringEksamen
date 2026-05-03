import WindowPartitioner as Windgpfyks
import pygame as pg
from signals import Signal
from typing import Tuple, List
from drawer import Drawer
from Board import Board, specielt_bræt
from gameSettings import GameSettings
from game import Game
from game import States

instance_active : bool = True

def quit():
    global instance_active
    instance_active = False

def switch_state(state : States):
    global game
    game.current_state = state
    global ui_managler
    ui_managler.esc_menu = False

def toggle_esc_menu():
    global ui_managler
    ui_managler.esc_menu = not ui_managler.esc_menu

El_capone = {
    "quit":quit,
    "main_menu": lambda: switch_state(States.HOVEVD_MUEN),
    "start_game": lambda: switch_state(States.SPIL_AKTIVIT),
    "toggle_esc_menu": toggle_esc_menu,
}

if __name__ == "__main__":

    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 800
    pg.init()
    pg.font.init()

    screen = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pg.RESIZABLE)
    pg.display.set_caption("Tingeling")
    clock = pg.time.Clock()
    board_size = 5
    settings = GameSettings(board_size)
    drawer = Drawer(board_size,board_size,(WINDOW_HEIGHT-100,WINDOW_HEIGHT-100),(50,50), margin=50)
    
    board = Board(settings, specielt_bræt)

    player_action: Signal[Tuple[int,int]] = Signal[Tuple[int,int]]()

    game = Game(board,drawer,player_action)

    ui_managler = Windgpfyks.Game(El_capone)
    ui_managler.load_menus("menu.json")

    game.start_game()
    game.current_state = States.HOVEVD_MUEN

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
                elif event.key == pg.K_i:
                    game.current_state = States.HOVEVD_MUEN
                elif event.key == pg.K_ESCAPE:
                    ui_managler.esc_menu = not ui_managler.esc_menu
            if (ui_managler.esc_menu):
                ui_managler.esc_event_handling(event)
            elif (game.current_state == States.HOVEVD_MUEN):
                ui_managler.menu_event_handling(event)

        mouse_pos = pg.mouse.get_pos()
        
        if game.current_state == States.HOVEVD_MUEN:
            # Tegn hovedmenuen.
            pg.Surface.fill(screen, (38, 206, 253))
            ui_managler.update()
            ui_managler.draw(screen)

        elif game.current_state == States.SPIL_INKAKTIVT:
            mouse_pos = (-470032, -432876234)
            drawer.draw(board,screen, mouse_pos,game.current_turn)
        elif game.current_state == States.SPIL_AKTIVIT:
            drawer.draw(board,screen, mouse_pos,game.current_turn)

        if (ui_managler.esc_menu):
            ui_managler.esc_update()
            ui_managler.esc_draw(screen)

        pg.display.flip()
        clock.tick(34)

    pg.quit()