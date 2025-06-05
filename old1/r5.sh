#!/bin/bash
# 激活antismash环境
source activate antismash_env



# 统计含BGC的基因组数量
grep -c "region_number" antismash_results/*/*bin_*.gbk  # 输出含BGC的文件数

# 计算比例（假设总样本数384）
find antismash_results -name "*bin_*.gbk" -exec grep -l "region_number" {} + | wc -l

# 统计有效基因组数
valid_files=$(find antismash_results -name "*bin_*.gbk" -exec grep -l "region_number" {} + | wc -l)

# 计算并输出
ratio=$(echo "scale=2; $valid_files / 382 * 100" | bc)
echo "有效BGC基因组比例：${ratio}%"