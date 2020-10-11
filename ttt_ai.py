# --------------------includes--------------------------
import ttt_board
import math


# ---------------end of includes---------------------------
class AI:
    def __init__(self, player: int):
        self.ai_player = player
        self.it = 0

    def minimax(self, state: ttt_board.Board, player=None, depth=0, maximizer=True):
        new_state = ttt_board.Board.copy(state)
        possible_moves = self.findPossibleMoves(new_state.getState())
        if len(possible_moves) == 9 and new_state.size == 3:    return 4
        if len(possible_moves) == 16 and new_state.size: return 1
        self.it += 1
        results = []
        if player is None : player = self.ai_player
        if player == 1:
            next_player = 2
        else:
            next_player = 1

        result = new_state.checkForEndgame()
        if len(possible_moves) == 0 or result != -1:

            if result == 0:
                return 0
            elif result == self.ai_player:
                return 1
            else:
                return -1

        """if depth > 0:
            for move in possible_moves:
                result += self.minimax(board.Board.copy(new_state, player, move), next_player, depth + 1, not maximizer)
            return result"""
        counter = 0
        maximum = 0
        minimum = 0
        if depth > 0:
            for move in possible_moves:
                results.append(self.minimax(ttt_board.Board.copy(new_state, player, move), next_player, depth + 1, not maximizer))
                if counter == 0:
                    maximum = results[0]
                    minimum = results[0]
                if results[counter] > maximum:
                    maximum = results[counter]
                elif results[counter] < minimum:
                    minimum = results[counter]
                counter += 1
            if maximizer: return maximum
            else: return minimum

        else:
            counter = 0
            maximum = 0
            best_move = 0
            for move in possible_moves:
                results.append(
                    self.minimax(ttt_board.Board.copy(new_state, player, move), next_player, depth + 1, not maximizer))
                #print(results[counter], "   ", move)
                if counter == 0:
                    maximum = results[0]
                    best_move = move
                if results[counter] > maximum:
                    maximum = results[counter]
                    best_move = move
                counter += 1
            return best_move

            """for move in possible_moves:
                if max(results) == self.minimax(board.Board.copy(new_state, player, move), next_player, depth + 1,
                                                not maximizer): return move"""

    def findPossibleMoves(self, state: list):
        result = []
        counter = 0
        for x in state:
            if x == 0:
                result.append(counter)
            counter += 1
        return result
