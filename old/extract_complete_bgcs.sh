#!/usr/bin/env bash
set -e

# 目标目录
OUTDIR=bigscape_input/complete

# 建目录
mkdir -p "$OUTDIR"

# 计数
count=0

# 遍历所有 .gbk
find antismash_out -type f -name "*.region*.gbk" | while read -r gbk; do
  # 如果包含 on_contig_edge="False"（即complete），就拷贝
  if grep -q 'on_contig_edge="False"' "$gbk"; then
    bin=$(basename "$(dirname "$gbk")")
    file=$(basename "$gbk")
    cp "$gbk" "$OUTDIR/${bin}__${file}"
    ((count++))
  fi
done

echo "共复制了 $count 个 complete BGC 到 $OUTDIR"
