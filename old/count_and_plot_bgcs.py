#!/usr/bin/env python3
import os
import csv
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 1. 配置：将此处替换为你的 antismash 输出目录名称或路径
ANTISMASH_DIR = 'antismash_out'

# 2. 输出文件名称
OUTPUT_COUNT_TSV = 'bgc_count_per_genome.tsv'
OUTPUT_HIST = 'bgc_count_distribution.png'
OUTPUT_TOP10 = 'bgc_top10_genomes.png'
OUTPUT_SUMMARY = 'bgc_summary.txt'

# 3. 验证目录是否存在
if not os.path.isdir(ANTISMASH_DIR):
    raise FileNotFoundError(f"Directory '{ANTISMASH_DIR}' not found. Please check the path.")

# 4. 遍历并统计每个基因组的 BGC 数量（包含 0）
mOTUs = sorted(os.listdir(ANTISMASH_DIR))
bgc_counts = {}
for mOTU in mOTUs:
    mOTU_path = os.path.join(ANTISMASH_DIR, mOTU)
    if not os.path.isdir(mOTU_path):
        continue
    region_files = [f for f in os.listdir(mOTU_path) if f.endswith('.gbk') and '.region' in f]
    bgc_counts[mOTU] = len(region_files)

# 5. 写入 TSV 文件
with open(OUTPUT_COUNT_TSV, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['mOTU ID', 'BGC Count'])
    for mOTU, count in bgc_counts.items():
        writer.writerow([mOTU, count])
print(f"Saved counts to {OUTPUT_COUNT_TSV}")

# 6. 生成数据摘要
df = pd.DataFrame.from_dict(bgc_counts, orient='index', columns=['BGC Count'])
df.index.name = 'mOTU ID'
total_genomes = len(df)
zero_bgcs = (df['BGC Count'] == 0).sum()
with open(OUTPUT_SUMMARY, 'w') as f:
    f.write(f"Total genomes: {total_genomes}\n")
    f.write(f"Genomes without any BGC: {zero_bgcs} ({zero_bgcs/total_genomes:.1%})\n")
    f.write(f"Genomes with ≥1 BGC: {total_genomes-zero_bgcs}\n")
print(f"Written summary to {OUTPUT_SUMMARY}")

# 7. 绘制分布直方图并保存
plt.figure(figsize=(6,4))
plt.hist(df['BGC Count'], bins=range(df['BGC Count'].max()+2), edgecolor='black')
plt.title('Distribution of BGC Counts per Genome')
plt.xlabel('BGC Count')
plt.ylabel('Number of Genomes')
plt.tight_layout()
plt.savefig(OUTPUT_HIST)
print(f"Saved histogram to {OUTPUT_HIST}")
plt.close()

# 8. 绘制 Top10 Genomes 柱状图并保存
top10 = df.sort_values('BGC Count', ascending=False).head(30)
plt.figure(figsize=(8,4))
plt.bar(top10.index, top10['BGC Count'])
plt.title('Top 30 Genomes by BGC Count')
plt.xlabel('mOTU ID')
plt.ylabel('BGC Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(OUTPUT_TOP10)
print(f"Saved top 10 bar chart to {OUTPUT_TOP10}")
plt.close()
