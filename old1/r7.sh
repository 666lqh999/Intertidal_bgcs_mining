# 计算region_number总数
total_regions=$(find antismash_results -name "*bin_*.gbk" -exec grep -c "region_number" {} + | awk -F: '{sum+=$2} END{print sum}')

# 计算product类型总数
total_products=$(find antismash_results -name "*bin_*.gbk" -exec grep -h "product=" {} + | wc -l)

# 对比结果
echo "Region总数: $total_regions | Product总数: $total_products"