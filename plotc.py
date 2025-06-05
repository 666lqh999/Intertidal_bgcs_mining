import pandas as pd

# 读取 BS.tsv 和 data1_transformed.tsv
bs_df = pd.read_csv("BS.tsv", sep="\t", header=0)
data_df = pd.read_csv("data1_transformed.tsv", sep="\t", header=0)

# 将列名统一，方便合并
bs_df = bs_df.rename(columns={"#BGC Name": "bgc_name"})
# data_df 已经是 bgc_name, membership_value

# 只保留需要的列，然后内连接
merged = pd.merge(
    bs_df[["bgc_name"]],           # BS 中所有 bgc_name
    data_df,                       # data1_transformed 中 bgc_name + membership_value
    on="bgc_name", 
    how="inner"
)

# 保存结果
merged.to_csv("BS_with_membership.tsv", sep="\t", index=False)

print(f"共找到 {len(merged)} 条共有的 BGC：")
print(merged)
