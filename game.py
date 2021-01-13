# ----------------------IMPORTS---------------------------------------
import math
import time
import copy
import os
import pickle
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
    last_options = [3, 2, 2, 1, 1]
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
            else:
                option_set[current_option] = 0
            return current_option
        elif event.key == pyg.K_ESCAPE:
            return -1
        elif event.key == pyg.K_RETURN:
            return None
    else:
        return current_option


def read_cache(size: int = 0):
    if size < 3 or size > 4:
        size = 0
    data_dir = 'data\\'
    ls = os.listdir(data_dir)
    if size == 0:
        caches = list()
        for file in ls:
            f = open(data_dir + file, 'rb')
            caches.append(pickle.load(f))
            f.close()
        return caches
    else:
        for file in ls:
            if str(size) in file:
                cache = dict()
                f = open(data_dir + file, 'rb')
                print(data_dir + file, f)
                cache = pickle.load(f)
                f.close()
                return cache


def save_cache(cache: dict, size: int):
    if cache is None:
        return
    data_dir = 'data\\cache'
    f = open(data_dir + str(size), 'wb')
    pickle.dump(cache, f)
    f.close()


def read_local():
    local_file = open("local", 'r')
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
    caches = read_cache(start_size)
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
        # setup players with IDs and symbols(X or O)
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
                    save_cache(ttt_ai.AI.CACHE, option_set[1] + 3)
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
                        save_cache(ttt_ai.AI.CACHE, option_set[1] + 3)
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
                            new_size = option_set[1] + 3
                            b = ttt_board.Board(size=new_size)
                            window.draw_loading_screen()
                            save_cache(ttt_ai.AI.CACHE, previous_options_set[1] + 3)
                            ttt_ai.AI.CACHE = read_cache(new_size)
                            turn = 1
                            game_number = 0
                            score = [0, 0, 0]
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
        # check for ending game conditions
        current_result = b.checkForEndgame()
        # if game has concluded
        if current_result != -1:
            # Add one to the winning side/draw's count
            if current_result == 0:
                score[0] += 1
            elif current_result == 1:
                if player1.is_x() == 1:
                    score[1] += 1
                else:
                    score[2] += 1
            else:
                if player1.is_x() == 1:
                    score[2] += 1
                else:
                    score[1] += 1

            # Increment game number
            game_number = game_number + 1
            # If the game number is even set turn to 1 which means player1 is X
            if game_number % 2 == 0:
                turn = 1
            # Else set turn to 2 which means player2 is X
            else:
                turn = 2
            # Initialize new, empty board
            b = ttt_board.Board(size=option_set[1] + 3)
            # Switch players symbols
            switch_symbols(player1, player2)
            continue

        if current_player.is_AI():
            if ttt_ai.AI.CACHE is None:
                ttt_ai.AI.CACHE = read_cache(size=option_set[1] + 3)
            move = current_player.minimax(b)
            b.update(current_player.is_x(), move)
            turn = switch_turn(turn)

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
