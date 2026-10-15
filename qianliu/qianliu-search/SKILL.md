---
name: qianliu-search
description: 千流云实时联网检索服务。当需要联网搜索最新资讯/资料（返回标题/链接/摘要/发布时间）、或搜索图片（返回直链/缩略图/尺寸/作者）时使用本技能，结果可直接喂给模型。两个工具：web_search 通用搜索、img_search 图片搜索。
---

# 千流云联网搜索 Skill

Base URL：`https://api.qlcloud.top/gateway/search/v1`

## 鉴权

```
Authorization: Bearer sk-ql-***
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 通用搜索

`POST /search`

请求体（JSON）：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| model | string | 是 | 档位 id，当前为 `search-general` |
| query | string | 是 | 检索词（≤ 500 字符） |
| max_results | integer | 否 | 返回条数 1-20，默认 5（每 5 条一档计费） |

响应：

```json
{
  "query": "2026 年 AI 发展趋势",
  "results": [
    { "title": "...", "url": "https://...", "content": "摘要...", "published_date": "2026-09-01", "score": 0.95 }
  ]
}
```

示例（curl）：

```bash
curl https://api.qlcloud.top/gateway/search/v1/search \
  -H "Authorization: Bearer sk-ql-***" \
  -H "Content-Type: application/json" \
  -d '{"model": "search-general", "query": "2026 年 AI 发展趋势", "max_results": 10}'
```

示例（Python）：

```python
import httpx

resp = httpx.post(
    "https://api.qlcloud.top/gateway/search/v1/search",
    headers={"Authorization": "Bearer sk-ql-***"},
    json={"model": "search-general", "query": "2026 年 AI 发展趋势", "max_results": 10},
    timeout=30,
)
for r in resp.json()["results"]:
    print(r["title"], r["url"])
```

## 图片搜索

同一 `POST /search` 端点，`model` 传图片档位 `search-image`。响应的 `results` 每项含：

| 字段 | 说明 |
| --- | --- |
| title | 图片描述 |
| url | 详情页链接（含授权信息） |
| image_url | 图片直链（可直接贴入文章） |
| thumb_url | 缩略图 |
| width / height | 原始尺寸 |
| author | 作者 |

```bash
curl https://api.qlcloud.top/gateway/search/v1/search \
  -H "Authorization: Bearer sk-ql-***" \
  -H "Content-Type: application/json" \
  -d '{"model": "search-image", "query": "山地日落", "max_results": 10}'
```

**下载**：返回均为图库直链，可免费商用；浏览器内可直接使用/下载，程序化下载若遇 403，给请求加上 `Referer` 头（取该图详情页 `url` 的域名）重试即可。

## 错误码

| 状态码 | 含义 | 处理 |
| --- | --- | --- |
| 400 | 参数错误（query 为空 / max_results 非整数） | 核对请求字段 |
| 401 | API Key 无效 | 检查 Key 状态 |
| 402 | 余额不足 | 控制台充值 |
| 404 | 模型不存在或未上架 | 取「可用模型」表中的 model_id |
| 429 | 触发限流 | 降低并发 |
| 502 | 检索服务暂时不可用 | 稍后重试 |
