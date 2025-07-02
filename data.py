import sqlite3


class Data:
    def __init__(self):
        pass

    def get_random_board(self):
        pass

    def FEN_to_board(self, fen):
        board = []
        setup_str = fen.split(" ")[0]
        for each in setup_str:
            if each.isdigit():
                for i in range(int(each)):
                    board.append("")
            
            elif each != "/":
                board.append(each)
        
        return board