import json
import re

# 1. 读取爬虫数据
with open("results/gs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 构建 标题 → 引用数 映射（忽略大小写）
citation_map = {
    pub["bib"]["title"].strip().lower(): int(pub.get("num_citations", 0))
    for pub in data.get("publications", [])
}

file_path = "../_pages/includes/publications.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. 定位 Papers 部分（只更新这一块）
match = re.search(r"(### 📝 Papers:.*?)(?=\n### |\Z)", content, flags=re.S)
if match:
    papers_section = match.group(1)

    # 4. 遍历 JSON 数据，在 papers_section 更新/插入 Badge
    for title, cites in citation_map.items():
        title_pattern = re.escape(title)

        def repl(m):
            text_after = m.group(2) or ""
            badge_pattern = r'<img src="https://img.shields.io/badge/Citations-\d+-blue" alt="Citations">'
            badge_html = f' <a href="https://scholar.google.com.hk/citations?user=e5ng8m0AAAAJ" target="_blank"><img src="https://img.shields.io/badge/Citations-{cites}-blue" alt="Citations"></a>'

            # 已有 Badge → 更新数字
            if re.search(badge_pattern, text_after):
                text_after = re.sub(r'(Citations-)\d+(-blue)', rf'\g<1>{cites}\g<2>', text_after)

            else:
                # ① 如果有图片（但不是引用数 Badge） → 标题后插 Badge
                if re.search(r'<img(?! src="https://img\.shields\.io/badge/Citations)', text_after):
                    text_after = badge_html + text_after

                # ② 否则如果同时有 Paper 和 Code → 插在 Code 后面
                elif re.search(r'\| \[Paper\]', text_after) and re.search(r'\| \[Code\]', text_after):
                    text_after = re.sub(r'(\| \[Code\]\([^)]+\))', rf'\1{badge_html}', text_after, count=1)

                # ③ 否则如果只有 Paper → 插在 Paper 后面
                elif re.search(r'\| \[Paper\]', text_after):
                    text_after = re.sub(r'(\| \[Paper\]\([^)]+\))', rf'\1{badge_html}', text_after, count=1)

                # ④ 默认情况 → 标题后插 Badge
                else:
                    text_after = badge_html + text_after

            return m.group(1) + text_after

        papers_section = re.sub(rf'({title_pattern})(.*)', repl, papers_section, flags=re.I)

    # 5. 替换原文中的 Papers 段落
    content = content.replace(match.group(1), papers_section)

# 6. 保存更新后的文件
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已更新 Papers 段落中的 Citation Badge!")
