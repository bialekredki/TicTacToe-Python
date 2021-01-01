# ----------------------IMPORTS---------------------------------------
import math
import time
import copy
import pygame as pyg
import ttt_gfx
import ttt_ai
import ttt_player
import ttt_board
import ttt_console

def switch_symbols(player1, player2):
    if player1.is_x() == 1:
        player1.set_symbol('O')
        player2.set_symbol('X')
    else:
        player1.set_symbol('X')
        player2.set_symbol('O')


def wait(milisecs: float):
    diff = 20
    start = time.time()
    print(time)
    while diff < milisecs:
        diff = time.time() - start
        print(diff)

def switch_turn(turn):
    if turn == 1:
        return 2
    else:
        return 1


def setup_players(game_mode: int = 0, game_number: int = 0):
    if game_number % 2 == 0:
        char_set = ('X', 'O')
    else:
        char_set = ('O', 'X')
    if game_mode == 0:
        return ttt_player.Player(1, char_set[0]), ttt_ai.AI(2, char_set[1])
    elif game_mode == 1:
        return ttt_player.Player(1, char_set[0]), ttt_player.Player(2, char_set[1])
    else:
        return ttt_ai.AI(1, char_set[0]), ttt_ai.AI(2, char_set[1])


def player_move(player, console: bool = False):
    if player.is_AI():
        return player.minimax()
    else:
        if console:
            pass
        else:
            return True

def process_menu_event(event:pyg.event,current_option:int,option_set:tuple):
    last_options = [3,6,2,1,1]
    if event.type == pyg.KEYDOWN:
        if event.key == pyg.K_UP:
            if current_option-1 >= 0:
                return current_option - 1
            else: return len(last_options) - 1
        elif event.key == pyg.K_DOWN:
            if current_option+1 <= len(last_options)-1:
                return current_option + 1
            else: return 0
        elif event.key == pyg.K_LEFT:
            if option_set[current_option] - 1 >= 0:
                option_set[current_option] = option_set[current_option] - 1
            else: option_set[current_option] = last_options[current_option]
            return current_option
        elif event.key == pyg.K_RIGHT:
            if option_set[current_option] + 1 <= last_options[current_option]:
                option_set[current_option] = option_set[current_option] + 1
            else: option_set[current_option] = 0
            return current_option
        elif event.key == pyg.K_ESCAPE:
            return -1
        elif event.key == pyg.K_RETURN:
            return None
    else:
        return current_option


def read_local():
    local_file = open("local",'r')
    local = dict()
    lines = local_file.readlines()
    local_file.close()
    for line in lines:
        split = line.split(';')
        for index, s in enumerate(split):
            if s.endswith('\n'):
                split[index] = s.replace('\n','')
        if not split[0].startswith('opt'):
            local[split[0]] = split[1]
        else:
            opt_list = list()
            for index,element in enumerate(split):
                if index != 0:
                    opt_list.append(element)
            local[split[0]] = opt_list
    return local

def run():
    global console, score,game_number,game_mode
    # Initializes board
    b = ttt_board.Board(size=start_size)
    # [0]resolution,[1]board size,[2]game mode,[3]console,[4]fullscreen
    option_set = [resolution, start_size-3, game_mode, console, fullscreen]
    previous_options_set = copy.deepcopy(option_set)
    closed = False
    # If console mode is not loaded initialize GUI
    if not console:
        # Read locals' text from local file
        local = read_local()
        # Initialize display
        window = ttt_gfx.GameWindow(resolutions[0], local, b.size)
        menu = False
        option = 0
    turn = 1
    player1 = None
    player2 = None
    # -------------------------main loop------------------------------
    while not closed:
        if player1 is None or player2 is None:
            player1, player2 = setup_players(game_mode, game_number)

        if turn % 2 == 1:
            current_player = player1
        else:
            current_player = player2
        # When console mode is off, render graphics and wait for events
        if not console:
            for event in pyg.event.get():
                # PRESS EXIT EVENT
                if event.type == pyg.QUIT:
                    window.close()
                    closed = True
                # Player's interaction events
                elif event.type == pyg.MOUSEBUTTONDOWN:
                    pos = ttt_gfx.mousePositionToGridTile(window.calculate_grid_parameters(b.size), pyg.mouse.get_pos(),
                                                          b.size)
                    menu_button_size = window.get_menu_button_size()
                    if pos is not None and not current_player.is_AI():
                        if b.update(current_player.is_x(), pos):
                            turn = switch_turn(turn)
                    elif pyg.mouse.get_pos()[0] < menu_button_size[0] and pyg.mouse.get_pos()[1] < menu_button_size[1]:
                        menu = True
                    elif pyg.mouse.get_pos()[0] < menu_button_size[0] and pyg.mouse.get_pos()[1] < menu_button_size[
                        1] * 3:
                        window.close()
                elif menu:
                    option = process_menu_event(event, option,option_set)
                    if option is None:
                        menu = False
                        option = 0
                        # If resolution/fullscreen settings has been changed, resize the Window
                        if option_set[0] != previous_options_set[0] or option_set[4] != previous_options_set[4]:
                            window.resize(resolutions[option_set[0]],bool(option_set[4]))
                        # If board size has been changed, create a new empty board and reset all game's parameters
                        if option_set[1] != previous_options_set[1]:
                            b = ttt_board.Board(size=option_set[1]+3)
                            turn = 1
                            game_number = 0
                            score = [0,0,0]
                        # If game mode has been changed, do something
                        if option_set[2] != previous_options_set[2]:
                            pass
                        if option_set[3] != previous_options_set[3]:
                            window.close(True)
                        previous_options_set = copy.deepcopy(option_set)
                    elif option == -1:
                        option_set = copy.deepcopy(previous_options_set)

            if not menu and not console:
                # Display game screen
                window.render(board=b, game_params=(current_player, score))
            elif menu and not console:
                # Display game menu screen
                window.render(
                    menu_params=(option, option_set[0], option_set[1], option_set[2], option_set[3], option_set[4]))
        current_result = b.checkForEndgame()
        if current_result != -1:
            b.display()
            score[current_result] += 1
            game_number = game_number + 1
            if game_number % 2 == 0:
                turn = 1
            else:
                turn = 2
            b = ttt_board.Board(size=option_set[1] + 3)
            print(turn, '\t', game_number)
            switch_symbols(player1, player2)
            continue

        if current_player.is_AI():
            print(current_player.player_number, current_player.is_x())
            b.update(current_player.is_x(), current_player.minimaxv2(b))
            turn = switch_turn(turn)
            # time.sleep(1)

    # -------------------------end of main loop-----------------------

# -------------------------GLOBAL VARIABLES---------------------------

score = [0,0,0]
fullscreen = bool(False)
game_mode = int(0)
console = bool(False)
game_number = int(0)
start_size = int()
resolution = int()
resolutions = ((800,600),(1270,720),(1280,1024),(0,0))
# -------------------------END OF GLOBAL VARIABLES--------------------

config = open("config", 'r')
for x in config:    exec(x)
config.close()
run()
