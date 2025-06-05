#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 参数配置
COMPLETE_LIST = 'complete_bgcs.txt'
GENOME_BGC_COUNTS = 'bgc_count_per_genome.tsv'
TOTAL_BGC = 7826  # 或根据你的实际输出修改

# 读取完整 BGC 列表
with open(COMPLETE_LIST) as f:
    paths = [l.strip() for l in f if l.strip()]

# 提取包含完整 BGC 的基因组 ID
mOTUs_complete = [os.path.basename(os.path.dirname(p)) for p in paths]
unique_mOTUs = sorted(set(mOTUs_complete))

# 读入每个基因组预测到的BGC总数（含0）
df_counts = pd.read_csv(GENOME_BGC_COUNTS, sep='\t')
total_genomes = df_counts.shape[0]

# 统计
complete_bgcs = len(paths)
fragmented_bgcs = TOTAL_BGC - complete_bgcs
n_genomes_with_complete = len(unique_mOTUs)
prop_genomes_with_complete = n_genomes_with_complete / total_genomes

# 1. 饼图：Complete vs Fragmented
plt.figure(figsize=(5,5))
plt.pie(
    [complete_bgcs, fragmented_bgcs],
    labels=['Complete', 'Fragmented'],
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Complete vs Fragmented BGCs')
plt.savefig('complete_vs_fragmented_pie.png')
plt.close()

# 2. 柱状图：含 vs 不含 完整BGC的基因组数
plt.figure(figsize=(6,4))
plt.bar(
    ['With Complete BGC', 'Without'],
    [n_genomes_with_complete, total_genomes - n_genomes_with_complete],
    color=['#4CAF50','#F44336']
)
plt.ylabel('Number of Genomes')
plt.title('Genomes with vs without Complete BGC')
plt.tight_layout()
plt.savefig('genomes_with_complete_bgc.png')
plt.close()

# 3. 保存基因组列表 & 汇总
df_genomes = pd.DataFrame(unique_mOTUs, columns=['mOTU ID'])
df_genomes.to_csv('genomes_with_complete_bgc.tsv', sep='\t', index=False)

with open('complete_bgc_summary.txt','w') as f:
    f.write(f"Total BGCs: {TOTAL_BGC}\n")
    f.write(f"Complete BGCs: {complete_bgcs}\n")
    f.write(f"Fragmented BGCs: {fragmented_bgcs}\n\n")
    f.write(f"Total genomes: {total_genomes}\n")
    f.write(f"Genomes with ≥1 Complete BGC: {n_genomes_with_complete} "
            f"({prop_genomes_with_complete:.1%})\n")

print("Done. Outputs:")
print(" - complete_vs_fragmented_pie.png")
print(" - genomes_with_complete_bgc.png")
print(" - genomes_with_complete_bgc.tsv")
print(" - complete_bgc_summary.txt")
