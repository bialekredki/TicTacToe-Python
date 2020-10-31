# --------------------includes--------------------------
import ttt_board
import math


# ---------------end of includes---------------------------
class AI:
    def __init__(self, player: int):
        self.ai_player = player

    def minimax(self, state: ttt_board.Board, player=None, depth=0, maximizer=True, alpha=-math.inf, beta=math.inf, max_depth=None):
        new_state = ttt_board.Board.copy(state)

        possible_moves = self.findPossibleMoves(new_state.getState())
        if max_depth is None and len(possible_moves) > 5: max_depth = len(possible_moves) // new_state.size

        result = new_state.checkForEndgame()
        if len(possible_moves) == 0 or result != -1:
            if result == 0: return 0
            elif result == self.ai_player: return 1
            else: return -1

        #if len(possible_moves) == 9 and new_state.size == 3:    return 4
        #if len(possible_moves) == math.pow(new_state.size,2): return 0

        if player is None: player = self.ai_player
        if player == 1:
            next_player = 2
        else:
            next_player = 1

        if depth > 0:
            #print(depth)
            if depth == max_depth:
                if maximizer: return new_state.evaluate(player)
                else: return new_state.evaluate(player)*(-1)
            if maximizer:
                best_value = -2
            else:
                best_value = 2
            for move in possible_moves:
                result = self.minimax(ttt_board.Board.copy(new_state, player, move), next_player, depth + 1,
                                      not maximizer, alpha, beta, max_depth)
                if maximizer:
                    best_value = max(result, best_value)
                    alpha = max(best_value, alpha)
                else:
                    best_value = min(result, best_value)
                    beta = min(best_value, beta)
                if beta <= alpha: break
            return best_value

        else:
            counter = 0
            maximum = 0
            best_move = 0
            results = []
            for move in possible_moves:
                result = self.minimax(ttt_board.Board.copy(new_state, player, move), next_player, depth + 1,
                                      not maximizer, alpha, beta,max_depth)
                #print(result, "\t", move)
                if counter == 0:
                    maximum = result
                    best_move = move
                if result > maximum:
                    maximum = result
                    best_move = move
                counter += 1
            return best_move

    def findPossibleMoves(self, state: list):
        result = []
        counter = 0
        for x in state:
            if x == 0:
                result.append(counter)
            counter += 1
        return result
