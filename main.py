from PyQt5.QtWidgets import QApplication, QLineEdit
import sys, ui, puzzles_database, users_database
from random import *
from PyQt5.QtCore import QTimer
import winsound

class Main:
    def __init__(self):
        self.data = puzzles_database.PuzzlesDatabase()
        self.users = users_database.UsersDatabase()
        self.window = ui.MainWindow(self)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.opponent_move)
        self.is_board_loaded = False


        for btn in self.window.buttons:
            btn.clicked.connect(self.on_btn_click)

        self.window.next_button.pressed.connect(self.on_next_pressed)
        self.window.answer_button.pressed.connect(self.show_answer)
        self.window.delete_user_button()
        self.window.input_box.returnPressed.connect(lambda: (
            self.window.on_enter_pressed(),
            self.load_new_puzzle(),
            self.window.delete_button.show(),
            self.window.login_button.hide()
        ))
        self.window.login_button.clicked.connect(lambda: (
            self.window.on_enter_pressed(),
            self.load_new_puzzle(),
            self.window.delete_button.show(),
            self.window.login_button.hide()
        ))

    def load_new_puzzle(self):
        if self.timer.isActive():
            self.timer.stop()

        # მოაქვს პაზლი ბაზიდან
        self.puzzle = self.data.get_next_puzzle()
        self.board = self.puzzle.board
        self.is_board_loaded = True

        self.moves = self.puzzle.moves.split(' ')
        self.move_num = 0

        self.color = self.puzzle.fen.split(' ')[1]
        if self.color == 'b':
            self.color = 'w'
        else:
            self.color = 'b'

        print(self.moves)

        self.selected_piece = -1
        self.can_click = False
        self.has_lost = False
        self.has_won = False

        if self.color == 'b':
            self.board.reverse()

        self.color_board()
        self.window.draw_pieces(self.board)
        self.timer.start(1000)
        self.window.setStyleSheet("background-color: #262626;")


    def on_btn_click(self):
        clicked_btn = self.window.sender()

        if self.selected_piece == -1:
            # როდესაც ფიგურა არ არის მონიშნული
            if self.puzzle.board[clicked_btn.id] != '' and self.board[clicked_btn.id].isupper() == (self.color == 'w') and self.can_click:
                self.selected_piece = clicked_btn.id
                self.color_board()

        elif self.can_click:
            # როდესაც სხვა ფიგურას ნიშნავ
            if self.board[clicked_btn.id] != "" and self.board[clicked_btn.id].isupper() == (self.color == 'w'):
                self.selected_piece = clicked_btn.id
                self.color_board()
            else:
                # როდესაც სვლას აკეთებ
                if self.selected_piece == self.sq_to_index(self.moves[self.move_num][0:2]) and clicked_btn.id == self.sq_to_index(self.moves[self.move_num][2:]):
                    self.change_board(self.selected_piece, clicked_btn.id)
                    self.window.draw_pieces(self.board)

                    if self.move_num < len(self.moves) - 1:
                        # თუ უბრალოდ სვლა კეთდება
                        self.move_num += 1
                        self.selected_piece = -1
                        self.color_board()
                        self.can_click = False
                        self.timer.singleShot(1000, self.opponent_move)
                        winsound.PlaySound("soundeffects/move", winsound.SND_ASYNC)
                    else:
                        # შამათი
                        self.color_board()
                        self.win()
                        winsound.PlaySound("soundeffects/checkmate", winsound.SND_ASYNC)
                else:
                    self.lose()
                    winsound.PlaySound("soundeffects/move", winsound.SND_ASYNC)
    
    def opponent_move(self):
        winsound.PlaySound("soundeffects/move", winsound.SND_ASYNC)
        self.change_board(self.sq_to_index(self.moves[self.move_num][0:2]), self.sq_to_index(self.moves[self.move_num][2:]))
        self.window.draw_pieces(self.board)

        self.move_num += 1
        self.color_board()

        # თუ მომხმარებელმა წააგო მეორდება ე.ი. აჩვენებს სწორ პასუზს
        if self.has_lost:
            if self.move_num != len(self.moves):
                self.timer.start(1000)
        else:
            self.can_click = True


    def color_board(self):
        for i in range(64):
            # მონიშნულ უჯრას აფერადებს
            if i == self.selected_piece:
                self.window.buttons[i].setStyleSheet("background: #f7f757; border: none")
            else:
                self.window.buttons[i].setStyleSheet("background: " + self.window.buttons[i].color + "; border: none")
        
        # ბოლო სვლას აფერადებს
        if self.move_num > 0:
            self.window.buttons[self.sq_to_index(self.moves[self.move_num -1][0:2])].setStyleSheet("background: #f7f757; border: none")
            self.window.buttons[self.sq_to_index(self.moves[self.move_num -1][2:])].setStyleSheet("background: #f7f757; border: none")

    def change_board(self, index1, index2):
        self.board[index2] = self.board[index1]
        self.board[index1] = ""

    def sq_to_index(self, square):
        # გადაყავს ჭადრაკის უჯრა მაგ. f4 რიცხვად 0 დან 63-ის ჩათვლით
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        index =  letters.index(square[0]) + (8 - int(square[1])) * 8

        if self.color == 'w':
            return index
        else:
            return 63 - index
    
    def show_answer(self):
        # პასუხის ნახვის არჩევის შემთხვევა
        if self.is_board_loaded and self.move_num < len(self.moves) and not self.timer.isActive() and not self.has_won:
            if not self.has_lost:
                self.lose()

            self.selected_piece = -1
            self.can_click = False
            self.timer.start(1000)
    
    def on_next_pressed(self):
        # ახალ პაზლზე გადასვლის შემთხვევა
        if self.is_board_loaded:
            if self.has_won == False and self.has_lost == False and ui.MainWindow.CURRENT_USER.elo != 0:
                ui.MainWindow.CURRENT_USER.elo = ui.MainWindow.CURRENT_USER.elo - randint(20, 50)
                self.users.update_user(*ui.MainWindow.CURRENT_USER.__str__())
                self.window.draw_user_stats(ui.MainWindow.CURRENT_USER)
            self.load_new_puzzle()


    def win(self):
        print("win")
        self.window.setStyleSheet("background-color: #0f3800;")
        self.can_click = False
        self.selected_piece = -1
        self.has_won = True
        self.color_board()
        ui.MainWindow.CURRENT_USER.puzzles_solved += 1
        ui.MainWindow.CURRENT_USER.elo = puzzles_database.PuzzlesDatabase.next_rating + randint(20,50)
        self.users.update_user(*ui.MainWindow.CURRENT_USER.__str__())
        self.window.draw_user_stats(ui.MainWindow.CURRENT_USER)

    def lose(self):
        print("lose")
        self.window.setStyleSheet("background-color: #380900;")
        self.can_click = False
        self.has_lost = True
        self.selected_piece = -1
        self.color_board()
        if ui.MainWindow.CURRENT_USER.elo != 0:
            ui.MainWindow.CURRENT_USER.elo = ui.MainWindow.CURRENT_USER.elo - randint(20, 50)
            self.users.update_user(*ui.MainWindow.CURRENT_USER.__str__())
            self.window.draw_user_stats(ui.MainWindow.CURRENT_USER)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())