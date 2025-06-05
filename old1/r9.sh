#!/bin/bash
# 输入：antiSMASH结果目录
# 输出：Region级产物统计报告

input_dir="antismash_results"
output_file="bgc_product_report.tsv"

echo -e "Filename\tRegionNumber\tProducts" > $output_file

find $input_dir -name "*bin_*.gbk" | while read gbk; do
  awk -v file="$gbk" '
    BEGIN {FS="\""; region=0; region_num=0; products=""}
    /region_number/ {region=1; region_num=$2; products=""}
    /product=/ && region {products = (products=="" ? $2 : products "," $2)}
    /^\/\// && region && region_num>0 {
      print file "\t" region_num "\t" products;
      region=0; region_num=0; products=""
    }
  ' $gbk
done >> $output_file

# 生成摘要
echo "=== 产物分布统计 ==="
awk -F'\t' '{split($3,a,","); for(i in a) print a[i]}' $output_file | sort | uniq -c