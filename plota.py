import pandas as pd

# 读取 mix_clustering_c0.50.tsv
file_path = "mix_clustering_c0.50.tsv"
df = pd.read_csv(file_path, sep='\t', header=0)

# 找出所有以 "BGC" 开头（MIBiG 参考 BGC）的 Family Number
ref_families = df[df['#BGC Name'].str.startswith('BGC')]['Family Number'].unique()

# 筛选不与这些参考 BGC 同族的条目
bs_df = df[~df['Family Number'].isin(ref_families)].copy()

# 保存结果到 BS.tsv
bs_df.to_csv("BS.tsv", sep='\t', index=False)

print(f"共筛选出 {len(bs_df)} 条未与 MIBiG 参考 BGC 同家族的记录，已保存为 BS.tsv")
