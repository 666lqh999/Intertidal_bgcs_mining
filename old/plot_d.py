import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

# 1. 读取数据
df = pd.read_csv('metadata.tsv', sep='\t')

# 2. 提取并清洗
gc = df['GC (%)']
cont = df['Contamination (%)']
comp = df['Completeness (%)']
mask = gc.notna() & cont.notna() & comp.notna()
gc = gc[mask]
cont = cont[mask]
comp = comp[mask]

# 3. 计算相关系数
pearson_gc_cont = pearsonr(gc, cont)
spearman_gc_cont = spearmanr(gc, cont)
pearson_gc_comp = pearsonr(gc, comp)
spearman_gc_comp = spearmanr(gc, comp)

print(f"GC vs Contamination: Pearson r = {pearson_gc_cont[0]:.3f}, p = {pearson_gc_cont[1]:.3e}")
print(f"GC vs Contamination: Spearman ρ = {spearman_gc_cont.correlation:.3f}, p = {spearman_gc_cont.pvalue:.3e}")
print(f"GC vs Completeness: Pearson r = {pearson_gc_comp[0]:.3f}, p = {pearson_gc_comp[1]:.3e}")
print(f"GC vs Completeness: Spearman ρ = {spearman_gc_comp.correlation:.3f}, p = {spearman_gc_comp.pvalue:.3e}")

# 4. 绘制并保存散点图+拟合线
# GC vs Contamination
plt.figure()
plt.scatter(gc, cont, alpha=0.6)
m, b = np.polyfit(gc, cont, 1)
plt.plot(gc, m*gc + b, linestyle='--')
plt.xlabel('GC Content (%)')
plt.ylabel('Contamination (%)')
plt.title('GC vs Contamination')
plt.tight_layout()
plt.savefig('gc_vs_contamination.png')
plt.close()

# GC vs Completeness
plt.figure()
plt.scatter(gc, comp, alpha=0.6)
m2, b2 = np.polyfit(gc, comp, 1)
plt.plot(gc, m2*gc + b2, linestyle='--')
plt.xlabel('GC Content (%)')
plt.ylabel('Completeness (%)')
plt.title('GC vs Completeness')
plt.tight_layout()
plt.savefig('gc_vs_completeness.png')
plt.close()
