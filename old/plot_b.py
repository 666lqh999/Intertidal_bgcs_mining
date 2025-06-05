import os
import glob
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# 统计 BGC 类型
bgc_counts = Counter()
pattern = os.path.join("antismash_out", "*", "*region*.gbk")
print(pattern)
for gbk_file in glob.glob(pattern, recursive=True):
    with open(gbk_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('/region_type='):
                # 提取引号内内容
                region_type = line.split('=')[1].strip().strip('"')
                print(region_type)
                bgc_counts[region_type] += 1

# 转换为 DataFrame
df = pd.DataFrame({
    "BGC_Type": list(bgc_counts.keys()),
    "Count": list(bgc_counts.values())
}).sort_values("Count", ascending=False)

# 保存数据
# os.makedirs("/", exist_ok=True)
csv_path = "bgc_type_counts.csv"
df.to_csv(csv_path, index=False)

# 绘制并保存柱状图
plt.figure(figsize=(10, 6))
colors = plt.cm.tab20.colors[:len(df)]
plt.bar(df["BGC_Type"], df["Count"], color=colors)
plt.xlabel("BGC Type")
plt.ylabel("Count")
plt.title("Counts of Predicted BGC Types")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
bar_path = "bgc_type_counts_bar.png"
plt.savefig(bar_path)
plt.close()

# 绘制并保存饼状图
plt.figure(figsize=(8, 8))
plt.pie(df["Count"], labels=df["BGC_Type"], autopct='%1.1f%%', startangle=140, colors=colors)
plt.title("Proportion of Predicted BGC Types")
plt.axis('equal')
pie_path = "bgc_type_counts_pie.png"
plt.savefig(pie_path)
plt.close()

# 展示表格给用户
#import ace_tools as tools; tools.display_dataframe_to_user(name="BGC Type Counts", dataframe=df)

#bar_path, pie_path, csv_path
