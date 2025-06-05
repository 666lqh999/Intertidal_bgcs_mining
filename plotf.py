import os
import pandas as pd

# 1. 遍历 antismash_out 文件夹，建立 bgc_name -> genome_name 的映射
mapping = {}
base_dir = "antismash_out"  # 根据实际路径修改

for genome_folder in os.listdir(base_dir):
    genome_path = os.path.join(base_dir, genome_folder)
    if not os.path.isdir(genome_path):
        continue
    for fname in os.listdir(genome_path):
        if fname.endswith(".gbk"):
            # 去掉扩展名，得到 bgc_name
            bgc_name = os.path.splitext(fname)[0]
            mapping[bgc_name] = genome_folder

# 2. 读入 BS_filtered.tsv
bs_df = pd.read_csv("BS_filtered.tsv", sep="\t", header=0)

# 3. 将 mapping 转为 DataFrame
map_df = pd.DataFrame.from_dict(mapping, orient="index", columns=["genome_name"])
map_df.index.name = "bgc_name"
map_df = map_df.reset_index()

# 4. 合并
merged = pd.merge(
    bs_df,
    map_df,
    on="bgc_name",
    how="left"   # 如果某些 bgc_name 没在 antismash_out 中找到，对应 genome_name 会是 NaN
)

# 5. 保存结果
merged.to_csv("BS_filtered_with_genome.tsv", sep="\t", index=False)

print(f"共处理 {len(bs_df)} 条 BGC，成功匹配到 {merged['genome_name'].notna().sum()} 条基因组名称")
print(merged)
