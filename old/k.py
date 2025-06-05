import pandas as pd

# 1. 读取含有原始 score 的文件
df = pd.read_csv("BS_scores_sorted.tsv", sep="\t", header=0)

# 2. 对 score 列做 Min–Max 归一化
min_score = df["score"].min()
max_score = df["score"].max()
df["score_norm"] = (df["score"] - min_score) / (max_score - min_score)

# 3. 筛选归一化后 score >= 0.5 的记录
filtered = df[df["score_norm"] >= 0.5].copy()

# 4. 仅保留 bgc_name、genome_name 和 归一化后的 score
result = filtered[["bgc_name", "genome_name", "score_norm"]].rename(columns={"score_norm": "score"})

# 5. 按归一化后的 score 降序排序（可选，因为原始已排序，但归一化后顺序不会变）
result = result.sort_values(by="score", ascending=False)

# 6. 保存结果
result.to_csv("BS_scores_normalized_filtered.tsv", sep="\t", index=False)

print(f"共筛选出 {len(result)} 条记录，已保存为 BS_scores_normalized_filtered.tsv")
print(result)
