import windowPartitioner as Windgpfyks
import pygame as pg
from signals import Signal
from typing import Tuple, Any, List
from drawer import Drawer
from Board import Board, calculate_score
from gameSettings import GameSettings
from game import Game
from game import States
from bouzy import BouzyAlgorithm

instance_active : bool = True

sizes : List[int] = [19, 13, 9]
current_size_setting : int = 13

game_active : bool = False

white_score : int = 0
black_score : int = 0

def quit():
    global instance_active
    instance_active = False

def switch_state(state : States):
    global game
    game.current_state = state
    global ui_manager
    ui_manager.switch_menu(0)
    ui_manager.esc_menu = False
    update_score()

def about():
    global game
    game.current_state = States.MAIN__MENU
    global ui_manager
    ui_manager.esc_menu = False
    ui_manager.switch_menu(1)

def new_game():
    global game
    game.current_state = States.MAIN__MENU
    global ui_manager
    ui_manager.esc_menu = False
    ui_manager.switch_menu(2)

def toggle_esc_menu():
    global ui_manager
    ui_manager.esc_menu = not ui_manager.esc_menu

def size_settings(size_index : int):
    global current_size_setting
    current_size_setting = sizes[size_index]
    global board
    board = Board(GameSettings(current_size_setting))
    global drawer
    drawer = Drawer(current_size_setting,current_size_setting,(WINDOW_HEIGHT-100,WINDOW_HEIGHT-100),(50,50), margin=50)
    global game
    global player_action
    game = Game(board,drawer,player_action)
    score_board = None
    print("Ændret brætstørrelse til noget")
    global game_active
    game_active = True
    game.start_game()
    switch_state(States.GAME_ACTIVE)

def continue_game():
    global game_active
    if (game_active):
        switch_state(States.GAME_ACTIVE)

def update_score():
    global ui_manager
    ui_manager.menus[0].components[4].text.text = f"{white_score}"
    ui_manager.menus[0].components[5].text.text = f"{black_score}"

El_capone: dict[str, Any] = {
    "quit":quit,
    "main_menu": lambda: switch_state(States.MAIN__MENU),
    "start_game": continue_game,
    "new_game" : new_game,
    "about": about,
    "settings": new_game,
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

    score_board = None

    ui_manager = Windgpfyks.Game(El_capone)
    ui_manager.load_menus("menu.json")
    update_score()

    game.start_game()
    game.current_state = States.MAIN__MENU

    while instance_active:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                instance_active = False

            elif event.type == pg.VIDEORESIZE:
                # Update screen size when resized
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            elif event.type == pg.MOUSEBUTTONDOWN and not ui_manager.esc_menu:
                if event.button == 1:  # 1 = Left click, 2 = Middle, 3 = Right
                    player_action.emit(event.pos)
                    score_board = None
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    game.current_state = States.GAME_ACTIVE
                elif event.key == pg.K_o:
                    game.current_state = States.GAME_INACTIVE
                elif event.key == pg.K_i:
                    game.current_state = States.MAIN__MENU
                elif event.key == pg.K_ESCAPE and game.current_state != States.MAIN__MENU:
                    ui_manager.esc_menu = not ui_manager.esc_menu

                if game.current_state == States.GAME_ACTIVE:
                    if event.key == pg.K_e:
                        score_board = BouzyAlgorithm.evaluate_territory_board(board)
                    elif event.key == pg.K_s:
                        game_active = game.pass_turn()
                        if game_active == False:
                            score_board = BouzyAlgorithm.evaluate_territory_board(board)
                            black_score, white_score = calculate_score(board, score_board)


            if (ui_manager.esc_menu):
                ui_manager.esc_event_handling(event)
            elif (game.current_state == States.MAIN__MENU):
                ui_manager.menu_event_handling(event)

        mouse_pos = pg.mouse.get_pos()
        
        if game.current_state == States.MAIN__MENU:
            # Tegn hovedmenuen.
            pg.Surface.fill(screen, (38, 206, 253))
            ui_manager.update()
            ui_manager.draw(screen)

        elif game.current_state == States.GAME_INACTIVE:
            pg.Surface.fill(screen, (0, 0, 0))
            mouse_pos = (-470032, -432876234)
            drawer.draw(board,screen, mouse_pos,game.current_turn, territory_indicator=score_board)
        elif game.current_state == States.GAME_ACTIVE:
            pg.Surface.fill(screen, (0, 0, 0))
            drawer.draw(board,screen, mouse_pos,game.current_turn, territory_indicator=score_board)

        if (ui_manager.esc_menu):
            ui_manager.esc_update()
            ui_manager.esc_draw(screen)


        pg.display.flip()
        clock.tick(30)

    pg.quit()