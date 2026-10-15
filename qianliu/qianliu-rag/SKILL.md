---
name: qianliu-rag
description: 千流云知识库（RAG）服务。当用户要求把文档/资料传入知识库、基于库内文档智能问答（回答带出处）、或对库内文档做语义检索取回片段自行拼接 prompt 时使用本技能。两种建库形态：纯向量库（默认，零抽取成本秒级入库）与向量库+图谱（可答关系型问题）。
---

# 千流云知识库 Skill

Base URL：`https://api.qlcloud.top/gateway/rag/v1`

## 鉴权

```
Authorization: Bearer sk-ql-***
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 知识库（kb）：文档的容器，先建后用

`POST /kbs`

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| name | string | 是 | 知识库名称（≤ 50 字符） |
| desc | string | 否 | 描述（≤ 200 字符） |
| lang | string | 否 | 库语言 `Chinese`（默认）/ `English`——实体沉淀语言，**建后不可改**（改了图谱双语混杂），英文文档为主的库建库时选 English |
| skip_kg | bool | 否 | **缺省 `true`** = 纯向量库（入库零 LLM 成本秒级完成，问答退化为段落召回）；显式 `false` 才建图谱（可答关系型问题），**建后不可改** |

响应：`{"kb_id": "550e8400-..."}`——妥善保存，后续所有操作都带它。

管理端点：`GET /kbs`（列表）· `GET / PATCH / DELETE /kbs/{kb_id}`（详情/编辑名称描述/删除整库，删除含全部文档与索引，不可逆）。

## 文档上传（提交制，后台处理）

`POST /kbs/{kb_id}/docs`

两种形态（二选一）：

- **文件**：`multipart/form-data`，字段 `file`（常见 Office / PDF / 图片，≤ 50MB；先经文档解析服务转 markdown，解析按各自单价单独计费）
- **文本**：JSON `{"text": "……", "file_name": "年假制度.txt"}`

响应（**提交即返，不等处理完成**）：

```json
{"kb": "550e8400-...", "doc_id": "doc-5bf22b13...", "status": "processing"}
```

入库在后台进行（解析/切片/向量化；图谱库另有实体关系抽取，分钟级）；`GET /kbs/{kb_id}/docs` 查看每篇状态（`processing` → `processed` / `failed`）。**处理完成才自动计费**：索引费按切片数 + 图谱抽取按 LLM 实耗（纯向量库只有索引费）；`DELETE /kbs/{kb_id}/docs/{doc_id}` 删除文档（含切片与索引，不可逆）。

`failed` = 抽取中断（如上游限流）：**chunk 已全量向量化、可正常检索**，仅图谱不完整。`POST /kbs/{kb_id}/docs/{doc_id}/retry` 续跑补齐——不重新上传（引擎读库内原文），已处理部分走缓存零成本，只补缺失部分。

```bash
# 文本直传
curl https://api.qlcloud.top/gateway/rag/v1/kbs/550e8400-.../docs \
  -H "Authorization: Bearer sk-ql-***" \
  -H "Content-Type: application/json" \
  -d '{"text": "年假制度：入职满一年可休 5 天……", "file_name": "年假制度.txt"}'

# 文件上传
curl https://api.qlcloud.top/gateway/rag/v1/kbs/550e8400-.../docs \
  -H "Authorization: Bearer sk-ql-***" \
  -F "file=@股权协议.docx"
```

## 智能问答

`POST /query`——混合检索后生成回答（带出处；纯向量库为段落召回）。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| kb | string | 是 | 知识库 id |
| query | string | 是 | 问题（自然语言） |

响应：`{"kb": "...", "query": "...", "answer": "……", "tokens": 2418}`（tokens = 实际消耗，按量计费，典型问答 ~2-3k tokens）

```python
import httpx

resp = httpx.post(
    "https://api.qlcloud.top/gateway/rag/v1/query",
    headers={"Authorization": "Bearer sk-ql-***"},
    json={"kb": kb_id, "query": "年假有几天"},
    timeout=60,
)
print(resp.json()["answer"])
```

## 语义搜索

`POST /search`——只检索不生成，按次计费。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| kb | string | 是 | 知识库 id |
| query | string | 是 | 检索词 |
| context | bool | 否 | `true` = 返回 LLM 就绪的上下文文本（含出处编号，**供自有模型直接拼接 prompt**）；缺省返回结构化片段 |

默认响应：`{"kb": "...", "query": "...", "chunks": [{"content": "……", "file_path": "年假制度.txt"}, ...]}`

`context=true` 响应：`{"kb": "...", "query": "...", "context": "Document Chunks …\n（可直接拼入自有 LLM 提示词的上下文文本）"}`

## 错误码

| 状态码 | 含义 | 处理 |
| --- | --- | --- |
| 400 | 参数错误（缺 kb/query、文件类型不支持、文件过大） | 核对请求字段 |
| 401 | API Key 无效或已吊销 | 检查 Key 状态 |
| 402 | 余额不足 | 控制台充值 |
| 404 | 知识库或文档不存在（或非本人名下） | 核对 kb_id；列表见 GET /kbs |
| 429 | 触发限流（按 Key 每分钟额度） | 降低调用频率 |
| 502 | 知识库引擎暂时不可用 | 稍后重试；持续出现请工单反馈 |
