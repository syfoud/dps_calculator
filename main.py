from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QCursor, QPalette, QBrush
from PyQt6.QtWidgets import QApplication, QListWidgetItem, QFileDialog, QLabel, QSizePolicy
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
        self.set_image('picture/ui/飞行路障鼠【特殊-路障】.png', self.obstacle)
        self.set_image('picture/ui/章鱼小丸子.png', self.people)

        # 设置 QTableWidget 的背景图片
        self.set_table_background('picture/map/美味岛/色拉岛（陆）.jpg', self.battle_ground, (368, 85, 670, 600),22)

        # 初始化鼠标样式状态
        self.mouse_active = "cursor"
        # 记忆化人物位置
        self.current_people_position = None
        # 连接槽函数
        self.shovel.clicked.connect(self.toggle_shovel_cursor)
        self.obstacle.clicked.connect(self.toggle_obstacle_cursor)
        self.people.clicked.connect(self.toggle_people_cursor)
        self.map_change.clicked.connect(self.set_background_image)

        self.close_map.clicked.connect(self.clear_table_background)

        self.battle_ground.cellClicked.connect(self.on_cell_clicked)

    def on_cell_clicked(self, row, column):
        if self.mouse_active == "shovel":
            # 清除单元格中的图片
            self.battle_ground.setCellWidget(row, column, None)
        else:
            image_path = ''
            if self.mouse_active == "obstacle":
                image_path = 'picture/ui/飞行路障鼠【特殊-路障】.png'
            elif self.mouse_active == "people":
                self.remove_previous_image(self.current_people_position)
                self.current_people_position = (row, column)
                image_path = 'picture/ui/章鱼小丸子.png'
            else:
                print("Unknown mouse_active state")
                return

            self.add_image_to_cell(image_path, row, column)

    def remove_previous_image(self, position):
        if position is not None:
            row, column = position
            self.battle_ground.setCellWidget(row, column, None)

    def add_image_to_cell(self, image_path, row, column):
        label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # 使用固定尺寸调整图像大小
            fixed_size = QSize(60, 60)  # 设置固定尺寸
            scaled_pixmap = pixmap.scaled(fixed_size, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # 将 QLabel 添加到单元格中
            self.battle_ground.setCellWidget(row, column, label)
        else:
            print(f"Failed to load image: {self.image_path}")

    def set_background_image(self):
        default_dir = os.path.join(os.path.dirname(__file__), 'picture', 'map')
        options = QFileDialog.Option(0)
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", default_dir, "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if file_path :
            self.set_table_background(file_path, self.battle_ground, (368, 85, 670, 600), 1)
    def clear_table_background(self):
        palette = self.battle_ground.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush())
        self.battle_ground.setPalette(palette)
        self.battle_ground.setAutoFillBackground(False)  # 关闭自动填充背景
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
        if self.mouse_active!= "shovel":
            pixmap = QPixmap('picture/ui/shovel.png')
            cursor = QCursor(pixmap)
            self.setCursor(cursor)
            self.mouse_active = "shovel"
        else:
            self.unsetCursor()
            self.mouse_active = "cursor"
    def toggle_obstacle_cursor(self):
        if self.mouse_active!= "obstacle":
            pixmap = QPixmap('picture/ui/飞行路障鼠【特殊-路障】.png')
            cursor = QCursor(pixmap)
            self.setCursor(cursor)
            self.mouse_active = "obstacle"
        else:
            self.unsetCursor()
            self.mouse_active = "cursor"
    def toggle_people_cursor(self):
        if self.mouse_active!= "people":
            pixmap = QPixmap('picture/ui/章鱼小丸子.png')
            cursor = QCursor(pixmap)
            self.setCursor(cursor)
            self.mouse_active = "people"
        else:
            self.unsetCursor()
            self.mouse_active = "cursor"



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
