import ttt_board
import ttt_ai


def EndConditionTest3():
    size = 3
    test0 = [1, 1, 1, 0, 0, 0, 0, 0, 0] # horizontal win for player 1
    test1 = [1, 0, 0, 1, 0, 0, 1, 0, 0] # vertical win for player 1
    test2 = [1, 0, 0, 0, 1, 0, 0, 1, 1] # diagonal win for player 1
    test3 = [1, 2, 1, 2, 1, 2, 1, 1, 2] # draw
    test4 = [0, 0, 2, 0, 2, 0, 2, 0, 0] # diagonal win for player 2
    test5 = [0, 0, 2, 0, 2, 0, 1, 0, 0] # game continues
    if(
        ttt_board.Board(test0, size).checkForEndgame() == 1 and
        ttt_board.Board(test1, size).checkForEndgame() == 1 and
        ttt_board.Board(test2, size).checkForEndgame() == 1 and
        ttt_board.Board(test3, size).checkForEndgame() == 0 and
        ttt_board.Board(test4, size).checkForEndgame() == 2 and
        ttt_board.Board(test5, size).checkForEndgame() == -1 ): return True
    return False

def AITest0():
    ai_player = ttt_ai.AI(1)

    test0 = [1,2,2, 1,0,2, 0,0,1]
    test1 = [1,0,0, 1,2,2, 0,1,1]
    test2 = [2,1,1, 1,2,0, 1,0,0]
    test3 = [0,0,0, 0,2,0, 0,0,0]
    test4 = [1,0,0, 0,2,0, 0,0,2]
    test5 = [1,2,0, 0,2,0, 0,0,0]
    test6 = [2,1,1,2, 1,2,1,0, 0,0,0,0, 0,0,0,0]
    b = ttt_board.Board(test6, size=4)
    b.display()
    print(ai_player.minimax(b))
    print(b.getState()[4])

def evalTest():
    ai_player = ttt_ai.AI(1)
    test0 = [1,0,1, 2,2,0, 0,0,0]
    test1 = [1,0,0, 2,2,1, 0,0,0]
    b = ttt_board.Board(test1,size=3)
    b.display()
    print("Eval v",b.evaluateVertical(1))
    print("Eval h", b.evaluateHorizontal(1))
    print("Eval d", b.evaluateDiagonal(1))
    print("Eval -v",b.evaluateVertical(2))
    print("Eval -h", b.evaluateHorizontal(2))
    print("Eval -d", b.evaluateDiagonal(2))
    print("Eval", b.evaluate(1))

#print(EndConditionTest3())
# AITest0()
evalTest()
