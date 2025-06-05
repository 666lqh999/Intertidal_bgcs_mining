import pandas as pd

# 1. 读取 BS_scores_normalized_filtered.tsv、metadata.tsv、Network_Annotations_Full.tsv
bs = pd.read_csv("BS_scores_normalized_filtered.tsv", sep="\t", header=0)
meta = pd.read_csv("metadata.tsv", sep="\t", header=0)
net = pd.read_csv("Network_Annotations_Full.tsv", sep="\t", header=0)

# 2. 重命名 meta 中的 mOTU ID 为 genome_name，以便与 bs 对齐
meta = meta.rename(columns={"mOTU ID": "genome_name"})

# 3. 重命名 net 中的 BGC 列为 bgc_name，以便与 bs 对齐
net = net.rename(columns={"BGC": "bgc_name"})

# 4. 合并 BS 与 metadata（左连接，保留所有 bs 条目）
bs_meta = pd.merge(
    bs,
    meta,
    on="genome_name",
    how="left"
)

# 5. 合并上 product prediction（左连接）
final = pd.merge(
    bs_meta,
    net[["bgc_name", "Product Prediction"]],
    on="bgc_name",
    how="left"
)
# 假设合并后的 DataFrame 是 df
final = final.loc[:, ~final.columns.str.startswith("Unnamed")]

# 6. 保存结果
final.to_csv("BS_complete.tsv", sep="\t", index=False)

print("合并完成，输出文件：BS_complete.tsv")
print(final.head())
