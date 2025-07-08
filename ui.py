from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout
import users_database

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 900)

        self.vertical_layout = QVBoxLayout()
        self.username_input_box()

        self.setup_squares()

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.wrapper)
        self.vertical_layout.addLayout(self.main_layout)

        self.setLayout(self.vertical_layout)
        self.show()
    
    def draw_pieces(self, board):
        for i in range(64):
            x, y = i // 8, i % 8
            if board[i] != '':
                pass  # თუ ცარიელი არ იქნება დახატავს x * 75 და y * 75

        # Board არის 64 ელემენტიანი ლისტი სადაც R - Rook, K - King, N - knight ა.შ თუ დიდი ასოა თეთრია და თუ პატარა მაგ r შავი.
    

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
        self.input_box.setFixedSize(300, 50)
        self.vertical_layout.addWidget(self.input_box)
        self.input_box.returnPressed.connect(self.on_enter_pressed)

    def on_enter_pressed(self):
        entered_text = self.input_box.text()
        print(f"შეყვანილი მომხმარებლის სახელი: {entered_text}")
        username_exists = users_database.UsersDatabase.check_if_username_exists(entered_text)
        print(f"არსებობს მომხმარებელი? {username_exists}")
        self.input_box.clear()

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