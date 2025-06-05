mkdir -p bigscape_input  # 关键步骤：-p参数确保目录存在
# 生成统计总表
antismash-summary -o all_results.tsv antismash_results/*

# 检查含BGC的基因组比例
awk -F'\t' 'NR>1 && $5>0 {count++} END {print count/NR}' all_results.tsv

# 提取所有预测BGC
find antismash_results -name "*.gbk" -exec cp {} bigscape_input/ \;