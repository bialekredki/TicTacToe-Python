# class containing operations on board

import copy
import math

# tiles, when 0 tile is empty, when 1 or 2 tile is occupied by player 1 or 2
class Board:

    def __init__(self, test=None, size=3, origin=None):
        if origin is None:
            if test is None:
                test = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            if test is int or len(test) != size * size:
                self.tiles = []
                for x in range(size * size):
                    self.tiles.append(0)
            else:
                self.tiles = test
            self.size = size
        else:
            copy.deepcopy(origin)

    def checkForEndgame(self):
        if self.checkForDraw():
            return 0
        for player in range(2):
            if self.checkForWin(player + 1):  return player + 1
        return -1

    def checkForDraw(self):
        counter = self.size * self.size
        for x in self.tiles:
            if x != 0:
                counter -= 1
        if counter > 0:    return False

        return True

    def checkForWin(self, player):
        if self.checkForVertical(player) or self.checkForDiagonal(player) or self.checkForHorizontal(
                player): return True
        return False

    def checkForVertical(self, player):
        for y in range(self.size):  # 0 3 6 y=0 x=0 y=0 x=1 y=0 x=2   1 4 7 y=1 x=0
            counter = 0
            for x in range(self.size):
                if self.tiles[self.size * x + y] == player: counter += 1
            if counter == self.size:
                return True
        return False

    def checkForHorizontal(self, player):
        for x in range(self.size):  # 0 1 2   3 4 5
            counter = 0
            for y in range(self.size):
                if self.tiles[x * self.size + y] == player: counter += 1
            if counter == self.size: return True
        return False

    def checkForDiagonal(self, player):
        counter = 0
        for x in range(self.size):
            if self.tiles[x * (self.size + 1)] == player: counter += 1
        if counter == self.size: return True
        counter = 0
        for x in range(1,self.size+1):
            if self.tiles[x * (self.size - 1)] == player: counter += 1
        if counter == self.size: return True
        return False

    # --------------------------------------------------------------------------------------------------------------------
    def update(self, player, index):
        if self.isMovePossible:
            self.tiles[index] = player
            return 1
        else:
            return 0

    def isMovePossible(self, player, index):
        if self.tiles[index] != 0:
            return False
        else:
            return True

    def display(self):
        column = 'A'
        row = '1'

        print("  ", end='')
        for x in range(self.size):
            print(column, end=' ')
            column = chr(ord(column) + 1)
        print()

        for x in range(self.size * self.size):
            if x % self.size == 0:
                print(row, end='|')
                row = chr(ord(row) + 1)
            if self.tiles[x] == 0:
                print(" ", end='')
            elif self.tiles[x] == 1:
                print("X", end='')
            elif self.tiles[x] == 2:
                print("O", end='')
            print("|", end='')
            if (x + 1) % self.size == 0: print()

    def getState(self):
        return self.tiles

    @staticmethod
    def copy(origin, player=None, index=None):
        if player is None or index is None:
            return copy.deepcopy(origin)
        else:
            new_board = copy.deepcopy(origin)
            new_board.update(player,index)
            return new_board

# --------------------------------------------------------------------

    def evaluateVertical(self,player):
        if player == 1: opponent = 2
        else: opponent = 1
        counter = 0
        eval = 0
        for y in range(self.size):
            if counter == self.size or counter - 1 == self.size: return math.inf
            eval += counter
            counter = 0
            for x in range(self.size):
                if self.tiles[y + x*self.size] == player: counter += 1
                elif self.tiles[y + x*self.size] == opponent:
                    counter = 0
                    break
        eval += counter
        return eval

    def evaluateHorizontal(self,player):
        if player == 1: opponent = 2
        else: opponent = 1
        counter = 0
        eval = 0
        for x in range(self.size):
            if counter == self.size or counter - 1 == self.size: return math.inf
            eval += counter
            counter = 0
            for y in range(self.size):
                if self.tiles[y + x*self.size] == player: counter += 1
                elif self.tiles[y + x*self.size] == opponent:
                    counter = 0
                    break
        eval += counter
        return eval

    def evaluateDiagonal(self,player):
        if player == 1: opponent = 2
        else: opponent = 1
        counter1 = 0
        counter2 = 0
        for x in range(self.size):
            if self.tiles[x * (self.size + 1)] == player: counter1 += 1
            elif self.tiles[x * (self.size+1)] == opponent:
                counter1 = 0
                break
        for x in range(1,self.size+1):
            if self.tiles[x * (self.size - 1)] == player: counter2 += 1
            elif self.tiles[x * (self.size - 1)] == opponent:
                counter2 = 0
                break
        return counter1 + counter2

    def evaluate(self,player):
        if player == 1: opponent = 2
        else: opponent = 1
        if self.checkForEndgame() == player: return math.inf
        return (self.evaluateVertical(player)+self.evaluateHorizontal(player)+self.evaluateDiagonal(player)-
                self.evaluateVertical(opponent)-self.evaluateHorizontal(opponent)-self.evaluateDiagonal(opponent))


