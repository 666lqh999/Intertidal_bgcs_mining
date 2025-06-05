import pandas as pd
import numpy as np

# 读取 BS_enriched.tsv
df = pd.read_csv("BS_enriched.tsv", sep="\t", header=0)

# 识别所有数值列
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# 复制一份用于存放归一化结果
df_norm = df.copy()

# 对每个数值列做 min–max 归一化
for col in numeric_cols:
    min_val = df_norm[col].min()
    max_val = df_norm[col].max()
    if max_val > min_val:
        df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
    else:
        # 若该列所有值相同，则统一设为 0
        df_norm[col] = 0.0

# 保存归一化后的表格
df_norm.to_csv("BS_enriched_normalized.tsv", sep="\t", index=False)

print("归一化完成，数值列：", numeric_cols)
print("输出文件：BS_enriched_normalized.tsv")
