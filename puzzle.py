class Puzzle:
    def __init__(self, puzzle_id, fen, moves, rating):
        self.puzzle_id = puzzle_id
        self.fen = fen
        self.moves = moves
        self.rating = rating
        self.board = self.fen_to_board()

    def fen_to_board(self):
        board = []
        setup_str = self.fen.split(" ")[0]
        for each in setup_str:
            if each.isdigit():
                for i in range(int(each)):
                    board.append("")

            elif each != "/":
                board.append(each)

        return board

    def __str__(self):
        return f"ID = {self.puzzle_id}\nFEN = {self.fen}\nMOVES = {self.moves}\nRATING = {self.rating}"