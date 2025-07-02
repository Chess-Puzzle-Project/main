from PyQt5.QtWidgets import QApplication
import sys, ui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ui.MainWindow()
    sys.exit(app.exec_())