import sys

from PyQt6.QtWidgets import QApplication, QMainWindow


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Время вспоминать QT')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
