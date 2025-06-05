import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
bgc_type_counts = pd.read_csv('bgc_type_counts.csv', header=None, names=['BGC_Type', 'Count'])
complete_bgc_type_counts = pd.read_csv('conplete_bgc_type_counts.csv')

# 计算比例
bgc_type_counts['Proportion'] = bgc_type_counts['Count'] / bgc_type_counts['Count'].sum()
complete_bgc_type_counts['Proportion'] = complete_bgc_type_counts['Count'] / complete_bgc_type_counts['Count'].sum()

# 创建子图
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# 绘制第一个柱状图：bgc_type_counts
ax[0].bar(bgc_type_counts['BGC_Type'], bgc_type_counts['Proportion'], color='skyblue')
ax[0].set_title('BGC Types Proportion in All BGCs')
ax[0].set_xlabel('BGC Type')
ax[0].set_ylabel('Proportion')
ax[0].tick_params(axis='x', rotation=45)

# 绘制第二个柱状图：complete_bgc_type_counts
ax[1].bar(complete_bgc_type_counts['BGC_Type'], complete_bgc_type_counts['Proportion'], color='salmon')
ax[1].set_title('BGC Types Proportion in Complete BGCs')
ax[1].set_xlabel('BGC Type')
ax[1].set_ylabel('Proportion')
ax[1].tick_params(axis='x', rotation=45)

# 显示图形
plt.tight_layout()
plt.show()
