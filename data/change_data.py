import os
import pandas as pd

# 输入文件夹路径和输出文件夹路径
input_folder = r"C:\Users\admin\Desktop\my_project\chat\data\citypulse_traffic_raw_data_aarhus_aug_sep_2014\traffic_june_sep"
output_folder = "traffic"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹内的所有CSV文件
for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 转换TIMESTAMP列格式为 YYYY-MM-DD
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP']).dt.date

        # 对于数值列，按天计算平均值并转为整数
        numeric_columns = df.select_dtypes(include=['number']).columns
        df[numeric_columns] = df.groupby('TIMESTAMP')[numeric_columns].transform('mean').round().astype(int)

        # 去重：只保留每天的第一条记录
        df = df.drop_duplicates(subset='TIMESTAMP')

        # 保存文件到输出文件夹
        output_path = os.path.join(output_folder, file_name)
        df.to_csv(output_path, index=False)

print(f"所有CSV文件处理完成，结果已保存到 {output_folder}")
