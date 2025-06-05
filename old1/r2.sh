# 设置线程限制环境变量
export OPENBLAS_NUM_THREADS=2
export OMP_NUM_THREADS=2

# 分阶段并行执行（推荐方案）
mkdir -p antismash_results
find data/ -name "*.fna" | parallel -j 8 --progress --eta \
  'antismash \
  --genefinding-tool prodigal-m \
  --cb-general \
  --cb-knownclusters \
  --pfam2go \
  --cpus 4 \
  --output-dir antismash_results/{/.} {}'