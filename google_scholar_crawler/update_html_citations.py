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

# 3. 遍历标题，插入或更新
for title, cites in citation_map.items():
    # 找到标题位置（忽略大小写）
    pattern = rf"({re.escape(title)})"
    matches = list(re.finditer(pattern, content, flags=re.I))

    for match in matches:
        start, end = match.span()
        # 查找标题后面是否已有 Badge
        badge_pattern = r'<img src="https://img.shields.io/badge/Citations-\d+-blue" alt="Citations">'
        after_text = content[end:end+200]  # 标题后最多200字符检查
        if re.search(badge_pattern, after_text):
            # 替换数字
            new_after = re.sub(r'(Citations-)\d+(-blue)', rf'\1{cites}\2', after_text)
            content = content[:end] + new_after + content[end+len(after_text):]
        else:
            # 在标题后面插入 Badge
            badge_html = f' <a href="https://scholar.google.com.hk/citations?user=e5ng8m0AAAAJ" target="_blank"><img src="https://img.shields.io/badge/Citations-{cites}-blue" alt="Citations"></a>'
            content = content[:end] + badge_html + content[end:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 引用数 Badge 已更新或插入完成")
