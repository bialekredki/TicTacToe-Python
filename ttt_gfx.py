"""
    TTT_GFX_PY_
    TicTacToe-Graphics module
    Responsible for rendering and handling game's graphics.
    AUTHOR OSKAR KORGUL
"""

import pygame as pyg
import consts
import ttt_board
import centeredText as centxt
import ttt_player


def determine_colour(option:int, value:int):
    if option == value:
        return consts.CRIMSON
    else: return consts.WHITE


class GameWindow():
    def __init__(self,resolution:tuple,local:dict,board_size:int,frame_rate:int=60):
        self.local = local
        self.display = pyg.display.set_mode(resolution)
        pyg.display.set_caption(local["window"])
        pyg.font.init()
        self.main_font = pyg.font.SysFont("Comic Sans", 30)
        self.xo_font = pyg.font.SysFont("Comic Sans", self.display.get_width() // 4 - 70 * (board_size - 3))
        self.clock = pyg.time.Clock()
        self.frame_rate = frame_rate

    def calculate_grid_parameters(self,board_size:int,resolution:tuple=None):
        if resolution is None:
            resolution = self.display.get_size()
        grid_params = {
            "width": 3 * resolution[0] // 4,
            "height": 3 * resolution[1] // 4
        }
        grid_params["start x"] = (resolution[0] - grid_params["width"]) // 2
        grid_params["start y"] = (resolution[1] - grid_params["height"]) // 2
        grid_params["block size"] = grid_params["height"] // board_size
        return grid_params

    def draw_grid(self,grid_params, board):
        state = board.getState()
        for x in range(board.size):
            for y in range(board.size):
                rect = pyg.Rect(grid_params["block size"] * x + grid_params["start x"],
                                grid_params["block size"] * y + grid_params["start y"],
                                grid_params["block size"], grid_params["block size"])
                pyg.draw.rect(self.display, consts.WHITE, rect, 1)
                if state[x + y * board.size] == 1:
                    centxt.selfcenteredText(self.xo_font, "X", rect.topleft, grid_params["block size"]).draw(self.display, consts.WHITE)
                elif state[x + y * board.size] == 2:
                    centxt.selfcenteredText(self.xo_font, "O", rect.topleft, grid_params["block size"]).draw(self.display, consts.WHITE)
                else:
                    continue

    def draw_side_bar(self, player: ttt_player.Player, score: tuple):
        self.display.blit(self.main_font.render(self.local["menu"], True, consts.WHITE), (0, 0))
        menu_button_size = self.main_font.size("MENU")
        self.display.blit(
            self.main_font.render(self.local["players_turn"].format(player.player_number, player.symbol), True,
                                  consts.WHITE), (0, menu_button_size[1]))
        self.display.blit(self.main_font.render(self.local["player1_score"].format(score[1]), True, consts.WHITE),
                          (self.display.get_width() // 2, 0))
        self.display.blit(self.main_font.render(self.local["player2_score"].format(score[2]), True, consts.WHITE),
                          (self.display.get_width() // 2, menu_button_size[1]))
        self.display.blit(self.main_font.render(self.local["draw_score"].format(score[0]), True, consts.WHITE),
                          (self.display.get_width() // 2, menu_button_size[1] * 2))
        self.display.blit(self.main_font.render(self.local["exit"], True, consts.CRIMSON), (0, menu_button_size[1] * 2))


    def get_menu_button_size(self):
        return self.main_font.size("MENU")

    def resize(self,resolution:tuple,fullscreen:bool=False):
        if fullscreen:
            self.display = pyg.display.set_mode(resolution,flags=pyg.FULLSCREEN)
        else:
            self.display = pyg.display.set_mode(resolution)

    def render(self,board:ttt_board.Board=None,game_params:tuple=None,menu_params:tuple=None):
        self.display.fill(consts.BLACK)
        if board is not None and game_params is not None:
            self.draw_grid(self.calculate_grid_parameters(board.size),board)
            self.draw_side_bar(game_params[0],game_params[1])
        elif menu_params is not None:
            self.draw_main_menu(menu_params)
        pyg.display.update()
        self.clock.tick(60)

    def draw_main_menu(self,menu_params):
        # menu_params :
        # 0 -> current selection
        # 1 -> resolution option current
        # 2 -> board size current
        # 3 -> game mode current
        # 4 -> console current
        menu_button_size = self.get_menu_button_size()
        self.display.blit(self.main_font.render(self.local["menu_instruction_1"], True, consts.WHITE),(0, 0))
        self.display.blit(self.main_font.render(self.local["menu_instruction_2"], True, consts.WHITE),(0, menu_button_size[1]))
        self.display.blit(self.main_font.render(self.local["menu_instruction_3"], True, consts.WHITE),(0, menu_button_size[1] * 2))
        self.display.blit(
            self.main_font.render("{} : {}".format(self.local["menu_resolution"],self.local["opt_resolution"][menu_params[1]]),
            True, determine_colour(menu_params[0],0)), (0,menu_button_size[1]*3))
        self.display.blit(
            self.main_font.render("{} : {}".format(self.local["menu_board_size"], self.local["opt_board_size"][menu_params[2]]),
            True, determine_colour(menu_params[0], 1)),(0,menu_button_size[1]*4))
        self.display.blit(
            self.main_font.render("{} : {}".format(self.local["menu_game_mode"], self.local["opt_game_mode"][menu_params[3]]),
            True, determine_colour(menu_params[0], 2)),(0,menu_button_size[1]*5))
        self.display.blit(
            self.main_font.render("{} : {}".format(self.local["menu_console"], self.local["opt_console"][menu_params[4]]),
            True, determine_colour(menu_params[0], 3)),(0,menu_button_size[1]*6))
        self.display.blit(
            self.main_font.render(
                "{} : {}".format(self.local["menu_fullscreen"], self.local["opt_fullscreen"][menu_params[5]]),
                True, determine_colour(menu_params[0], 4)), (0, menu_button_size[1] * 7))

    def close(self,to_console:bool=False):
        pyg.display.quit()
        pyg.quit()
        if not to_console:
            exit()



def wait():
    close = False
    while not close:
        for event in pyg.event.get():
            if event.type == pyg.MOUSEBUTTONDOWN:
                close = True
            elif event.type == pyg.QUIT:
                close = True
                pyg.display.quit()
                pyg.quit()




def mousePositionToGridTile(grid_params:dict, mouse_pos:tuple, size:int):
    for x in range(size):
        for y in range(size):
            if (grid_params["block size"] * x + grid_params["start x"] < mouse_pos[0] < grid_params["block size"] * x +
                    grid_params["start x"] + grid_params[
                        "block size"] and
                    grid_params["block size"] * y + grid_params["start y"] < mouse_pos[1] < grid_params[
                        "block size"] * y + grid_params["start y"] + grid_params["block size"]):
                return x + y * size
