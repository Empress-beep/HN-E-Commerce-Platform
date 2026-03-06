import pandas as pd
import numpy as np
# 绘图模块
import matplotlib.pyplot as plt
# 可视化模块
import seaborn as sns
# 警告模块
import warnings
# 忽略所有警告信息
warnings.filterwarnings('ignore')

# 设置中文字体，(避免图表中文乱码)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 解决数据输出时，列名不对齐的问题
pd.set_option('display.unicode.east_asian_width', True)

# 加载数据
df = pd.DataFrame(pd.read_csv('招标公告.csv', encoding='utf-8'))
print(df.head())
# 查看缺失值以及类型
print(df.info())

# 数据处理————将不重要的行和列进行替换

# 将"system"替换为"系统", 增加可读性
df['平台'] = df['平台'].replace('system', '系统')

# 把“招标编号”和“平台”为空的替换为"未知"
df['招标编号'] = df['招标编号'].fillna('未知')
df['平台'] = df['平台'].fillna('未知')

# 将"创建时间"列的时间戳转换为可读性的时间
# unit: 按毫秒级转换
df['创建时间'] = pd.to_datetime(df['创建时间'], unit='ms')

# 提取年、月、日
df['创建年份'] = df['创建时间'].dt.year
df['创建月份'] = df['创建时间'].dt.month


# 开始数据清洗

# 去除重复值("ID"为唯一标识)
duplicated_ins = df['公告ID'].duplicated().sum()
print('重复公告ID数量',duplicated_ins)
df = df.drop_duplicates(['公告ID'],keep='first')

# 根据上述代码info()发现“活跃时间”整列为空，删除整列空值
df = df.dropna(axis=1, how='all', inplace=False)

# 重新设置索引，因为删除了重复行，索引没有变，还是之前的索引
df = df.reset_index(drop=True)

# 数据可视化

# 分组统计数据
monthly_counts = df.groupby(['创建年份','创建月份']).size().reset_index(name='数量')
# 创建画布
plt.figure(figsize=(12,6))

# 按年份分组绘制折线
for year in monthly_counts['创建年份'].unique():
    data = monthly_counts[monthly_counts['创建年份'] == year]
    plt.plot(data['创建月份'], data['数量'], marker='o', label=f'{year}年')

plt.xlabel('月份')
plt.ylabel('招标数量')
plt.title('2018-2026年各月招标数量对比')
plt.xticks(range(1,13))  # 设置X轴刻度为1-12月
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# 导出清洗后的数据
df.to_csv('招标公告(清洗).csv', encoding='utf-8', index=False)