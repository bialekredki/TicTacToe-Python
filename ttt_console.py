import ttt_board
import ttt_player

def run():
    b = ttt_board.Board()
    player1 = ttt_player.Player(1)
    player2 = ttt_player.Player(2)

    turn = 1
    while True:
        b.display()
        check = b.checkForEndgame()
        if check != -1 :
            if check == 1: print("Player 1 won.")
            elif check == 2: print("Player 2 won.")
            else: print("Draw.")
            break
        if turn == 1 :
            b.update(turn, player1.makeMove(b.size))
            turn = 2
        else :
            b.update(turn, player2.makeMove(b.size))
            turn = 1
    return 0



