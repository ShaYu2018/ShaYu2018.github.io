import json
import re

# 1. 加载爬虫结果 JSON
with open("results/gs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 构建标题 → 引用数映射
citation_map = {
    pub["bib"]["title"].strip().lower(): int(pub.get("num_citations", 0))
    for pub in data.get("publications", [])
}

file_path = "../_pages/includes/publications.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. 遍历每个标题
for title, cites in citation_map.items():
    title_pattern = re.escape(title)
    badge_pattern = rf'(<img src="https://img.shields.io/badge/Citations-)\d+(-blue" alt="Citations">)'

    # 查找该标题所在块
    match = re.search(rf'({title_pattern}.*?)(<img src="https://img.shields.io/badge/Citations-\d+-blue" alt="Citations">)?', content, flags=re.S | re.I)
    if match:
        if match.group(2):
            # 已有Badge，替换数字
            updated_block = re.sub(badge_pattern, rf'\g<1>{cites}\g<2>', match.group(0), flags=re.S | re.I)
        else:
            # 没有Badge，插入新的
            badge_html = f'<a href="https://scholar.google.com.hk/citations?user=e5ng8m0AAAAJ" target="_blank"><img src="https://img.shields.io/badge/Citations-{cites}-blue" alt="Citations"></a>'
            updated_block = f'{match.group(1)} {badge_html}'
        content = content.replace(match.group(0), updated_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 引用数 Badge 已更新/新增完成")
