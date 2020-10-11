class Player:

    def __init__(self, number):
        self.number = number

    def makeMove(self, size):
        print("Player ", self.number, "'s turn")
        while True:
            str_move = input("Choose column(capital letter) and row(number) example : A2, B3 etc.")
            if len(str_move) != 2 or str_move[0] < 'A' or str_move[0] > chr(ord('A')+(size-1)) or str_move[1] > chr(ord('1')+(size-1)) or str_move[1] < '1':
                print("Improper input.")
                continue
            else:
                break
        return (ord(str_move[0]) - 65) + (ord(str_move[1]) - 49) * size
