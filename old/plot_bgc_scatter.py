#!/usr/bin/env python3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 读取统计好的 BGC Count 表
df = pd.read_csv('bgc_count_per_genome.tsv', sep='\t')

# 计算平均数和中位数
mean_count = df['BGC Count'].mean()
median_count = df['BGC Count'].median()

# 绘制散点图
plt.figure(figsize=(10, 5))
plt.scatter(range(len(df)), df['BGC Count'], alpha=0.6, s=10)
plt.axhline(mean_count, color='red', linestyle='--', label=f'Mean = {mean_count:.2f}')
plt.axhline(median_count, color='green', linestyle=':', label=f'Median = {median_count:.2f}')
plt.title('Scatter Plot of BGC Count per Genome')
plt.xlabel('Genome Index')
plt.ylabel('BGC Count')
plt.legend()
plt.tight_layout()
plt.savefig('bgc_count_scatter.png')
plt.close()

# 输出统计结果
with open('bgc_scatter_stats.txt', 'w') as f:
    f.write(f"Mean BGC count: {mean_count:.2f}\n")
    f.write(f"Median BGC count: {median_count:.2f}\n")

print("Scatter plot saved as 'bgc_count_scatter.png'")
print("Statistics saved as 'bgc_scatter_stats.txt'")
