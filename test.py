import ttt_board
import ttt_ai
import pickle


def EndConditionTest3():
    size = 3
    test0 = [2, 1, 1, 1, 2, 2, 2, 2, 2] # horizontal win for player 1
    test1 = [1, 0, 0, 1, 0, 0, 1, 0, 0] # vertical win for player 1
    test2 = [1, 0, 0, 0, 1, 0, 0, 1, 1] # diagonal win for player 1
    test3 = [1, 2, 1, 2, 1, 2, 2, 1, 2] # draw
    test4 = [0, 0, 2, 0, 2, 0, 2, 0, 0] # diagonal win for player 2
    test5 = [0, 0, 2, 0, 2, 0, 1, 0, 0] # game continues //0 1 2 // 3 4 5 // 6 7 8
    print(ttt_board.Board(test3, size).checkForEndgame())
    if(
        ttt_board.Board(test0, size).checkForEndgame() == 2 and
        ttt_board.Board(test1, size).checkForEndgame() == 1 and
        ttt_board.Board(test2, size).checkForEndgame() == 1 and
        ttt_board.Board(test3, size).checkForEndgame() == 0 and
        ttt_board.Board(test4, size).checkForEndgame() == 2 and
        ttt_board.Board(test5, size).checkForEndgame() == -1 ): return True
    return False

def AITest0():
    ai_player = ttt_ai.AI(1, 'X')

    test0 = [1, 2, 2, 1, 0, 2, 0, 0, 1]
    test1 = [1, 0, 0, 1, 2, 2, 0, 1, 1]
    test2 = [2, 1, 1, 1, 2, 0, 1, 0, 0]
    test3 = [1, 1, 2, 2, 2, 1, 0, 0, 0]
    test4 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    test5 = [1, 2, 0, 0, 2, 0, 0, 0, 0]
    test6 = [2, 1, 1, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    b = ttt_board.Board(test4, size=3)
    b.display()
    print(ai_player.minimaxv2(b))
    b.update(ai_player.is_x(), ai_player.minimaxv2(b))
    b.display()

def evalTest():
    ai_player = ttt_ai.AI(1)
    test0 = [1,0,1, 2,2,0, 0,0,0]
    test1 = [1,0,0, 2,2,1, 0,0,0]
    test2 = [2, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2]
    b = ttt_board.Board(test2, size=4)
    b.display()
    print("Eval v", b.evaluateVertical(1))
    print("Eval h", b.evaluateHorizontal(1))
    print("Eval d", b.evaluateDiagonal(1))
    print("Eval -v", b.evaluateVertical(2))
    print("Eval -h", b.evaluateHorizontal(2))
    print("Eval -d", b.evaluateDiagonal(2))
    print("Eval", b.evaluate(1))

def XD():
    test0 = [1, 0, 1, 2, 2, 0, 0, 0, 0]
    b = ttt_board.Board(test0, size=3)
    print(b.update(1, 0))

def save_cache():
    for x in range(3, 4):
        filename = "cache{}".format(x)
        aix = ttt_ai.AI(1, 'X')
        aio = ttt_ai.AI(2, 'O')
        draws = 0
        winx = 0
        wino = 0

        for y in range(10):
            b = ttt_board.Board(size=x)
            moves = []
            while b.checkForEndgame():
                moves.append(aix.minimaxv2(b))
                b.update(aix.is_x(), moves[-1])
                moves.append(aio.minimaxv2(b))
                b.update(aio.is_x(), moves[-1])
                res = b.checkForEndgame()
                if res > 0:
                    print(b.checkForEndgame(), '\t Size ', b.size)
                    b.display()
                    print(moves)
                    if res == 1:
                        winx += 1
                    else:
                        wino += 1
                    break
                elif res == 0:
                    draws += 1
                    break
            print("XD:", y)
        print("CACHE lenght : ", len(aix.CACHE), '\tDraws ', draws, '\tWinx ', winx, '\tWino', wino)
        f = open(filename, 'wb')
        pickle.dump(aix.CACHE, f)
        f.close()


save_cache()
# AITest0()
