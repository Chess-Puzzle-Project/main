from PyQt5.QtWidgets import QApplication
import sys, ui, puzzles_database


class Main:
    def __init__(self):
        self.data = puzzles_database.PuzzlesDatabase()
        self.window = ui.MainWindow()

        self.puzzle = self.data.get_random_puzzle()
        self.window.draw_pieces(self.puzzle.board)

        print(self.puzzle.moves[:2])
        print(self.sq_to_index("b2"))

        for btn in self.window.buttons:
            btn.clicked.connect(self.on_btn_click)
        
    def on_btn_click(self):
        clicked_btn = self.window.sender()
        print(clicked_btn.id)
    
    def sq_to_index(self, square):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return letters.index(square[0]) + (int(square[1]) -1) * 8

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())