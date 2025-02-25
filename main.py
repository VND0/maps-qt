import sys

from PyQt6.QtGui import QPixmap, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow

from desisn import Ui_MainWindow
from tools import to_api_ll, get_image, ApiException


class MapApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_app()
        self.add_shortcuts()

    def set_map_image(self):
        elements = get_image(self.api_key, to_api_ll(*self.ll), self.zoom)
        map_pixmap = QPixmap()
        map_pixmap.loadFromData(elements, "PNG")
        self.map_lbl.setPixmap(map_pixmap)

    def init_app(self):
        self.ll = 61.668797, 50.836497
        self.api_key = "d94029a4-b4b6-48db-b4b3-cc9085862f55"
        self.zoom = 15

        try:
            self.set_map_image()
        except ApiException:
            self.statusbar.showMessage(str(ApiException))

    def add_shortcuts(self):
        self.pg_up = QShortcut(QKeySequence("PgUp"), self)
        self.pg_up.activated.connect(lambda: self.change_zoom(1))
        self.pg_down = QShortcut(QKeySequence("PgDown"), self)
        self.pg_down.activated.connect(lambda: self.change_zoom(-1))

    def change_zoom(self, how: int):
        backup = self.zoom
        self.zoom += how
        try:
            assert 0 <= self.zoom <= 21
            self.set_map_image()
            self.statusbar.clearMessage()
        except (ApiException, AssertionError):
            self.statusbar.showMessage("Достигнуто предельное значение масштаба")
            self.zoom = backup


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
