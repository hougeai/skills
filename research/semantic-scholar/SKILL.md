---
name: semantic-scholar
description: 学术论文搜索与元数据查询。用于搜索全学科论文（~2亿）、查引用关系、获取 IEEE/CVF 会议论文元数据。触发场景：deepxiv 搜不到时补漏、需要引用关系、需要查 IEEE/CVF/ACM 会议论文。
---

# Semantic Scholar — 学术搜索 API

需要 API key（[Semantic Scholar API](https://www.semanticscholar.org/product/api#api-key) 免费申请），存放在本 skill 目录的 `.env`：

```bash
export SS_API_KEY="xxxxxxxx"        # 或直接读取本 skill 目录下的 .env
```

## 覆盖范围

- **arXiv**、**IEEE**、**CVF/ACM**、**Springer**、**Nature**、**Science** 等
- 约 2.25 亿论文，6.5 亿引用关系

## API 调用示例

```python
import os
from dotenv import load_dotenv
from pathlib import Path
import requests

# 加载 token：读取本 skill 目录下的 .env（SS_API_KEY=...）
load_dotenv(Path(__file__).resolve().parent / ".env")
api_key = os.getenv("SS_API_KEY")

BASE_URL = "https://api.semanticscholar.org/graph/v1"
headers = {"x-api-key": api_key}

# 搜索论文
def search_papers(query, limit=10):
    url = f"{BASE_URL}/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,venue,citationCount,externalIds,url"
    }
    r = requests.get(url, params=params, headers=headers)
    return r.json()

# 查论文详情
def get_paper(paper_id, fields="title,abstract,citationCount,references,citations"):
    url = f"{BASE_URL}/paper/{paper_id}"
    params = {"fields": fields}
    r = requests.get(url, params=params, headers=headers)
    return r.json()

# 查引用/参考文献
def get_citations(paper_id, limit=100):
    url = f"{BASE_URL}/paper/{paper_id}/citations"
    params = {"limit": limit, "fields": "title,authors,year,venue"}
    r = requests.get(url, params=params, headers=headers)
    return r.json()

def get_references(paper_id, limit=100):
    url = f"{BASE_URL}/paper/{paper_id}/references"
    params = {"limit": limit, "fields": "title,authors,year,venue"}
    r = requests.get(url, params=params, headers=headers)
    return r.json()
```

## 使用流程

```python
# 1. 搜索论文
results = search_papers("VisDrone object detection", limit=10)
for p in results.get("data", []):
    print(f"{p.get('year')} | {p.get('title')}")
    print(f"  venue: {p.get('venue')}, citations: {p.get('citationCount')}")

# 2. 获取详情（用 paper ID）
paper_detail = get_paper("DOI:10.1109/CVPR.2023.00001")

# 3. 查引用关系
citations = get_citations("CorpusId:215416146", limit=50)
references = get_references("CorpusId:215416146", limit=50)
```

## paper_id 类型

- Semantic Scholar ID：`CorpusId:215416146`
- DOI：`DOI:10.1109/CVPR.2023.00001`
- arXiv：`arXiv:2301.10140`

## 全文获取

SS API **不提供全文**，只有元数据+摘要。

获取全文：
1. 从 `externalIds` 取 DOI，去期刊官网下载
2. 用 `deepxiv` 搜 arXiv 版本

## 注意事项

- **速率限制**：有 API key 后更高
- **fields 参数**：只请求需要的字段，减少数据量