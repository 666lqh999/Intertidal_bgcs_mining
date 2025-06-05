#!/usr/bin/env python3
import os
import pandas as pd

# 1. 配置路径
ANTISMASH_DIR = 'antismash_out'
METADATA_FILE = 'metadata.tsv'
OUTPUT_FILE = 'Network_With_Taxonomy.tsv'

# 2. 读取 metadata，只保留需要的列
meta = pd.read_csv(METADATA_FILE, sep='\t', usecols=['mOTU ID', 'GTDB taxonomy'])

# 3. 遍历 antismash_out 目录，收集每个 BGC 文件所属的 mOTU ID
records = []
for mOTU in os.listdir(ANTISMASH_DIR):
    mOTU_dir = os.path.join(ANTISMASH_DIR, mOTU)
    if not os.path.isdir(mOTU_dir):
        continue
    for fname in os.listdir(mOTU_dir):
        if fname.endswith('.gbk') and 'region' in fname:
            bgc_id = os.path.splitext(fname)[0]  # 去掉 .gbk
            records.append({'mOTU ID': mOTU, 'BGC': bgc_id})

bgc_df = pd.DataFrame(records)

# 4. 将 BGC DataFrame 和 metadata 根据 mOTU ID 合并
merged = bgc_df.merge(meta, on='mOTU ID', how='left')

# 5. 保存结果
merged.to_csv(OUTPUT_FILE, sep='\t', index=False)

print(f'Merged table saved to {OUTPUT_FILE}')
