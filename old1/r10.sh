# 创建有效文件列表（仅含BGC的GBK）
grep -l "region_number" antismash_results/*/*.gbk > valid_bgcs.list

# 构建BiG-SCAPE输入目录
mkdir -p bigscape_input
cat valid_bgcs.list | xargs -I{} cp {} bigscape_input/

# 删除冗余的contig子文件（若存在）
find bigscape_input -name "*contig*.gbk" -delete