import WindowPartitioner as Windgpfyks
import pygame as pg
from signals import Signal
from typing import Tuple, Any, List
from drawer import Drawer
from Board import Board, specielt_bræt
from gameSettings import GameSettings
from game import Game
from game import States

instance_active : bool = True

sizes : List[int] = [19, 13, 9]
current_size_setting : int = 13

def quit():
    global instance_active
    instance_active = False

def switch_state(state : States):
    global game
    game.current_state = state
    global ui_managler
    ui_managler.switch_menu(0)
    ui_managler.esc_menu = False

def about():
    global game
    game.current_state = States.HOVEVD_MUEN
    global ui_managler
    ui_managler.esc_menu = False
    ui_managler.switch_menu(1)

def options():
    global game
    game.current_state = States.HOVEVD_MUEN
    global ui_managler
    ui_managler.esc_menu = False
    ui_managler.switch_menu(2)

def toggle_esc_menu():
    global ui_managler
    ui_managler.esc_menu = not ui_managler.esc_menu

def size_settings(size_index : int):
    global current_size_setting
    current_size_setting = sizes[size_index]
    global board
    board = Board(GameSettings(current_size_setting))
    global drawer
    drawer = Drawer(current_size_setting,current_size_setting,(WINDOW_HEIGHT-100,WINDOW_HEIGHT-100),(50,50), margin=50)
    print("Ændret brætstørrelse til noget")

El_capone: dict[str, Any] = {
    "quit":quit,
    "main_menu": lambda: switch_state(States.HOVEVD_MUEN),
    "start_game": lambda: switch_state(States.SPIL_AKTIVIT),
    "about": about,
    "settings": options,
    "toggle_esc_menu": toggle_esc_menu,
    "19x19": lambda: size_settings(0),
    "13x13": lambda: size_settings(1),
    "9x9": lambda: size_settings(2),
}

if __name__ == "__main__":

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    pg.init()
    pg.font.init()

    screen = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pg.RESIZABLE)
    pg.display.set_caption("Tingeling")
    clock = pg.time.Clock()

    settings = GameSettings(current_size_setting)
    drawer = Drawer(current_size_setting,current_size_setting,(WINDOW_HEIGHT-100,WINDOW_HEIGHT-100),(50,50), margin=50)
    
    board = Board(settings)

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
            elif event.type == pg.MOUSEBUTTONDOWN and not ui_managler.esc_menu:
                if event.button == 1:  # 1 = Left click, 2 = Middle, 3 = Right
                    player_action.emit(event.pos)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    game.current_state = States.SPIL_AKTIVIT
                elif event.key == pg.K_o:
                    game.current_state = States.SPIL_INKAKTIVT
                elif event.key == pg.K_i:
                    game.current_state = States.HOVEVD_MUEN
                elif event.key == pg.K_ESCAPE and game.current_state != States.HOVEVD_MUEN:
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
            pg.Surface.fill(screen, (0, 0, 0))
            mouse_pos = (-470032, -432876234)
            drawer.draw(board,screen, mouse_pos,game.current_turn)
        elif game.current_state == States.SPIL_AKTIVIT:
            pg.Surface.fill(screen, (0, 0, 0))
            drawer.draw(board,screen, mouse_pos,game.current_turn)

        if (ui_managler.esc_menu):
            ui_managler.esc_update()
            ui_managler.esc_draw(screen)

        pg.display.flip()
        clock.tick(34)

    pg.quit()