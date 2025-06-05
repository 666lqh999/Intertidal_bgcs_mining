import pandas as pd
import os
import shutil
import sys
import re
import filecmp
from pathlib import Path
import logging
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    filename='processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_metadata(path):
    """增强型元数据加载"""
    dtype_map = {
        "mOTU ID": str,
        "N50 (bp)": int,
        "Genome length (bp)": int
    }
    try:
        return pd.read_csv(
            path, sep='\t', dtype=dtype_map,
            usecols=["mOTU ID", "Completeness (%)", "Contamination (%)", 
                     "N50 (bp)", "Genome length (bp)"]
        )
    except Exception as e:
        logging.critical(f"元数据加载失败: {str(e)}")
        sys.exit(1)

def extract_id(filename):
    """方案B：提取完整前缀（适用于元数据ID含地理标记）"""
    return os.path.splitext(filename)[0]

def main():
    if len(sys.argv) != 3:
        print("Usage: python process.py <metadata.tsv> <source_dir>")
        sys.exit(1)

    metadata_path, source_dir = sys.argv[1], sys.argv[2]
    target_dir = "top5_samples"
    Path(target_dir).mkdir(exist_ok=True)

    try:
        df = load_metadata(metadata_path)
        
        # 严格筛选
        filtered = df.query(
            "`Completeness (%)` >= 90 & "
            "`Contamination (%)` <= 5 & "
            "`N50 (bp)` >= 10000 & "
            "`Genome length (bp)` >= 2000000"
        )
       # 在原有代码的filtered = df.query(...)之后添加排序逻辑
        filtered_sorted = filtered.sort_values(
            by=["Completeness (%)", "Contamination (%)", "N50 (bp)"],
            ascending=[False, True, False]
        )

        # 选择前5个样本
        top5_samples = filtered_sorted.head(5)
        top5_samples.to_csv("top5_samples.tsv", sep='\t', index=False) 

        
        # 构建ID集合
        valid_ids = set(top5_samples["mOTU ID"].str.strip())
        
        # 预筛文件列表
        all_files = list(Path(source_dir).glob("*.fna"))
        matched_files = [
            f for f in all_files 
            if (ext_id := extract_id(f.name)) is not None 
            and ext_id in valid_ids
        ]
        
        # 带进度条复制
        with tqdm(total=len(matched_files), desc="Copying") as pbar:
            for src in matched_files:
                dst = Path(target_dir)/src.name
                shutil.copy2(src, dst)
                if not filecmp.cmp(src, dst):
                    logging.error(f"校验失败: {src.name}")
                pbar.update(1)
                
        print(f"\n结果统计:")
        print(f"- 筛选后基因组: {len(top5_samples)}")
        print(f"- 实际找到文件: {len(matched_files)}")
        print(f"- 缺失文件: {len(valid_ids)-len(matched_files)}")

    except Exception as e:
        logging.error(f"致命错误: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()