import matplotlib.pyplot as plt
import matplotlib

# 设置全局字体为微软雅黑
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'

# 示例数据
categories = ['A', 'B', 'C', 'D']
values = [25, 30, 20, 15]

# 创建柱状图
plt.figure(figsize=(8, 6))
plt.bar(categories, values, color=['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'])

# 添加标题和标签，并设置字体
plt.title('示例柱状图')
plt.xlabel('类别')
plt.ylabel('值')

# 显示图形
plt.show()