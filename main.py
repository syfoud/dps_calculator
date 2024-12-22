from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication
import sys

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dps_calculator.ui', self)

    def sayHi(self):  # 槽函数
        print("hi")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())