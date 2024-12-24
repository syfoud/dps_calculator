import shutil

from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QIcon, QPixmap, QCursor, QPalette, QBrush, QDesktopServices, QFontDatabase
from PyQt6.QtWidgets import QApplication, QListWidgetItem, QFileDialog, QLabel, QSizePolicy, QWidget, QVBoxLayout
from json_load import load_json_file
import sys
import os
import json
def create_icon(color, mode):
    """
    绘制图表
    :param color: Q color
    :param mode: "-" "x" "<-" "->"
    :return:
    """
    pixmap = QtGui.QPixmap(16, 16)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    # 绘制图标
    painter.setPen(QtGui.QPen(color, 2))
    match mode:
        case "x":
            painter.drawLine(3, 3, 13, 13)
            painter.drawLine(3, 13, 13, 3)
        case "-":
            painter.drawLine(3, 8, 13, 8)
        case "<-":
            painter.drawLine(2, 8, 14, 8)  # 主线
            painter.drawLine(2, 8, 6, 4)  # 左上角
            painter.drawLine(2, 8, 6, 12)  # 左下角
        case "->":
            painter.drawLine(2, 8, 14, 8)  # 主线
            painter.drawLine(14, 8, 10, 4)  # 右上角
            painter.drawLine(14, 8, 10, 12)  # 右下角
        case _:
            pass

    painter.end()

    return QtGui.QIcon(pixmap)

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('dps_calculator.ui', self)
        self.cards={}
        self.edit_card=''
        self.cache_path = os.path.join(os.path.dirname(__file__), 'cache')





        self.set_image('picture/ui/bag.png', self.Bag)
        self.set_image('picture/ui/logo.png', self.Title_Logo)
        self.set_image('picture/ui/shovel.png', self.shovel)
        self.set_image('picture/ui/飞行路障鼠【特殊-路障】.png', self.obstacle)
        self.set_image('picture/ui/章鱼小丸子.png', self.people)

        # 设置 QTableWidget 的背景图片
        # self.set_table_background('picture/map/美味岛/色拉岛（陆）.jpg', self.battle_ground, (368, 85, 670, 600),22)

        # 初始化鼠标样式状态
        self.mouse_active = "cursor"
        # 记忆化人物位置
        self.current_people_position = None
        # 初始化障碍位置集合
        self.obstacle_positions = set()
        #无边框设计
        self.set_no_border()
        self.set_common_theme()
        # 根据系统样式,设定开关图标
        self.set_exit_and_minimized_btn_icon()
        # 连接槽函数
        self.shovel.clicked.connect(lambda: self.toggle_cursor("shovel", 'picture/ui/shovel.png'))
        self.obstacle.clicked.connect(lambda: self.toggle_cursor("obstacle", 'picture/ui/飞行路障鼠【特殊-路障】.png'))
        self.people.clicked.connect(lambda: self.toggle_cursor("people", 'picture/ui/章鱼小丸子.png'))
        self.map_change.clicked.connect(self.set_background_image)
        self.Bag.clicked.connect(self.load_cards)

        # 连接卡组点击事件
        self.cardlist.itemClicked.connect(self.on_card_clicked)

        self.close_map.clicked.connect(self.clear_table_background)

        self.battle_ground.cellClicked.connect(self.on_cell_clicked)

        self.Title_Logo.clicked.connect(self.open_github_page)

    def on_card_clicked(self, item):
        # 获取 QWidget 容器
        widget = self.cardlist.itemWidget(item)
        # 从 QWidget 中找到 QLabel 并获取卡的名称
        label_name = widget.findChild(QLabel, "card")
        if label_name:
            card_name = label_name.text()
            # 构建卡的图片路径
            image_path = os.path.join(self.cache_path, 'cardphoto', f"{card_name}.png")
            unknown_path = os.path.join(self.cache_path, 'cardphoto', "未知.png")

            # 检查图片是否存在
            if os.path.exists(image_path):
                # 设置鼠标图标
                pixmap = QPixmap(image_path)
                cursor = QCursor(pixmap)
                self.setCursor(cursor)
                self.mouse_active = "card"
                self.edit_card=card_name
            else:
                pixmap = QPixmap(unknown_path)
                cursor = QCursor(pixmap)
                self.setCursor(cursor)
                self.mouse_active = "card"
                self.edit_card=card_name
        else:
            print("未找到卡的名称标签")

    def open_github_page(self):
        url = QUrl("https://github.com/syfoud/dps_calculator")  # 替换为你的项目地址
        QDesktopServices.openUrl(url)

    def clear_obstacles(self):
        # 使用集合中的位置清空障碍图像
        for row, col in self.obstacle_positions:
            self.battle_ground.setCellWidget(row, col, None)
        # 清空集合
        self.obstacle_positions.clear()
    def load_obstacles(self, map_name):
        # 清空所有障碍图像
        self.clear_obstacles()
        # 读取障碍信息

        with open('data/obstacle/obstacle_info.json', 'r', encoding='utf-8') as file:
            obstacle_data = json.load(file)

        # 获取指定地图的障碍位置
        obstacles = obstacle_data.get(map_name, [])

        # 在 battle_ground 上绘制障碍
        for obstacle in obstacles:
            row, col = map(int, obstacle.split('-'))
            self.add_image_to_cell('picture/ui/飞行路障鼠【特殊-路障】.png', col - 1, row - 1)
            self.obstacle_positions.add((col - 1, row - 1))

    def set_exit_and_minimized_btn_icon(self):
        """
        设置退出按钮和最小化按钮样式，需已获取主题
        :return:
        """
        # 根据系统样式,设定开关图标
        color = QtGui.QColor(15, 15, 15)
        self.Button_Exit.setIcon(create_icon(color=color, mode="x"))
        self.Button_Minimized.setIcon(create_icon(color=color, mode="-"))
    def set_common_theme(self):

        style_sheet = self.styleSheet()
        # 增加边框
        style_sheet += "#MainFrame{border-radius: 8px; border: 1px solid #3c3d3e;} "
        style_sheet = self.styleSheet()
        style_sheet += "#MainFrame{background-color: #FFFFFF;}"

        self.setStyleSheet(style_sheet)

    def set_no_border(self):
        # 设置无边框窗口
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # 设背景为透明
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    def update_cardlist(self, cards):
        # 清空当前的cardlist
        self.cardlist.clear()
        default_dir = os.path.join(os.path.dirname(__file__), 'picture', 'card')


        # 提取id和name并添加到cardlist
        for card in cards.get('card', {}).get('default', []):
            # 创建一个QWidget作为QListWidgetItem的容器
            image_path = os.path.join(default_dir, f"{card['name']}.png")
            if not os.path.exists(image_path):
                image_path = os.path.join(default_dir, "未知.png")
            widget = QWidget()
            layout = QVBoxLayout()
            # 设置布局的边距为0，减少间距
            layout.setContentsMargins(2, 0, 2, 0)
            # 创建一个QLabel来显示卡片名字
            label_name = QLabel(card['name'])
            label_name.setObjectName("card")
            label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置文本居中
            layout.addWidget(label_name)
            # 创建一个QLabel来显示图片
            label_image = QLabel()
            pixmap = QPixmap(image_path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label_image)



            # 设置布局到QWidget
            widget.setLayout(layout)

            # 创建一个QListWidgetItem并设置其大小
            item = QListWidgetItem(self.cardlist)
            item.setSizeHint(widget.sizeHint())

            # 将QWidget添加到QListWidget
            self.cardlist.addItem(item)
            self.cardlist.setItemWidget(item, widget)
            # item = QListWidgetItem(f"{card['name']}")
            # self.cardlist.addItem(item)
            # item.setSizeHint(QSize(50, 100))
    def load_cards(self):
        self.cards = load_json_file(self)
        if self.cards:
            self.update_cardlist(self.cards)
            self.clear_cardphoto_cache()
            self.copy_card_images_to_cache(self.cards)
        # print("JSON数据已成功加载:", self.cards)
    def clear_cardphoto_cache(self):
        # 清空 cardphoto 文件夹
        for filename in os.listdir(os.path.join(self.cache_path, 'cardphoto')):
            file_path = os.path.join(os.path.join(self.cache_path, 'cardphoto'), filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    def copy_card_images_to_cache(self, cards):
        default_dir = os.path.join(os.path.dirname(__file__), 'picture', 'card_battle')
        cache_path = os.path.join(self.cache_path, 'cardphoto')
        for card in cards.get('card', {}).get('default', []):
            image_name = f"{card['name']}.png"
            source_path = os.path.join(default_dir, image_name)
            destination_path = os.path.join(cache_path, image_name)

            if os.path.exists(source_path):
                shutil.copy2(source_path, destination_path)
            else:
                pass
        shutil.copy2(os.path.join(default_dir, "未知.png"), os.path.join(cache_path, "未知.png"))

    def on_cell_clicked(self, row, column):
        if self.mouse_active == "shovel":
            # 清除单元格中的图片
            self.battle_ground.setCellWidget(row, column, None)
            # 从集合中移除该位置
            if (row, column) in self.obstacle_positions:
                self.obstacle_positions.remove((row, column))
        else:
            if self.mouse_active == "obstacle":
                image_path = 'picture/ui/飞行路障鼠【特殊-路障】.png'
                # 将位置添加到集合中
                self.obstacle_positions.add((row, column))
                self.add_image_to_cell(image_path, row, column)
            elif self.mouse_active == "people":
                self.remove_previous_image(self.current_people_position)
                self.current_people_position = (row, column)
                image_path = 'picture/ui/章鱼小丸子.png'
                self.add_image_to_cell(image_path, row, column)
            elif self.mouse_active == "card":
                # 获取卡片图片路径
                card_name = self.edit_card
                image_path = os.path.join(self.cache_path, 'cardphoto', f"{card_name}.png")

                # 检查图片是否存在
                if os.path.exists(image_path):
                    self.add_image_to_cell(image_path, row, column)
                else:
                    self.add_text_to_cell(card_name, row, column)
            else:
                return



    def add_text_to_cell(self, text, row, column):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 将 QLabel 添加到单元格中
        self.battle_ground.setCellWidget(row, column, label)
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
            self.set_table_background(file_path, self.battle_ground, (368, 85, 670, 600), 1.05)
            map_name = os.path.splitext(os.path.basename(file_path))[0]
            self.load_obstacles(map_name)
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

    def toggle_cursor(self, mode, image_path):
        if self.mouse_active != mode:
            pixmap = QPixmap(image_path)
            cursor = QCursor(pixmap)
            self.setCursor(cursor)
            self.mouse_active = mode
        else:
            self.unsetCursor()
            self.mouse_active = "cursor"
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            # 移动窗口
            self.move(self.pos() + self._endPos)

    # 鼠标按下事件
    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        # 根据鼠标按下时的位置判断是否在QFrame范围内
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "FrameTitle":
            # 判断鼠标按下的是左键
            if a0.button() == QtCore.Qt.MouseButton.LeftButton:
                self._isTracking = True
                # 记录初始位置
                self._startPos = QtCore.QPoint(a0.pos().x(), a0.pos().y())

    # 鼠标松开事件
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.MouseButton.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None



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
    # 加载自定义字体
    font_path = os.path.join(os.path.dirname(__file__), 'resources', 'font', 'font.ttf')
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        raise ("Failed to load font.")
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QtGui.QFont(font_family, 10)
        app.setFont(font)
    myapp = MyApp()
    myapp.font=font
    myapp.show()
    sys.exit(app.exec())
