import pandas as pd

def add_ratio_column(input_csv, output_csv):
    try:
        # 读取CSV文件
        df = pd.read_csv(input_csv)

        # 检查是否存在需要的列
        if 'vehiclecount' not in df.columns or 'totalspaces' not in df.columns:
            print("Error: Columns 'vehiclecount' and 'totalspaces' are required in the CSV file.")
            return

        # 计算新列的值并添加到DataFrame
        df['vehiclecount_totalspaces_ratio'] = df['vehiclecount'] / df['totalspaces']

        # 保存修改后的DataFrame到新文件
        df.to_csv(output_csv, index=False)
        print(f"New column added successfully. Saved to {output_csv}")

    except FileNotFoundError:
        print("Error: The input CSV file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 示例用法
input_csv = r'C:\Users\admin\Desktop\my_project\chat\data\parking.csv'   # 输入文件名
output_csv = r'C:\Users\admin\Desktop\my_project\chat\data\parking2.csv' # 输出文件名
add_ratio_column(input_csv, output_csv)
