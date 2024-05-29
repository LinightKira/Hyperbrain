import matplotlib.pyplot as plt

# 示例数据
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 创建折线图
plt.plot(x, y, marker='o')

# 添加标题和标签
plt.title('示例折线图', fontdict={'fontname': 'Microsoft YaHei'})
plt.xlabel('X 轴', fontname='Microsoft YaHei')
plt.ylabel('Y 轴', fontname='Microsoft YaHei')

# 显示网格
plt.grid(True)

# 显示图形
plt.show()