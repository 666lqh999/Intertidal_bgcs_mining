# Step 1: Prokka注释
nohup parallel -j 16 --progress --eta "prokka \
  --outdir prokka_out/{/.} \
  --prefix {/.} \
  --kingdom Bacteria \
  --addgenes \
  --mincontiglen 1000 \
  --cpus 8 \
  --norrna \
  {}" ::: meta_data/*.fna 

# Step 2: antiSMASH分析

nohup parallel -j 16 --progress --eta "antismash \
  --genefinding-tool none \
  --output-dir antismash_out/{/.} \
  --taxon bacteria \
  --cb-knownclusters \
  --asf \
  --smcog-trees \
  --clusterhmmer \
  --rre \
  -c 8 \
  prokka_out/{/.}/{/.}.gbk" \
  ::: meta_data/*.fna

3.
echo "=== Running BiG-SCAPE (本地模式) ==="
python bigscape.py \
  -i ../antismash_out \
  -o ../bigscape_out \
  --mix \
  --cutoffs 0.3 0.6 0.7 \
  --mibig \
  --clan_cutoff 0.3 0.7 \
  --cores 8 \
  --pfam_dir ../ \
  --min_bgc_size 5000 \
  --mode glocal \
  --verbose          

nohup python bigscape.py \
  -i ../antismash_out \
  -o ../bigscape_out1 \
  --include_gbk_str 'region' \
  --include_singletons \
  --mix \
  --cutoffs 0.5 \
  --mibig \
  --cores 128 \
  --pfam_dir ../ \
  --min_bgc_size 1000 \
  --mode glocal \
  --verbose 

nohup python bigscape.py \
  -i ../bigscape_input \
  -o ../bigscape_out \
  --include_gbk_str 'region' \
  --include_singletons \
  --mix \
  --cutoffs 0.4 0.5 0.6 \
  --mibig \
  --cores 128 \
  --pfam_dir ../ \
  --min_bgc_size 1000 \
  --mode glocal \
  --verbose 


  parallel -j 1 "echo prokka_out/{/.}/{/.}.gbk" ::: data2/meta_data/*.fna > new_gbk_list.txt

  nohup parallel -j 16 --progress --eta --arg-file new_gbk_list.txt "antismash \
  --genefinding-tool none \
  --output-dir antismash_out/{/.} \
  --taxon bacteria \
  --cb-knownclusters \
  --asf \
  --smcog-trees \
  --clusterhmmer \
  --rre \
  -c 8 \
  {}" > antismash.log 2>&1 &

  nohup parallel -j 2 --progress --eta --arg-file missing_mOTUs.txt "antismash \
  --genefinding-tool prodigal \
  --output-dir antismash_out/{/.} \
  --taxon bacteria \
  --cb-knownclusters \
  --asf \
  --smcog-trees \
  --clusterhmmer \
  --rre \
  -c 16 \
  {}" > antismash.log 2>&1 &

  nohup parallel -j 16 --progress --eta --arg-file failed_samples.txt "antismash \
  --genefinding-tool none \
  --output-dir antismash_out/{/.} \
  --taxon bacteria \
  --cb-knownclusters \
  --asf \
  --smcog-trees \
  --clusterhmmer \
  --rre \
  -c 8 \
  {}" > antismash1.log 2>&1 &



python bigscape.py \
  -i ../antismash_out \
  -o ../bigscape_out \
  --include_gbk_str 'region' \
  --include_singletons \
  --mix \
  --cutoffs 0.3 0.6 0.7 \
  --mibig \
  --clan_cutoff 0.3 0.7 \
  --cores 128 \
  --pfam_dir ../ \
  --min_bgc_size 5000 \
  --mode glocal \
  --verbose 



nohup python bigscape.py \
  -i ../antismash_out \
  -o ../bigscape_out \
  --include_gbk_str 'region' \
  --include_singletons \
  --mix \
  --cutoffs 0.3 0.6 0.7 \
  --mibig \
  --clan_cutoff 0.3 0.7 \
  --cores 128 \
  --pfam_dir ../ \
  --min_bgc_size 5000 \
  --mode glocal \
  --verbose 

nohup parallel -j 4 --progress --eta \
  "deepbgc pipeline \
    --prodigal-meta-mode \
    --output deepbgc_out/{/.} \
    --min-bio-domains 2 \
    {}" \
  ::: meta_data/*.fna > deepbgc.log 2>&1 &


  mkdir -p bigslice_input/{taxonomy,dataset_1}

  cat > bigslice_input/datasets.tsv <<EOF
#dataset_name	dataset_folder	taxonomy_file	description
dataset_1	dataset_1	taxonomy/taxonomy_dataset_1.tsv	Intertidal_BGCs
EOF

# 为每个样本创建对应的基因组文件夹
find antismash_out -type f -name "*.region*.gbk" | while read gbk; do
  # 提取contig ID（如GD_ST_contig_20467069）
  contig_id=$(basename "$gbk" | cut -d. -f1)
  
  # 创建以contig ID命名的基因组文件夹
  mkdir -p "bigslice_input1/dataset_1/$contig_id"
  
  # 复制GBK文件（保持原始文件名）
  cp "$gbk" "bigslice_input1/dataset_1/$contig_id/"
done

cat > bigslice_input/taxonomy/taxonomy_dataset_1.tsv <<EOF
Genome folder	Kingdom	Class	Order	Family	Genus	Species	Strain
GD_ST_contig_20467069/	Bacteria	Unknown	Unknown	Unknown	Unknown	Unknown	GD_ST
GD_ST_contig_8457/	Bacteria	Unknown	Unknown	Unknown	Unknown	Unknown	GD_ST
EOF

find bigslice_input/dataset_1 -maxdepth 1 -type d -name "GD_ST_contig_*" | while read dir; do
  contig=$(basename "$dir")
  echo -e "${contig}/\tBacteria\tUnknown\tUnknown\tUnknown\tUnknown\tUnknown\t${contig}"
done > bigslice_input/taxonomy/taxonomy_dataset_1.tsv

# 添加表头
sed -i '1i Genome folder\tKingdom\tClass\tOrder\tFamily\tGenus\tSpecies\tStrain' bigslice_input/taxonomy/taxonomy_dataset_1.tsv



nohup bigslice -i bigslice_input/ bigslice_output4 

bigslice bigslice_output/ --export-tsv bigslice_output/result_tsv

pip install -r bigslice_output/requirements.txt

bash <output_folder>/start_server.sh <port(可选)>
./bigslice_output/start_server.sh 5000
chmod +x bigslice_output/start_server.sh


cat bigscape_out/network_files/2025-04-24_15-32-54_hybrids_glocal/Network_Annotations_Full.tsv \
  | awk -F'\t' 'BEGIN {OFS="\t"} {print $1, $4, $5, $6, $7}' \
  | sed '1s/^/#BGC_ID\tProduct\tClass\tOrganism\tTaxonomy\n/' \
  > nodes.tsv


# 进入输出目录
cd bigscape_out/network_files/2025-04-24_15-32-54_hybrids_glocal

# 合并所有类型的c0.30.network文件（注意排除注释行）
find . -name "*_c0.30.network" -exec grep -v '^Clustername 1' {} \; \
  | awk -F'\t' 'BEGIN {OFS="\t"} {print $1, $2, $5}' \
  | sed '1i Source\tTarget\tDSS' \
  > edges_0.30.tsv


# 在当前路径下创建 bigslice_input 及子目录
mkdir -p bigslice_input/complete_set

# 遍历 complete_bgcs.txt，将所有 region*.gbk 拷贝到 bigslice_input/complete_set 下对应的 genome 文件夹
while read gbk; do
  # 假设 gbk 格式如 antismash_out/FJ_XM_bin_114/FJ_XM_contig_10132429.region001.gbk
  genome_dir=$( dirname "$gbk" | sed 's@.*/@@' )       # e.g. FJ_XM_bin_114
  mkdir -p "bigslice_input/complete_set/${genome_dir}"
  cp "$gbk" "bigslice_input/complete_set/${genome_dir}/"
done < complete_bgcs.txt


find bigslice_input/complete_set -maxdepth 1 -type d -name "GD_ST_contig_*" | while read dir; do
  contig=$(basename "$dir")
  echo -e "${contig}/\tBacteria\tUnknown\tUnknown\tUnknown\tUnknown\tUnknown\t${contig}"
done > bigslice_input/taxonomy/taxonomy_dataset_1.tsv

# 添加表头
sed -i '1i Genome folder\tKingdom\tClass\tOrder\tFamily\tGenus\tSpecies\tStrain' bigslice_input/taxonomy/taxonomy_dataset_1.tsv