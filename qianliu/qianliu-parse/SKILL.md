---
name: qianliu-parse
description: 千流云文档解析服务。当需要把 Office / PDF / 图片文档转成标准 Markdown（RAG 入库、资料整理、扫描件识别的标准前置环节）时使用本技能。Office 与文本型 PDF 同步直返；扫描件/图片走 OCR 异步任务轮询。
---

# 千流云文档解析 Skill

Base URL：`https://api.qlcloud.top/gateway/parse/v1`

## 鉴权

```
Authorization: Bearer sk-ql-***
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 支持格式与限制

- PDF（文本型本地解析；扫描件/图片型走 OCR 引擎）
- 图片：png / jpg / jpeg / webp / bmp / tiff（OCR 引擎）
- Word：doc / docx / docm
- PowerPoint：ppt / pps / pot / pptx / pptm / ppsx / ppsm
- Excel：xls / xlsx / xlsm / xlsb
- OpenDocument / RTF：odt / ods / odp / rtf
- 单文件 ≤ 50MB（扫描件/图片 ≤ 400 页）；epub / html / csv 暂不支持
- 计费：Office/文本 PDF **按字符**、扫描件/图片**按页**（单价以「接入指南」页目录为准），失败不计费；文件零缓存，结果仅保留 2 小时，请及时下载

## 文档解析

`POST /parse`（multipart 表单）

| 字段 | 位置 | 必填 | 说明 |
| --- | --- | --- | --- |
| file | 表单字段 | 是 | 文档文件 |

**响应形态**：Office/文本型 PDF 同步 200 直返结果；**扫描件/图片统一 202** + `task_id`（OCR 任务制），轮询取结果。

```bash
curl https://api.qlcloud.top/gateway/parse/v1/parse \
  -H "Authorization: Bearer sk-ql-***" \
  -F "file=@商业计划书.docx"

# 快路径响应 200：
# {"markdown": "# 一、项目概述\n\n...", "pages": 0, "chars": 19196,
#  "meta": {"ext": "docx", "latency_ms": 860}}

# 慢路径响应 202：
# {"task_id": "a1b2c3...", "status": "running", "pages": 120}
```

## 任务轮询（异步）

`GET /parse/{task_id}`

```bash
curl https://api.qlcloud.top/gateway/parse/v1/parse/a1b2c3... \
  -H "Authorization: Bearer sk-ql-***"

# {"status": "running", "pages": 120}
# {"status": "completed", "pages": 120, "markdown": "..."}
```

status：`running` / `completed`（带 markdown）/ `failed`（带 error）。建议每 3-5 秒轮询一次。

## Python 完整示例

```python
import time
import httpx

BASE = "https://api.qlcloud.top/gateway/parse/v1"
HEADERS = {"Authorization": "Bearer sk-ql-***"}

def parse_file(path: str) -> str:
    with open(path, "rb") as f:
        resp = httpx.post(f"{BASE}/parse", headers=HEADERS, files={"file": f}, timeout=300)
    resp.raise_for_status()
    if resp.status_code == 200:
        return resp.json()["markdown"]
    task_id = resp.json()["task_id"]  # 202：异步轮询
    while True:
        time.sleep(3)
        t = httpx.get(f"{BASE}/parse/{task_id}", headers=HEADERS, timeout=30).json()
        if t["status"] == "completed":
            return t["markdown"]
        if t["status"] == "failed":
            raise RuntimeError(t.get("error", "parse failed"))

markdown = parse_file("report.pdf")
```

## 错误码

| 码 | 含义 |
| --- | --- |
| 400 | 格式不支持 / 文件过大 / 页数超限 / 文件损坏或加密 |
| 401 | API Key 无效或已吊销 |
| 402 | 余额不足 |
| 404 | 任务不存在或已过期 |
| 429 | 触发限流 |
| 502 | 解析服务暂时不可用 |
