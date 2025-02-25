import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from desisn import Ui_MainWindow
from tools import to_api_ll, to_api_spn, get_image, ApiException


class MapApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_app()

    def init_app(self):
        self.ll = 61.668797, 50.836497
        self.spn = 0.05
        self.api_key = "d94029a4-b4b6-48db-b4b3-cc9085862f55"

        try:
            elements = get_image(self.api_key, to_api_ll(*self.ll), to_api_spn(self.spn))
            map_pixmap = QPixmap()
            map_pixmap.loadFromData(elements, "PNG")
            self.map_lbl.setPixmap(map_pixmap)
        except ApiException:
            self.statusbar.showMessage(str(ApiException))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
