code_str = """
a = 12
def my_function():
    return a + 1  # 修正了语法错误

aaa = my_function()
"""

local_namespace = {}
exec(code_str, globals(), local_namespace)

# 从 local_namespace 获取变量 aaa
print(local_namespace.get("aaa", None))
