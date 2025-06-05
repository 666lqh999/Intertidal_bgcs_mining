import pandas as pd

# 读取 BS_filtered.tsv 和 Network_Annotations_Full.tsv
bs = pd.read_csv("BS_filtered.tsv", sep="\t", header=0)
net = pd.read_csv("Network_Annotations_Full.tsv", sep="\t", header=0)

# 提取 Network_Annotations_Full 中的 BGC 和 Product Prediction 两列，并重命名以便合并
net_pp = net[["BGC", "Product Prediction"]].rename(columns={"BGC": "bgc_name"})

# 将 BS_filtered 与 Product Prediction 合并
merged = pd.merge(
    bs, 
    net_pp,
    on="bgc_name",
    how="left"   # 若某些 BGC 在 annotations 中找不到，则对应的 Product Prediction 为 NaN
)

# 保存结果
merged.to_csv("BS_filtered_with_product_prediction.tsv", sep="\t", index=False)

print("已将 Product Prediction 添加到 BS_filtered 中，共合并出 {} 条记录：".format(len(merged)))
print(merged)
