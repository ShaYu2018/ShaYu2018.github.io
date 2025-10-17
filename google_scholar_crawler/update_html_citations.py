import json
import re

# 1. 加载爬虫结果 JSON
with open("google_scholar_crawler/results/gs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 构建标题 → 引用数映射，忽略大小写和多空格
citation_map = {
    pub["bib"]["title"].strip().lower().replace("\u00a0", " ").replace("\t", " ").replace("  ", " "): int(pub.get("num_citations", 0))
    for pub in data.get("publications", [])
}

file_path = "_pages/includes/publications.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. 遍历每个标题进行替换
for title, cites in citation_map.items():
    # 模糊匹配标题所在段落并替换 badge 数字
    pattern = rf'({re.escape(title)}.*?<img src="https://img.shields.io/badge/Citations-)\d+(-blue" alt="Citations">)'
    replacement = rf'\g<1>{cites}\g<2>'
    # 忽略大小写匹配
    content = re.sub(pattern, replacement, content, flags=re.S | re.I)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已更新 publications.md 中的 Citation Badge 数字")
