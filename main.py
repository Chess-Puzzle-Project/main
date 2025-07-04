from PyQt5.QtWidgets import QApplication
import sys, ui, puzzles_database


class Main:
    def __init__(self):
        self.data = puzzles_database.PuzzlesDatabase()
        self.window = ui.MainWindow()

        self.puzzle = self.data.get_random_puzzle()
        self.board = self.puzzle.board
        self.window.draw_pieces(self.board)
        self.moves = self.puzzle.moves.split(' ')
        self.move_num = 0
        print(self.moves)

        for btn in self.window.buttons:
            btn.clicked.connect(self.on_btn_click)

        self.selected_piece = -1
        
    def on_btn_click(self):
        clicked_btn = self.window.sender()

        if self.selected_piece == -1:
            if self.puzzle.board[clicked_btn.id] != '':
                self.selected_piece = clicked_btn.id
                self.color_board()
        else:
            if clicked_btn.id == self.selected_piece:
                self.selected_piece = -1
                self.color_board()
            else:
                if self.selected_piece == self.sq_to_index(self.moves[self.move_num][0:2]) and clicked_btn.id == self.sq_to_index(self.moves[self.move_num][2:]):
                    if self.move_num < len(self.moves) - 1:
                        self.change_board(self.selected_piece, clicked_btn.id)
                        self.window.draw_pieces(self.board)
                        self.move_num += 1
                        self.selected_piece = -1
                        self.color_board()
                    else:
                        print("win")
                else:
                    print("lose")
    
    def color_board(self):
        for i in range(64):
            if i == self.selected_piece:
                self.window.buttons[i].setStyleSheet("background: #f7f757; border: none")
            else:
                self.window.buttons[i].setStyleSheet("background: " + self.window.buttons[i].color + "; border: none")

    def change_board(self, index1, index2):
        self.board[index2] = self.board[index1]
        self.board[index1] = ""

    def sq_to_index(self, square):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return letters.index(square[0]) + (8 - int(square[1])) * 8

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())