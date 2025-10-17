import json
import re

# 1. 读取爬虫数据
with open("results/gs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 构建标题 → 引用数映射（忽略大小写）
citation_map = {
    pub["bib"]["title"].strip().lower(): int(pub.get("num_citations", 0))
    for pub in data.get("publications", [])
}

file_path = "../_pages/includes/publications.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. 定位 Papers 部分（到下一个 ### 或文件结束）
match = re.search(r"(### 📝 Papers:.*?)(?=\n### |\Z)", content, flags=re.S)
if match:
    papers_section = match.group(1)

    # 4. 在 papers_section 内更新/插入引用数
    for title, cites in citation_map.items():
        title_pattern = re.escape(title)

        # 查找标题并更新或插入 Badge
        def repl(m):
            text_after = m.group(2) or ""
            badge_pattern = r'<img src="https://img.shields.io/badge/Citations-\d+-blue" alt="Citations">'
            if re.search(badge_pattern, text_after):
                # 已有 Badge → 替换数字
                text_after = re.sub(r'(Citations-)\d+(-blue)', rf'\g<1>{cites}\g<2>', text_after)
            else:
                # 没有 Badge → 插入
                badge_html = f' <a href="https://scholar.google.com.hk/citations?user=e5ng8m0AAAAJ" target="_blank"><img src="https://img.shields.io/badge/Citations-{cites}-blue" alt="Citations"></a>'
                text_after = badge_html + text_after
            return m.group(1) + text_after

        papers_section = re.sub(rf'({title_pattern})(.*)', repl, papers_section, flags=re.I)

    # 5. 替换原文中的 Papers 部分
    content = content.replace(match.group(1), papers_section)

# 6. 保存更新后的文件
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已更新 Papers 段落中的 Citation Badge!")
