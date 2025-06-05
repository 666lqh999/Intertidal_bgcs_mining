# 创建报告导航页（方便人工核查）
find antismash_results -name "index.html" > report_list.txt
echo "BGC可视化报告列表：" > summary.html
cat report_list.txt | sed 's/^/<a href="file:\/\/&">&<\/a><br>/' >> summary.html