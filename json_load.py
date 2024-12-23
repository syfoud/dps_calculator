import json
import os

from PyQt6.QtWidgets import QFileDialog


def load_json_file(win):
        default_dir = os.path.join(os.path.dirname(__file__), 'data', 'battle_plan')
        options = QFileDialog.Option(0)
        file_path, _ = QFileDialog.getOpenFileName(win, "选择JSON文件", default_dir, "JSON Files (*.json)", options=options)
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data
                    # 在这里你可以对加载的数据进行进一步处理
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
            except Exception as e:
                print(f"文件读取错误: {e}")
        else:
            return None
