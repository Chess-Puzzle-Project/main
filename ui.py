from PyQt5.QtWidgets import QWidget



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(700, 900)

        self.show()