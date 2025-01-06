def run_code_from_string(code_str):
    """
    去掉包含的代码块标记（```python 和 ```）并运行代码

    :param code_str: str，包含代码的字符串
    :return: any，返回代码中定义的变量 searched_result 的值（如果存在）
    """
    # 去掉 ```python 和 ``` 标记
    if code_str.startswith("```python"):
        code_str = code_str[len("```python"):]
    # 直接移除最后一行的 ``` 标记
    lines = code_str.splitlines()
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    code_str = "\n".join(lines)

    # 去除可能的首尾空格
    code_str = code_str.strip()

    # 定义局部命名空间
    local_namespace = {}

    # 执行代码
    exec(code_str, globals(), local_namespace)

    # 返回 searched_result 的值（如果存在）
    return local_namespace.get("searched_result", None)

# 示例展示 globals() 的作用
example_global_var = "I am a global variable"
code_string = """```python
print('Hello from the code block!')
print(f'Accessing global variable: {example_global_var}')
new_global_var = 'I am defined within exec and now accessible globally!'
searched_result = 42
```
"""
result = run_code_from_string(code_string)

# 打印返回的 searched_result
print(result)  # 输出: 42
