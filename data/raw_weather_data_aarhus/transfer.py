import json
import pandas as pd


def json_list_to_csv(json_list_file, output_csv_file):
    # 读取 JSON 文件
    with open(json_list_file, 'r', encoding='utf-8') as f:
        json_list = json.load(f)

    # 将 JSON 列表转换为 Pandas DataFrame
    df = pd.DataFrame(json_list)

    # 保存为 CSV 文件，确保正确编码
    df.to_csv(output_csv_file, index=False, encoding='utf-8-sig')


# 使用示例
# 将 'input.json' 替换为您的 JSON 列表文件路径，'weather.csv' 为输出文件路径
json_list_to_csv('daily_weather.json', '../../available_data/weather.csv')
