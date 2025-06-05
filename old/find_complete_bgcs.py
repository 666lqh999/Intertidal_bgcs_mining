#!/usr/bin/env python3
import os
from Bio import SeqIO

ANTISMASH_DIR = "antismash_out"
OUT_FILE = "complete_bgcs.txt"

complete_paths = []

# 遍历子目录
for root, dirs, files in os.walk(ANTISMASH_DIR):
    for fname in files:
        # 只处理 region*.gbk 文件
        if fname.endswith(".gbk") and "region" in fname:
            path = os.path.join(root, fname)
            try:
                # 读取 GenBank 记录
                record = SeqIO.read(path, "genbank")
            except Exception as e:
                print(f"无法解析 {path}: {e}")
                continue

            # 查找 region feature 上的 on_contig_edge 标记
            is_complete = False
            for feat in record.features:
                if feat.type.lower() in ("region", "cluster", "bgc"):
                    # antiSMASH v5+ 通常用 qualifier "on_contig_edge"
                    val = feat.qualifiers.get("on_contig_edge", ["True"])[0]
                    if val.lower() == "false":
                        is_complete = True
                        break

                    # 某些版本可能只用 "contig_edge"
                    val2 = feat.qualifiers.get("contig_edge", ["True"])[0]
                    if val2.lower() == "false":
                        is_complete = True
                        break

            if is_complete:
                complete_paths.append(path)

# 写出结果
with open(OUT_FILE, "w") as out:
    for p in sorted(complete_paths):
        out.write(p + "\n")

print(f"找到 {len(complete_paths)} 条完整 BGC，并写入 {OUT_FILE}")
