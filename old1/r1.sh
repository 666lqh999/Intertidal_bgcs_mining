find data/ -name "*.fna" | parallel -j 32 \
  'antismash --genefinding-tool prodigal-m \
  --cb-general --cb-knownclusters --pfam2go \
  --output-dir antismash_results/{/.} {}'