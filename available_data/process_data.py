import json

import pandas as pd
import numpy as np
import csv
def know_data( column_names,csv_file):
    """
    获取指定CSV文件中指定列的数据类型和数据范围。

    参数：
        csv_file (str): CSV文件的名称或路径。
        column_names (list): 需要分析的列名列表。

    返回：
        dict: 包含每个列的数据类型和数据范围的信息。
    """
    csv_file+='.csv'
    data_range_string='data_range'

    try:
        # 读取CSV文件
        df = pd.read_csv(csv_file)
        if not column_names:
            column_names = df.columns.tolist()
        # 检查列名是否存在
        missing_columns = [col for col in column_names if col not in df.columns]
        if missing_columns:
            raise ValueError(f"以下列名不存在于CSV文件中: {missing_columns}")

        result = {csv_file.replace(".csv",''):{}}

        for column_name in column_names:
            # 获取列的数据类型
            column_data = df[column_name]
            data_type = column_data.dtypes

            # 检查是否为日期格式字符串
            if data_type == 'object':
                try:
                    parsed_dates = pd.to_datetime(column_data, format='%Y-%m-%d', errors='coerce')
                    if parsed_dates.notna().all():
                        mapped_type = 'string(date)'
                        data_range = (
                            parsed_dates.min().strftime('%Y-%m-%d'),
                            parsed_dates.max().strftime('%Y-%m-%d')
                        )
                    else:
                        raise ValueError
                except ValueError:
                    mapped_type = 'string'
                    unique_values = column_data.dropna().unique()
                    if len(unique_values) <= 10:
                        data_range = list(unique_values)
                        data_range_string = 'All data type'

                    else:
                        sample_values = column_data.dropna().unique()[:3]
                        data_range = list(sample_values) if len(sample_values) > 0 else (None, None)
                        data_range_string = 'sampled three data'
            elif np.issubdtype(data_type, np.number):
                data_range_string = 'data_range'

                if np.issubdtype(data_type, np.integer):
                    mapped_type = 'int'
                else:
                    mapped_type = 'float'
                data_range = (column_data.min(), column_data.max())

            elif np.issubdtype(data_type, np.datetime64):
                data_range_string = 'data_range'

                mapped_type = 'string(date)'
                data_range = (
                    column_data.min().strftime('%Y-%m-%d') if pd.notnull(column_data.min()) else None,
                    column_data.max().strftime('%Y-%m-%d') if pd.notnull(column_data.max()) else None
                )
            else:
                mapped_type = '未知'
                sample_values = column_data.dropna().unique()[:3]
                data_range = list(sample_values) if len(sample_values) > 0 else (None, None)
                data_range_string='sampled three data'

            result[csv_file.replace(".csv",'')][column_name] = {
                'data_type': mapped_type,
                data_range_string: data_range
            }

        print(result)
        return result

    except FileNotFoundError:
        return {"error": f"文件 '{csv_file}' 未找到。"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"发生未知错误: {e}"}
def get_data(data_names, csv_filename):
    """
    从CSV文件中查找数据名称并返回对应行的数据，返回格式为JSON。

    :param data_names: 单个数据名称或数据名称列表
    :param csv_filename: CSV文件名
    :return: JSON格式的结果
    """
    # 确保 data_names 是列表
    csv_filename+='.csv'
    if not isinstance(data_names, list):
        data_names = [data_names]

    # 存储匹配的行
    matched_rows = []

    # 打开CSV文件
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                # 检查每行是否包含任何一个数据名称
                if any(data_name in row.values() for data_name in data_names):
                    matched_rows.append(row)

        # 转换为JSON格式
        print(json.dumps(matched_rows, ensure_ascii=False, indent=4))
        return json.dumps(matched_rows, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        return json.dumps({"error": "CSV file not found."}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

# 示例用法
# result = get_column_info("example.csv", "column_name")
# print(result)
# Step 1: Understand the relevant columns in the `weather` and `pollution` databases
# a=know_data(None,'pollution')
# b=know_data(None,'weather')
c=know_data(None,'filtered_events')

# pollution_data_query = get_data(good_pollution_condition, pollution_db)
# weather_data_query = get_data(good_weather_conditions, weather_db)