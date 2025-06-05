# 精准匹配主文件（排除region文件）
find antismash_results -name "*bin_*.gbk" -exec cp {} bigscape_input/ \;

# 验证文件数量（应与样本数一致）
ls bigscape_input | wc -l  # 应输出382