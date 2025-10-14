from scholarly import scholarly
import json
from datetime import datetime
import os

# 读取你的 Google Scholar ID（例如 https://scholar.google.com.hk/citations?user=e5ng8m0AAAAJ → e5ng8m0AAAAJ）
SCHOLAR_ID = os.environ.get('GOOGLE_SCHOLAR_ID', '').strip()

if not SCHOLAR_ID:
    raise ValueError("GOOGLE_SCHOLAR_ID 环境变量未设置")

print(f"Fetching Google Scholar data for ID: {SCHOLAR_ID}")

# 获取作者数据
author = scholarly.search_author_id(SCHOLAR_ID)
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])

# 添加更新时间
author['updated'] = str(datetime.utcnow())
author['publications'] = {v['author_pub_id']: v for v in author['publications']}

# 保存完整数据
os.makedirs('results', exist_ok=True)
with open('results/gs_data.json', 'w', encoding='utf-8') as f:
    json.dump(author, f, ensure_ascii=False, indent=2)

# 生成 Shields.io Badge 数据
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
    "color": "9cf"
}
with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
    json.dump(shieldio_data, f, ensure_ascii=False)

print("✅ Scholar data updated successfully!")
