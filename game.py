# ----------------------IMPORTS---------------------------------------
import math
import time

import pygame as pyg


import centeredText as ctxt
import ttt_ai
import ttt_board
import ttt_console


# ----------------------------END OF IMPORTS--------------------------

def setResolution(str_value:str,value:int):
    global width, height
    if value == 0:
        width = 800
        height = 600
    elif value == 1:
        width = 1280
        height = 720
    elif value == 2:
        width = 1280
        height = 1024

def drawSideBar(main_font:pyg.font,turn:int):
    display.blit(main_font.render("MENU", True, WHITE), (0,0))
    menu_button_size = main_font.size("MENU")
    if turn == 1:   xo = 'X'
    else : xo = 'O'
    display.blit(main_font.render("Player {}'s turn({})".format(turn,xo), True, WHITE), (0,menu_button_size[1]))
    display.blit(main_font.render("Player 1 : {}".format(score[1]), True, WHITE), (width//2, 0))
    display.blit(main_font.render("Player 2 : {}".format(score[2]), True, WHITE), (width // 2, menu_button_size[1]))
    display.blit(main_font.render("Draw : {}".format(score[0]), True, WHITE), (width // 2, menu_button_size[1]*2))

    return menu_button_size


def mainMenu(main_font:pyg.font):
    close = False
    while not close:
        for event in pyg.event.get():
            if event.type == pyg.MOUSEBUTTONDOWN:
                close = True
        display.fill(BLACK)
        pyg.display.update()



def endMenu(result:int=0):
    pass

def drawGrid(grid_params, board, xo_font):
    state = board.getState()
    for x in range(board.size):
        for y in range(board.size):
            rect = pyg.Rect(grid_params["block size"] * x + grid_params["start x"],
                            grid_params["block size"] * y + grid_params["start y"],
                            grid_params["block size"], grid_params["block size"])
            pyg.draw.rect(display, WHITE, rect, 1)
            if state[x + y * board.size] == 1:
                ctxt.selfcenteredText(xo_font, "X", rect.topleft, grid_params["block size"]).draw(display, WHITE)
            elif state[x + y * board.size] == 2:
                ctxt.selfcenteredText(xo_font, "O", rect.topleft, grid_params["block size"]).draw(display, WHITE)
            else:
                continue


def mousePositionToGridTile(grid_params:dict, mouse_pos:list, size:int):
    for x in range(size):
        for y in range(size):
            if (grid_params["block size"] * x + grid_params["start x"] < mouse_pos[0] < grid_params["block size"] * x +
                    grid_params["start x"] + grid_params[
                        "block size"] and
                    grid_params["block size"] * y + grid_params["start y"] < mouse_pos[1] < grid_params[
                        "block size"] * y + grid_params["start y"] + grid_params["block size"]):
                return x + y * size


# --------------MAIN FUNCTION FOR GRAPHICAL TIC TAC TOE---------------
def run():
    # ---------------------initialization-----------------------------
    global game_number
    pyg.display.set_caption("TicTacToe")
    closed = False
    clock = pyg.time.Clock()
    b = ttt_board.Board(size=start_size)
    turn = 1
    xo_font = pyg.font.SysFont("Comic Sans", 270 - 70 * (b.size - 3))
    grid_params = {
        "width": 3 * width // 4,
        "height": 3 * height // 4
    }
    grid_params["start x"] = (width - grid_params["width"]) // 2
    grid_params["start y"] = (height - grid_params["height"]) // 2
    grid_params["block size"] = int(
        math.sqrt(grid_params["width"] * grid_params["height"] // (b.size * b.size)))
    # ---------------------end of initialization----------------------
    if game_number % 2 == 0:
        turn = 1
    else:
        turn = 2

    ai1 = ttt_ai.AI(1)
    ai2 = ttt_ai.AI(2)
    space = False
    # -------------------------main loop------------------------------
    while not closed:
        current_result = b.checkForEndgame()
        if current_result != -1:
            score[current_result] += 1
            game_number = game_number + 1
            return 0
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                closed = True
                pyg.display.quit()
                pyg.quit()
            elif event.type == pyg.MOUSEBUTTONDOWN and turn == 2:
                pos = mousePositionToGridTile(grid_params, pyg.mouse.get_pos(), b.size)
                if pos is not None:
                    b.update(turn, pos)
                    if turn == 1:
                        turn = 2
                    else:
                        turn = 1
                elif pyg.mouse.get_pos()[0] < menu_button_size[0] and pyg.mouse.get_pos()[1] < menu_button_size[1]:
                    print("XD")
                    mainMenu(main_font)

        display.fill(BLACK)
        drawGrid(grid_params, b, xo_font)
        menu_button_size = drawSideBar(main_font,turn)
        pyg.display.update()

        clock.tick(60)

        if turn == 1:
            #start = time.time_ns()
            b.update(1,ai1.minimax(b))
            turn = 2
            #end = time.time_ns()
            #print("MiniMax time : ", end - start, "ns")
        else:
            b.update(2,ai2.minimax(b))
            turn = 1

    # -------------------------end of main loop-----------------------

# -------------------------GLOBAL VARIABLES---------------------------


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
img_x = 0
img_o = 0
width = 800
height = 600
score = [0,0,0]
fullscreen = False
pvp_on_start = True
console = False
game_number = 0
start_size = 0


# -------------------------END OF GLOBAL VARIABLES--------------------

config = open("config", 'r')
for x in config:    exec(x)
config.close()
while True:
    if pyg.display is None: break
    if not console:
        pyg.init()
        display = pyg.display.set_mode((width, height))
        pyg.font.init()
        main_font = pyg.font.SysFont("Comic Sans", 30)
        run()
    else:
        if ttt_console.run() == 0: break
exit()
