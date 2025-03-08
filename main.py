import sys
from decimal import Decimal
from typing import Literal

from PyQt6.QtGui import QPixmap, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow
from tools import to_api_ll, get_image, ApiException, to_api_spn


class MapApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_app()
        self.add_shortcuts()

    def set_map_image(self):
        elements = get_image(self.api_key, to_api_ll(*self.ll), to_api_spn(self.spn), self.map_theme)
        map_pixmap = QPixmap()
        map_pixmap.loadFromData(elements, "PNG")
        self.map_lbl.setPixmap(map_pixmap)

    def init_app(self):
        self.ll = Decimal("61.668797"), Decimal("50.836497")
        self.api_key = "d94029a4-b4b6-48db-b4b3-cc9085862f55"
        self.map_theme = "light"
        self.spn = Decimal("0.05")

        self.theme_switcher.clicked.connect(self.change_map_theme)

        try:
            self.set_map_image()
        except ApiException as e:
            self.statusbar.showMessage(str(e))

    def add_shortcuts(self):
        # Scaling
        self.pg_up = QShortcut(QKeySequence("PgUp"), self)
        self.pg_up.activated.connect(lambda: self.change_spn(-1))
        self.pg_down = QShortcut(QKeySequence("PgDown"), self)
        self.pg_down.activated.connect(lambda: self.change_spn(1))
        # Moving
        self.arrow_right = QShortcut(QKeySequence("Right"), self)
        self.arrow_right.activated.connect(lambda: self.change_ll("R"))
        self.arrow_up = QShortcut(QKeySequence("Up"), self)
        self.arrow_up.activated.connect(lambda: self.change_ll("U"))
        self.arrow_left = QShortcut(QKeySequence("Left"), self)
        self.arrow_left.activated.connect(lambda: self.change_ll("L"))
        self.arrow_down = QShortcut(QKeySequence("Down"), self)
        self.arrow_down.activated.connect(lambda: self.change_ll("D"))

    def change_map_theme(self):
        self.map_theme = "dark" if self.map_theme == "light" else "light"
        self.set_map_image()

    def change_spn(self, how: int):
        backup = self.spn
        if how == 1:
            self.spn *= 2
        else:
            self.spn /= 2

        try:
            assert self.spn >= Decimal("0.0001")
            self.set_map_image()
            self.statusbar.clearMessage()
        except (ApiException, AssertionError):
            self.statusbar.showMessage("Достигнуто предельное значение масштаба")
            self.spn = backup

    def change_ll(self, direction: Literal["R", "U", "L", "D"]):
        # API: "lon,lat"
        # Storing: (lat, lon)
        backup = self.ll
        work_with = list(self.ll)
        delta = self.spn / 2

        if direction == "R":
            work_with[1] += delta
        elif direction == "U":
            work_with[0] += delta
        elif direction == "L":
            work_with[1] -= delta
        else:
            work_with[0] -= delta
        self.ll = tuple(work_with)

        try:
            assert -90 <= work_with[0] <= 90
            assert -180 <= work_with[1] <= 180
            self.set_map_image()
        except (ApiException, AssertionError) as e:
            print(str(e))
            self.ll = backup
        print(self.ll)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
