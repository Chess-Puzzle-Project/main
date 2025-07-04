from PyQt5.QtWidgets import QApplication
import sys, ui, puzzles_database


class Main:
    def __init__(self):
        self.data = puzzles_database.PuzzlesDatabase()
        self.window = ui.MainWindow()

        self.puzzle = self.data.get_random_puzzle()
        self.window.draw_pieces(self.puzzle.board)

        for btn in self.window.buttons:
            btn.clicked.connect(self.on_btn_click)
        
    def on_btn_click(self):
        clicked_btn = self.window.sender()
        print(clicked_btn.id)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())