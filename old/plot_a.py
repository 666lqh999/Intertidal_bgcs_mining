import matplotlib
# 使用无界面后端
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
# 载入 metadata.tsv
metadata = pd.read_csv('metadata.tsv', sep='\t')


# 1. MAG 完整度分布直方图
plt.figure(figsize=(6,4))
plt.hist(metadata['Completeness (%)'], bins=20)
plt.title('Distribution of MAG Completeness')
plt.xlabel('Completeness (%)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('completeness_distribution.png')
plt.close()

# 2. 完整度 vs 污染度 散点图
plt.figure(figsize=(6,4))
plt.scatter(
    metadata['Completeness (%)'],
    metadata['Contamination (%)'],
    alpha=0.7
)
plt.title('Completeness vs Contamination')
plt.xlabel('Completeness (%)')
plt.ylabel('Contamination (%)')
plt.tight_layout()
plt.savefig('completeness_vs_contamination.png')
plt.close()

# 3. Top 10 门(Phylum)丰度柱状图
# 从 GTDB taxonomy 字段提取门级信息
metadata['Phylum'] = metadata['GTDB taxonomy'].str.extract(r'p__([^;]+)')
phylum_counts = metadata['Phylum'].value_counts().head(10)

plt.figure(figsize=(6,4))
phylum_counts.plot(kind='bar')
plt.title('Top 10 Phyla by mOTU Count')
plt.xlabel('Phylum')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('top10_phyla.png')
plt.close()