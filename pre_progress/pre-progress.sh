1. 序列预处理（QC & 格式规范）

检查每个 .fna 的基本指标

mkdir stats
for f in meta_data/*.fna; do
  perl -e '$len=0; $count=0; open F,"'"$f"'"; while(<F>){ chomp; next if /^>/; $len+=length $_; $count++ }  
    $avg=$len/$count; printf "%s\tcontigs=%d\tbases=%d\tavg_contig=%.1f\n", "'"$f"'", $count, $len, $avg;' \
    >> stats/assembly_stats.tsv
done

