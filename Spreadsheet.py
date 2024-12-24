import os
import pandas as pd

def find_name_in_excel(name_to_find, file_path=os.path.join(os.path.dirname(__file__), 'data', 'card', '美食大全.xlsx')):
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=0)

    # 查找名字所在的行
    result = df[df.apply(lambda row: row.astype(str).str.contains(name_to_find, case=False).any(), axis=1)]

    if not result.empty:
        # 返回找到的第一行的第一到第四列的值
        first_four_values = result.iloc[0, :4].tolist()
        return first_four_values
    else:
        return None

def add_alias_to_row(name_to_find, alias, file_path=os.path.join(os.path.dirname(__file__), 'data', 'card', '美食大全.xlsx')):
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=0)

    # 查找名字所在的行
    result = df[df.apply(lambda row: row.astype(str).str.contains(name_to_find, case=False).any(), axis=1)]

    if not result.empty:
        # 获取找到的第一行的索引
        index = result.index[0]

        # 检查最后一列是否有数据，如果有则添加别名，否则直接添加
        if pd.notna(df.iloc[index, -1]):
            df.iloc[index, -1] = f"{df.iloc[index, -1]}, {alias}"
        else:
            df.iloc[index, -1] = alias

        # 获取工作表名称
        xls = pd.ExcelFile(file_path)
        sheet_name = xls.sheet_names[0]

        # 保存修改后的Excel文件
        df.to_excel(file_path, sheet_name=sheet_name, index=False)
        print(f"别名 '{alias}' 已成功添加到名字 '{name_to_find}' 的记录中。")
    else:
        print(f"未找到名字 '{name_to_find}' 的记录。")

# 示例调用
name_to_find = '盖亚圣神'
alias = 'Gaea Saint Goddess'
add_alias_to_row(name_to_find, alias)
