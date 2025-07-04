from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 900)

        self.setup_squares()

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.wrapper)

        self.setLayout(self.main_layout)
        self.show()
    
    def draw_pieces(self, board):
        pass # Board არის 64 ელემენტიანი ლისტი სადაც R - Rook, K - King, N - knight ა.შ თუ დიდი ასოა თეთრია და თუ პატარა მაგ r შავი.

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
    



class SquareButton(QPushButton):
    color1 = "#eeeed2"
    color2 = "#769656"
    
    def __init__(self, id):
        super().__init__(str(id))
        self.id = id
        
        if (id % 2 == 0 and id // 8 % 2 == 0) or (id % 2 != 0 and id // 8 % 2 != 0):
            self.color = self.color1
        else:
            self.color = self.color2

        self.setFixedSize(75, 75)
        self.setStyleSheet("background: " + self.color + "; border: none")