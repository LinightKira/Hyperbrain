import matplotlib.pyplot as plt

# 示例数据
labels = ['A', 'B', 'C', 'D']
sizes = [25, 30, 20, 25]  # 各部分大小
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']  # 各部分颜色
explode = (0, 0.1, 0, 0)  # 突出显示第二部分

# 创建饼状图
plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

# 添加标题并设置字体
plt.title('示例饼状图', fontproperties='Microsoft YaHei')

# 显示图形
plt.axis('equal')  # 使饼图为正圆形
plt.show()