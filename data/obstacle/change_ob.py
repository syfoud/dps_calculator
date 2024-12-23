import json

# 读取原始JSON文件
with open('stage_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 创建一个新的字典来存储结果
result = {}

# 遍历JSON数据以提取所需的信息
for stage in data.values():
    if isinstance(stage, dict):
        for sub_stage in stage.values():
            if isinstance(sub_stage, dict):
                for sub_sub_stage in sub_stage.values():
                    if isinstance(sub_sub_stage, dict):
                        name = sub_sub_stage.get("name")
                        obstacle = sub_sub_stage.get("obstacle", [])
                        if name:
                            result[name] = obstacle

# 将结果保存为新的JSON文件
with open('obstacle_info.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print("解析完成，结果已保存到 obstacle_info.json 文件中。")
