#!/bin/bash
# 检查数据一致性
check_consistency() {
  total_regions=$(find antismash_results -name "*bin_*.gbk" -exec grep -c "region_number" {} + | awk -F: '{sum+=$2} END{print sum}')
  total_products=$(find antismash_results -name "*bin_*.gbk" -exec grep -h "product=" {} + | wc -l)
  
  if [ "$total_regions" -eq "$total_products" ]; then
    echo "√ 数据一致: Regions=$total_regions, Products=$total_products"
  else
    echo "× 数据异常: Regions=$total_regions ≠ Products=$total_products"
    echo ">> 建议检查以下文件："
    find antismash_results -name "*bin_*.gbk" -exec awk '
      /region_number/ {reg++} 
      /product=/ {prod++} 
      END{if(reg!=prod) print FILENAME ": Regions=" reg " vs Products=" prod}' {} \;
  fi
}

check_consistency