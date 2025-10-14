from scholarly import scholarly
import json
from datetime import datetime
import os
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # 从环境变量获取 Google Scholar ID
        SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID", "").strip()
        if not SCHOLAR_ID:
            raise ValueError("GOOGLE_SCHOLAR_ID 环境变量未设置")

        logger.info(f"Fetching data for Google Scholar ID: {SCHOLAR_ID}")

        # 获取作者数据
        author = scholarly.search_author_id(SCHOLAR_ID)
        scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

        # 添加更新时间
        author["updated"] = datetime.utcnow().isoformat()
        author["publications"] = {v["author_pub_id"]: v for v in author["publications"]}

        # 保存完整数据
        os.makedirs("results", exist_ok=True)
        with open("results/gs_data.json", "w", encoding="utf-8") as f:
            json.dump(author, f, ensure_ascii=False, indent=2)
            logger.info("Saved author data to results/gs_data.json")

        # 生成 Shields.io 数据
        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{author.get('citedby', 'N/A')}",
            "color": "9cf",
        }
        with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
            json.dump(shieldio_data, f, ensure_ascii=False)
            logger.info("Saved badge data to results/gs_data_shieldsio.json")

    except Exception as e:
        logger.error(f"Script failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
