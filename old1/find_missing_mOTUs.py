#!/usr/bin/env python3
import os

meta_dir  = 'meta_data'
asm_dir   = 'antismash_out'

# 1. 从 meta_data/*.fna 提取所有基因组 ID（去掉 .fna）
meta_ids = {
    os.path.splitext(f)[0]
    for f in os.listdir(meta_dir)
    if f.endswith('.fna')
}

# 2. 从 antismash_out 子目录列表提取已跑的基因组 ID
asm_ids = {
    d for d in os.listdir(asm_dir)
    if os.path.isdir(os.path.join(asm_dir, d))
}

# 3. 求差集
missing = sorted(meta_ids - asm_ids)

# 4. 输出
print(f"Meta 中共有 {len(meta_ids)} 个 mOTU，antismash_out 中有 {len(asm_ids)} 个子目录。")
print(f"缺少的基因组共有 {len(missing)} 个：")
for m in missing:
    print(" ", m)

# 5. 写入文件
with open('missing_mOTUs.txt','w') as out:
    out.write("\n".join(missing))
print("已将缺少的基因组列表保存到 missing_mOTUs.txt")
