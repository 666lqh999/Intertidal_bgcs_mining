import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('metadata.tsv', sep='\t')

# 从 GTDB taxonomy 中提取 Phylum
def extract_phylum(gt):
    try:
        parts = gt.split(';')
        ph = parts[1].replace('p__', '')
        return ph if ph else 'Unknown'
    except:
        return 'Unknown'
df['Phylum'] = df['GTDB taxonomy'].apply(extract_phylum)

# 1. Completeness 分布直方图
plt.figure()
plt.hist(df['Completeness (%)'].dropna(), bins=50)
plt.xlabel('Completeness (%)')
plt.ylabel('Count')
plt.title('Completeness Distribution')
plt.tight_layout()
plt.savefig('completeness_distribution.png')
plt.close()

# 2. Contamination 分布直方图
plt.figure()
plt.hist(df['Contamination (%)'].dropna(), bins=50)
plt.xlabel('Contamination (%)')
plt.ylabel('Count')
plt.title('Contamination Distribution')
plt.tight_layout()
plt.savefig('contamination_distribution.png')
plt.close()

# 3. Completeness vs Contamination 散点图
plt.figure()
plt.scatter(df['Contamination (%)'], df['Completeness (%)'], alpha=0.6)
plt.xlabel('Contamination (%)')
plt.ylabel('Completeness (%)')
plt.title('Completeness vs Contamination')
plt.tight_layout()
plt.savefig('completeness_vs_contamination.png')
plt.close()

# 4. GC 含量分布直方图
plt.figure()
plt.hist(df['GC (%)'].dropna(), bins=50)
plt.xlabel('GC Content (%)')
plt.ylabel('Count')
plt.title('GC Content Distribution')
plt.tight_layout()
plt.savefig('gc_content_distribution.png')
plt.close()

# 5. N50 vs Genome Length (Log-Log) 散点图
plt.figure()
plt.scatter(df['Genome length (bp)'], df['N50 (bp)'], alpha=0.6)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Genome Length (bp) [log scale]')
plt.ylabel('N50 (bp) [log scale]')
plt.title('N50 vs Genome Length')
plt.tight_layout()
plt.savefig('n50_vs_genome_length.png')
plt.close()

# 6. Genome Count per Phylum 柱状图
phylum_counts = df['Phylum'].value_counts()
plt.figure(figsize=(10, 6))
plt.bar(phylum_counts.index, phylum_counts.values)
plt.xticks(rotation=90)
plt.xlabel('Phylum')
plt.ylabel('Number of Genomes')
plt.title('Genome Count per Phylum')
plt.tight_layout()
plt.savefig('genome_count_per_phylum.png')
plt.close()

# 7. Coding Density by Top 10 Phyla 箱线图
top_phyla = phylum_counts.index[:10]
groups = [df[df['Phylum'] == ph]['Coding density'] for ph in top_phyla]
plt.figure(figsize=(10, 6))
plt.boxplot(groups, labels=top_phyla)
plt.xticks(rotation=90)
plt.ylabel('Coding Density')
plt.title('Coding Density by Top 10 Phyla')
plt.tight_layout()
plt.savefig('coding_density_boxplot_top10_phyla.png')
plt.close()

# 8. Metabolic Pathway Presence 柱状图
path_col = 'Metabolic pathways evaluated by KEGG-Decoder module (sulphate reduction bacteria within Deltaproteobacteria and Thermodesulfobacteria, and ammonia oxidation archaea within Thaumarchaeota)'
path_counts = df[path_col].fillna('None').value_counts()
plt.figure(figsize=(8, 4))
plt.bar(path_counts.index, path_counts.values)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Number of Genomes')
plt.title('Metabolic Pathway Presence')
plt.tight_layout()
plt.savefig('metabolic_pathway_counts.png')
plt.close()
