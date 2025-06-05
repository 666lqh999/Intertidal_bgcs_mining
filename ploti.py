import pandas as pd

# 1. 读取 BS_enriched.tsv
df = pd.read_csv("BS_enriched_normalized.tsv", sep="\t", header=0)

# 2. 计算 score：
#    score = (1 - membership_value)
#          + Completeness (%)
#          + (1 - Contamination (%))
#          + N50 (bp)
#          + Genome length (bp)
#          + # of contigs
#          + # of predicted genes
#          + Longest contig
#          + Coding density
#          + # markers in checkm
#          + Strain heterogeneity
df["score"] = (
    (1 - df["membership_value"])
    + df["Completeness (%)"]
    + (1 - df["Contamination (%)"])
    + df["N50 (bp)"]
    + df["Genome length (bp)"]
    + df["# of contigs"]
    + df["# of predicted genes"]
    + df["Longest contig"]
    + df["Coding density"]
    + df["# markers in checkm"]
    + df["Strain heterogeneity"]
)

# 3. 只保留 bgc_name 和 score，并按 score 降序排序
result = df[["bgc_name", "genome_name","score"]].sort_values(by="score", ascending=False)

# 4. 保存或输出
result.to_csv("BS_scores_sorted.tsv", sep="\t", index=False)
print(result)
