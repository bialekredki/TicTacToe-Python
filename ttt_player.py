class Player:

    def __init__(self, player_number:int):
        self.player_number = player_number

    def isAI(self):
        return False

    def make_move_console(self, size):
        print("Player ", self.number, "'s turn")
        while True:
            str_move = input("Choose column(capital letter) and row(number) example : A2, B3 etc.")
            if len(str_move) != 2 or str_move[0] < 'A' or str_move[0] > chr(ord('A')+(size-1)) or str_move[1] > chr(ord('1')+(size-1)) or str_move[1] < '1':
                print("Improper input.")
                continue
            else:
                break
        return (ord(str_move[0]) - 65) + (ord(str_move[1]) - 49) * size
