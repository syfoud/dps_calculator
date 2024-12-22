from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QListWidgetItem
import sys

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dps_calculator.ui', self)

        # 添加一些项
        for i in range(1,22):
            item = QListWidgetItem(f"card {i}")
            self.cardlist.addItem(item)

            # 设置每个项的大小
            item.setSizeHint(QSize(50, 100))

    def sayHi(self):  # 槽函数
        print("hi")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())