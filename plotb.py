import pandas as pd

# 读取 data1.tsv（根据实际路径调整）
df = pd.read_csv("data1.tsv", sep='\t', header=0)

# 只保留 bgc_name 和 membership_value
df2 = df[['bgc_name', 'membership_value']].copy()

# 对 bgc_name 进行处理：将“/”及其之前的部分去除
df2['bgc_name'] = df2['bgc_name'].apply(lambda x: x.split('/', 1)[-1])

# 保存或打印结果
df2.to_csv("data1_transformed.tsv", sep='\t', index=False)
print(df2)
