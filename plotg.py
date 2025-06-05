import pandas as pd

# 1. 读取 BS_filtered_with_genome.tsv 和 metadata.tsv
bs = pd.read_csv("BS_filtered_with_genome.tsv", sep="\t", header=0)
meta = pd.read_csv("metadata.tsv", sep="\t", header=0)

# 2. 重命名 metadata 中的 "mOTU ID" 列为 "genome_name"，以便合并
meta = meta.rename(columns={"mOTU ID": "genome_name"})

# 3. 合并：左连接保留所有 BGC 条目
merged = pd.merge(
    bs,
    meta,
    on="genome_name",
    how="left"
)

# 4. 保存结果
merged.to_csv("BS_enriched.tsv", sep="\t", index=False)

print(f"共 {len(merged)} 条记录，已将基因组属性合并完成，输出文件：BS_enriched.tsv")
print(merged.head())
