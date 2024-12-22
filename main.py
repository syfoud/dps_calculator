from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QCursor, QPalette, QBrush
from PyQt6.QtWidgets import QApplication, QListWidgetItem
import sys
import os

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dps_calculator.ui', self)

        # 添加一些项
        for i in range(1, 22):
            item = QListWidgetItem(f"card {i}")
            self.cardlist.addItem(item)
            item.setSizeHint(QSize(50, 100))

        self.set_image('picture/ui/bag.png', self.Bag)
        self.set_image('picture/ui/shovel.png', self.shovel)

        # 设置 QTableWidget 的背景图片
        self.set_table_background('picture/map/美味岛/色拉岛（陆）.jpg', self.battle_ground, (368, 85, 670, 600),22)

        # 初始化鼠标样式状态
        self.shovel_active = False
        # 连接槽函数
        self.shovel.clicked.connect(self.toggle_shovel_cursor)


    def set_table_background(self, image_path, table_widget, crop_rect, scale_factor):

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
            return

        cropped_pixmap = pixmap.copy(*crop_rect)
        # 缩放图片
        scaled_pixmap = cropped_pixmap.scaled(table_widget.size() * scale_factor,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        brush = QBrush(scaled_pixmap)
        palette = table_widget.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        table_widget.setPalette(palette)
        table_widget.setAutoFillBackground(True)


    def toggle_shovel_cursor(self):
        if self.shovel_active:
            self.unsetCursor()
        else:
            shovel_pixmap = QPixmap('picture/ui/shovel.png')
            shovel_cursor = QCursor(shovel_pixmap)
            self.setCursor(shovel_cursor)

        self.shovel_active = not self.shovel_active

    def set_image(self, path, name):
        icon = QIcon(path)
        if not icon.isNull():
            name.setIcon(icon)
            name.setIconSize(icon.availableSizes()[0])
            name.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
            """)
        else:
            print(f"Failed to load image: {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())
