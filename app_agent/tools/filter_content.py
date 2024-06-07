import json
import re


# 将文本中的方括号内的内容和数组内容提取出来
def extract_array_data_from_text(text):
    # 使用正则表达式匹配第一个方括号内的数组数据
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, text)

    if match:
        array_data = []
        match_str = match.group(1)
        # 替换中文逗号为英文逗号
        match_str = match_str.replace('，', ',')
        # 使用逗号分割数组元素
        elements = [elem.strip('"') for elem in match_str.split(',')]
        array_data.extend(elements)
        return array_data
    else:
        return []


# 从文本中提取 JSON 数据
def extract_json_from_text(input_string):
    # 正则表达式匹配JSON字符串
    # 正则表达式匹配最外层的JSON对象
    json_regex = re.compile(r'({.*})', re.DOTALL)

    # 查找所有匹配的JSON字符串
    matches = json_regex.findall(input_string)

    for match in matches:
        try:
            # 尝试解析匹配的字符串为JSON对象
            json.loads(match)
            # 如果解析成功，返回这个JSON字符串
            return match
        except json.JSONDecodeError:
            # 如果解析失败，继续尝试下一个匹配
            continue

    # 如果没有找到有效的JSON对象，返回提示信息
    return "No valid JSON found"
