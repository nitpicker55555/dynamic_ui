import pandas as pd

def get_unique_values_from_column(csv_file, column_name):
    """
    读取 CSV 文件并输出某一列的所有不重复值。

    Args:
        csv_file (str): CSV 文件路径。
        column_name (str): 要提取不重复值的列名。

    Returns:
        list: 不重复值的列表。
    """
    # 读取 CSV 文件
    df = pd.read_csv(csv_file)

    # 检查列是否存在
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the CSV file.")

    # 获取不重复值
    unique_values = df[column_name].unique()

    return unique_values

# 示例用法
csv_file_path = r'C:\Users\admin\Desktop\my_project\chat\available_data\weather.csv'  # 替换为你的 CSV 文件路径
column_name = 'weather'  # 替换为你要提取的列名

unique_values = get_unique_values_from_column(csv_file_path, column_name)
print(f"Unique values in column '{column_name}':")
print(unique_values)
