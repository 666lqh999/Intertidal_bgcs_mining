import pandas as pd

# 读取 BS_with_membership.tsv（根据实际路径调整）
df = pd.read_csv("BS_with_membership.tsv", sep="\t", header=0)

# 筛选 membership_value 小于等于 0.4 的行
filtered_df = df[df["membership_value"] <= 0.4].copy()

# 保存结果
filtered_df.to_csv("BS_filtered.tsv", sep="\t", index=False)

print("筛选结果：")
print(filtered_df)
