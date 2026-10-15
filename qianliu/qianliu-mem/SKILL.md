---
name: qianliu-memory
description: 千流云长期记忆服务。当需要跨会话记住用户偏好/事实/对话要点、随时语义检索已记忆的内容、或让大脑基于全部记忆归纳回答问题时使用本技能。核心操作：retain 写入、recall 检索、reflect 反思。
---

# 千流云长期记忆 Skill

Base URL：`https://api.qlcloud.top/gateway/memory/v1`

## 鉴权

```
Authorization: Bearer sk-ql-***
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 大脑（bank）：记忆的容器，先建后用

`POST /banks`

请求体（JSON）：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| name | string | 是 | 大脑名称（≤ 50 字符） |
| desc | string | 否 | 描述（≤ 200 字符） |
| retain_mission | string | 否 | 写入策略：哪些该记、哪些忽略，如「只记用户偏好，忽略寒暄」 |

响应：`{"bank_id": "550e8400-e29b-41d4-a716-446655440000"}`——妥善保存，后续所有操作都带它。

管理端点：`GET /banks`（列表）· `GET / PATCH / DELETE /banks/{bank_id}`（详情/编辑/删除，删除清除全部记忆，不可逆）。

查看记忆：`GET /memories?bank=&page=&page_size=&q=`（分页 + 全文搜索）；`PATCH /memories/{memory_id}?bank=`（编辑正文）· `DELETE /memories/{memory_id}?bank=`（软删除）。注意：「观察」（自动归纳的派生记忆）只读，不可编辑/删除——改它对应的源事实即可。

## 记忆写入

`POST /retain`

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| bank | string | 是 | 大脑 id |
| content | string | 是 | 要记住的内容（对话/笔记/事实原文，≤ 10 万字符） |
| context | string | 否 | 内容背景（如「项目周会」） |
| timestamp | string | 否 | 内容发生时间（ISO 格式；回填历史数据时用，默认当前） |

响应：`{"bank": "...", "items_count": 1, "tokens": 3749}`（tokens = 实际消耗，含提取开销）

```bash
curl https://api.qlcloud.top/gateway/memory/v1/retain \
  -H "Authorization: Bearer sk-ql-***" \
  -H "Content-Type: application/json" \
  -d '{"bank": "550e8400-...", "content": "用户对花生过敏，不吃辣", "context": "饮食偏好"}'
```

## 记忆检索

`POST /recall`

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| bank | string | 是 | 大脑 id |
| query | string | 是 | 检索问题（自然语言即可） |

响应（每条含综合相关度 score，语义+关键词+图谱+时序四路召回 + 重排序）：

```json
{
  "bank": "550e8400-...",
  "query": "用户在饮食上有哪些忌口",
  "results": [
    { "id": "...", "text": "用户对花生过敏", "type": "world", "context": "饮食偏好", "entities": ["用户", "花生"], "score": 0.95 }
  ]
}
```

```python
import httpx

resp = httpx.post(
    "https://api.qlcloud.top/gateway/memory/v1/recall",
    headers={"Authorization": "Bearer sk-ql-***"},
    json={"bank": bank_id, "query": "用户在饮食上有哪些忌口"},
    timeout=30,
)
for m in resp.json()["results"]:
    print(m["text"])  # 可直接拼进 system prompt
```

## 记忆反思

`POST /reflect`——带着问题问大脑，LLM 基于全部记忆归纳回答（区别于检索只回原文）。

```bash
curl https://api.qlcloud.top/gateway/memory/v1/reflect \
  -H "Authorization: Bearer sk-ql-***" \
  -H "Content-Type: application/json" \
  -d '{"bank": "550e8400-...", "query": "该用户有什么偏好"}'

# {"bank": "...", "query": "...", "text": "## 用户偏好\n\n- 饮食：花生过敏，不吃辣\n- ...", "tokens": 9922}
```

## 错误码

| 状态码 | 含义 | 处理 |
| --- | --- | --- |
| 400 | 参数错误（bank/content/query 缺失、content 超长） | 核对请求字段 |
| 401 | API Key 无效 | 检查 Key 状态 |
| 402 | 余额不足 | 控制台充值 |
| 404 | 大脑不存在或不属于当前账户 | 核对 bank_id；列表见 GET /banks |
| 429 | 触发限流 | 降低并发 |
| 502 | 记忆服务暂时不可用 | 稍后重试 |
