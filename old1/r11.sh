#!/bin/bash
# r11.sh

# 进入BiG-SCAPE目录
cd BiG-SCAPE-1.1.5

# 清除旧结果（避免缓存干扰）
rm -rf ../bigscape_out/*

python bigscape.py -i ../bigscape_input -o ../bigscape_out \
  --include_gbk_str "bin_" \
  --pfam_dir ../ \
  --cutoffs 0.7 0.5 0.3 \
  --mix \
  --hybrids \
  --include_singletons \
  --cores 32