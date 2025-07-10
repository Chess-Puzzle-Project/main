from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QLabel
import users_database, user

class MainWindow(QWidget):
    CURRENT_USER = None

    def __init__(self, main):
        super().__init__()
        self.resize(600, 900)
        self.main = main
        self.stats_box = QLabel(self)
        self.setStyleSheet("background-color: #262626;")

        self.vertical_layout = QVBoxLayout()
        self.draw_user_stats()
        self.username_input_box()

        self.setup_squares()

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.wrapper)
        self.vertical_layout.addLayout(self.main_layout)

        self.pieces = {'K': 'pieces/wk.png', 'k': 'pieces/bk.png',
                       'Q': 'pieces/wq.png', 'q': 'pieces/bq.png',
                       'N': 'pieces/wn.png', 'n': 'pieces/bn.png',
                       'B': 'pieces/wb.png', 'b': 'pieces/bb.png',
                       'P': 'pieces/wp.png', 'p': 'pieces/bp.png',
                       'R': 'pieces/wr.png', 'r': 'pieces/br.png'}

        self.next_and_correct_buttons()

        self.setLayout(self.vertical_layout)
        self.show()
    
    def draw_pieces(self, board):
        for i in range(64):
            piece = board[i]
            if piece != '':
                path = self.pieces[piece]
                if piece:
                    self.buttons[i].setIcon(QIcon(path))
                    self.buttons[i].setIconSize(QSize(75, 75))
            else:
                self.buttons[i].setIcon(QIcon())
    

    def setup_squares(self):
        self.btn_layout = QGridLayout()
        self.btn_layout.setSpacing(0)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = []
        for i in range(64):
            btn = SquareButton(i)
            self.btn_layout.addWidget(btn, i // 8, i % 8)
            self.buttons.append(btn)

        self.wrapper = QWidget()
        self.wrapper.setFixedSize(600, 600)
        self.wrapper.setLayout(self.btn_layout)

    def username_input_box(self):
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("შეიყვანეთ მომხმარებლის სახელი...")
        self.input_box.setFixedHeight(50)
        self.input_box.setStyleSheet("font-size: 18px; color: white; background-color: #424242; border-radius: 20px; padding: 10px;")
        self.vertical_layout.addWidget(self.input_box)

    def on_enter_pressed(self):
        self.entered_text = self.input_box.text()
        print(f"შეყვანილი მომხმარებლის სახელი: {self.entered_text}")
        username_exists = users_database.UsersDatabase.check_if_username_exists(self.entered_text)
        print(f"არსებობს მომხმარებელი? {username_exists}")
        self.input_box.clear()

        if username_exists:
            current_user = self.main.users.return_user_as_class(self.entered_text)
            self.input_box.hide()
            self.draw_user_stats(current_user)
            MainWindow.CURRENT_USER = current_user

        else:
            new_user = user.User(self.entered_text, 0, 0)
            self.main.users.add_user(*new_user.__str__())
            self.input_box.hide()
            self.draw_user_stats(new_user)
            MainWindow.CURRENT_USER = new_user

    def draw_user_stats(self, user=None):
        if user is None:
            self.stats_box.setFixedHeight(50)
            self.stats_box.setStyleSheet(
                "font-size: 18px; color: white; background-color: #424242; border-radius: 20px; padding: 10px;")
            self.stats_box.hide()
            self.vertical_layout.addWidget(self.stats_box)
        else:
            self.stats_box.show()
            self.stats_box.setText(f"👤 {user.username}     📈 რეიტინგი: {user.elo}     ✅ ამოხსნილი პაზლები: {user.puzzles_solved}")

    def next_and_correct_buttons(self):
        self.button_layout = QHBoxLayout()
        self.answer_button = QPushButton('სწორი პასუხის ნახვა')
        self.next_button = QPushButton('შემდეგი')
        self.next_button.setFixedSize(250, 50)
        self.next_button.setStyleSheet("font-size: 20px; color: white; background-color: #424242; border-radius: 20px;")
        self.next_button.setCursor(Qt.PointingHandCursor)

        self.answer_button.setFixedSize(250, 50)
        self.answer_button.setStyleSheet("font-size: 20px; color: white; background-color: #424242; border-radius: 20px;")
        self.answer_button.setCursor(Qt.PointingHandCursor)

        self.button_layout.addWidget(self.answer_button)
        self.button_layout.addWidget(self.next_button)
        self.vertical_layout.addLayout(self.button_layout)

    def delete_user_function(self):
        username = self.entered_text
        self.main.users.delete_user(username)
        self.input_box.show()
        self.input_box.clear()
        self.stats_box.hide()
        self.delete_button.hide()

    def delete_user_button(self):
        self.delete_layout = QHBoxLayout()
        self.delete_layout.addStretch()
        self.delete_button = QPushButton('🗑️ მომხმარებლის წაშლა')
        self.delete_button.setFixedSize(270, 50)
        self.delete_button.setStyleSheet("font-size: 20px; color: red; background-color: #424242; border-radius: 20px;")
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_layout.addWidget(self.delete_button)
        self.vertical_layout.insertLayout(1, self.delete_layout)
        self.delete_button.hide()
        self.delete_button.clicked.connect(self.delete_user_function)

class SquareButton(QPushButton):
    color1 = "#eeeed2"
    color2 = "#769656"
    
    def __init__(self, id):
        super().__init__()
        self.id = id
        
        if (id % 2 == 0 and id // 8 % 2 == 0) or (id % 2 != 0 and id // 8 % 2 != 0):
            self.color = self.color1
        else:
            self.color = self.color2

        self.setFixedSize(75, 75)
        self.setStyleSheet("background: " + self.color + "; border: none")