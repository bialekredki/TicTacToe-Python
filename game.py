# ----------------------IMPORTS---------------------------------------
import math
import time
import copy
import pygame as pyg
import ttt_gfx
import ttt_ai
import ttt_board
import ttt_console

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
    global console, score
    # Initializes board
    b = ttt_board.Board(size=start_size)
    closed = False
    # If console mode is not loaded initialize GUI
    if not console:
        # Read locals' text from local file
        local = read_local()
        # Initialize display
        window = ttt_gfx.GameWindow(resolutions[0], local, b.size)
        menu = False
        option = 0
        # Options for GUI
        option_set = [0, 0, 0, 0, 0]
        previous_options_set = copy.deepcopy(option_set)
    turn = 1
    game_number = 0
    ai1 = ttt_ai.AI(1)
    ai2 = ttt_ai.AI(2)
    # -------------------------main loop------------------------------
    while not closed:
        # When console mode is off, render graphics and wait for events
        if not console:
            for event in pyg.event.get():
                # PRESS EXIT EVENT
                if event.type == pyg.QUIT:
                    window.close()
                    closed = True
                # Player's interaction events
                elif event.type == pyg.MOUSEBUTTONDOWN and turn == 2:
                    pos = ttt_gfx.mousePositionToGridTile(window.calculate_grid_parameters(b.size), pyg.mouse.get_pos(), b.size)
                    menu_button_size = window.get_menu_button_size()
                    if pos is not None:
                        b.update(turn, pos)
                        if turn == 1:
                            turn = 2
                        else:
                            turn = 1
                    elif pyg.mouse.get_pos()[0] < menu_button_size[0] and pyg.mouse.get_pos()[1] < menu_button_size[1]:
                        menu = True
                    elif pyg.mouse.get_pos()[0] < menu_button_size[0] and pyg.mouse.get_pos()[1] < menu_button_size[1]*3:
                        window.close()
                elif menu:
                    option = process_menu_event(event, option,option_set)
                    if option is None:
                        menu = False
                        option = 0
                        if option_set[0] != previous_options_set[0] or option_set[4] != previous_options_set[4]:
                            window.resize(resolutions[option_set[0]],bool(option_set[4]))
                        if option_set[1] != previous_options_set[1]:
                            b = ttt_board.Board(size=option_set[1]+3)
                            turn = 1
                            game_number = 0
                            score = [0,0,0]
                        if option_set[2] != previous_options_set[2]:
                            pass
                        if option_set[3] != previous_options_set[3]:
                            window.close(True)
                        previous_options_set = copy.deepcopy(option_set)
                    elif option == -1:
                        option_set = copy.deepcopy(previous_options_set)

            if not menu:
                window.render(board=b,game_params=(turn,score))
            else:
                window.render(menu_params=(option,option_set[0],option_set[1],option_set[2],option_set[3],option_set[4]))
        current_result = b.checkForEndgame()
        if current_result != -1:
            score[current_result] += 1
            game_number = game_number + 1
            b = ttt_board.Board(size=option_set[1]+3)
            continue

        if turn == 1:
            #start = time.time_ns()
            b.update(1,ai1.minimax(b))
            turn = 2
            #end = time.time_ns()
            #print("MiniMax time : ", end - start, "ns")
        #else:
            #b.update(2,ai2.minimax(b))
            #turn = 1
    # -------------------------end of main loop-----------------------

# -------------------------GLOBAL VARIABLES---------------------------

score = [0,0,0]
fullscreen = bool()
game_mode = int()
console = bool()
game_number = int()
start_size = int()
resolution = int()
resolutions = ((800,600),(1270,720),(1280,1024),(0,0))
# -------------------------END OF GLOBAL VARIABLES--------------------

config = open("config", 'r')
for x in config:    exec(x)
config.close()
run()
