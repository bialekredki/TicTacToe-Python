# --------------------includes--------------------------
import ttt_board
import math
import random
import ttt_player


# ---------------end of includes---------------------------
class AI(ttt_player.Player):
    CACHE = {}

    def __init__(self, player_number: int, symbol: chr):
        super().__init__(player_number, symbol)

    def is_AI(self):
        return True

    def is_x(self):
        return super(AI, self).is_x()

    def set_symbol(self, symbol: chr = 'X'):
        super().set_symbol(symbol)

    def minimax(self, state: ttt_board.Board, player=None, depth=0, maximizer=True, alpha=-math.inf, beta=math.inf,
                max_depth=None):
        # create deepcopy of previous state
        new_state = ttt_board.Board.copy(state)
        cache_state = (tuple(new_state.getState()), maximizer)
        if cache_state not in AI.CACHE.keys():
            AI.CACHE[cache_state] = None
        elif AI.CACHE[cache_state] is not None and depth != 0:
            return AI.CACHE[cache_state]
        possible_moves = self.findPossibleMoves(new_state.getState())

        result = new_state.checkForEndgame()
        if len(possible_moves) == 0 or result != -1:
            if result == 0:
                AI.CACHE[cache_state] = 0
                return 0
            elif result == self.is_x():
                AI.CACHE[cache_state] = 1
                return 1
            else:
                AI.CACHE[cache_state] = -1
                return -1

        # if len(possible_moves) == 9 and new_state.size == 3:    return 4
        if len(possible_moves) == 9: return random.randrange(0, 9)

        if player is None: player = self.is_x()
        if player == 1:
            next_player = 2
        else:
            next_player = 1

        if depth > 0:
            # print(depth)
            if maximizer:
                best_value = -math.inf
            else:
                best_value = math.inf
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
            AI.CACHE[cache_state] = best_value
            return best_value

        else:
            counter = 0
            maximum = 0
            best_move = 0
            results = []
            for move in possible_moves:
                result = self.minimax(ttt_board.Board.copy(new_state, player, move), next_player, depth + 1,
                                      not maximizer, alpha, beta, max_depth)
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

    def minimaxv2(self, board, depth: int = 0):
        if depth % 2 == 0:
            player = self.is_x()
            maximizer = True
        else:
            if self.is_x() == 1:
                player = 2
            else:
                player = 1
            maximizer = False
        if (board, maximizer) not in AI.CACHE.keys():
            AI.CACHE[(board, maximizer)] = None
        else:
            if AI.CACHE[(board, maximizer)] is not None and depth > 0:
                return AI.CACHE[(board, maximizer)]
        res = board.checkForEndgame()
        moves = self.findPossibleMoves(board.getState())
        if len(moves) == 9:
            return random.randrange(0, 9)
        if res != -1:
            if res == 0:
                AI.CACHE[(board, maximizer)] = 0
                return 0
            elif res == self.is_x():
                AI.CACHE[(board, maximizer)] = 1
                return 1
            else:
                AI.CACHE[(board, maximizer)] = -1
                return -1
        else:
            vals = []
            for move in moves:
                nstate = ttt_board.Board.copy(board, player, move)
                val = self.minimaxv2(nstate, depth + 1)
                if val == 1 and maximizer:
                    return val
                elif val == -1 and not maximizer:
                    return val
                vals.append(val)
            if maximizer:
                best_val = max(vals)
            else:
                best_val = min(vals)
            if depth > 0:
                AI.CACHE[(board, maximizer)] = best_val
                return best_val
            else:
                index = vals.index(best_val)
                return moves[index]
