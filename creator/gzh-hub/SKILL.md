---
name: gzh-hub
description: 当任务需要实际操作微信公众号内容生产时使用——粘贴 URL 导入公众号文章、关键词/公众号/收藏夹多维度检索知识库、Markdown 排版一键推送公众号草稿箱（图文 news / 贴图 newspic 双体裁）、AI 生成标题与摘要、上传图床。仅覆盖到推送草稿箱为止（正式发布由用户人工操作）。仅在需要调用 API 实际操作时使用：公众号运营观点讨论、平台概念解释、写作润色本身（不涉及推送/收藏/检索）等无需调接口的话题不要加载本 skill。
version: 1.0.0
---

# GzhHub 公众号创作工作台 · 开放 API 工具包

三大能力域 · 13 个端点：

- **1 文章收藏**（1.1-1.2）：导入微信文章（URL → Markdown + AI 摘要）、删除——建知识库的写入侧
- **2 文章检索**（2.1-2.4）：关键词/公众号/收藏夹筛选、按 id 取正文、公众号与收藏夹列表——读侧（知识库问答由 Agent 取正文后自行作答，无后端问答端点）
- **3 排版发布**（3.1-3.7）：先拿已绑定公众号 mp_id（3.1）→ 选主题（图文/贴图）→ 内容准备（图床图片、标题、摘要）→ 推送草稿箱（图文/贴图双体裁）。Agent 链路到草稿箱为止

**安装：** 放到所用 Agent 自己的技能目录：Claude Code `~/.claude/skills/gzh-hub/SKILL.md`（项目级 `.claude/skills/gzh-hub/`）、Cursor `~/.cursor/skills/gzh-hub/`、Codex `~/.codex/skills/gzh-hub/`。

## 端点路由速查（按需定位，不必通读全文）

**能力域 1 · 文章收藏**

| 端点 | 方法 | 拿什么 / 干什么 |
|------|------|----------------|
| 1.1 `/collections/articles/import` | POST | 粘贴微信文章 URL → 转 Markdown 入库 + 异步 AI 摘要 |
| 1.2 `/collections/articles/delete` | DELETE | 删除文章 |

**能力域 2 · 文章检索**

| 端点 | 方法 | 拿什么 / 干什么 |
|------|------|----------------|
| 2.1 `/collections/articles/list` | GET | 文章列表（分页 + 关键字/公众号/收藏夹筛选，不含正文） |
| 2.2 `/collections/articles/get` | GET | 文章详情（含 Markdown 正文） |
| 2.3 `/collections/feeds/list` | GET | 公众号列表（按用户文章聚合，含 AI 简介） |
| 2.4 `/collections/collections/list` | GET | 收藏夹列表 |

**能力域 3 · 排版发布**

| 端点 | 方法 | 拿什么 / 干什么 |
|------|------|----------------|
| 3.1 `/accounts/list` | GET | 当前用户绑定的公众号列表（拿 mp_id，推送前必调） |
| 3.2 `/themes/news/list` | GET | 图文排版主题列表（选 theme_id） |
| 3.3 `/themes/newspic/list` | GET | 贴图主题列表（选 theme_id） |
| 3.4 `/drafts/image` | POST | 上传图片到图床（multipart，得封面/插图 URL） |
| 3.5 `/drafts/digest` | POST | AI 生成摘要（≤120 字，直传 content） |
| 3.6 `/drafts/title` | POST | AI 生成标题（article_type 控制体裁口径） |
| 3.7 `/publish/draft` | POST | **核心端点**：Markdown 推送公众号草稿箱，双体裁（3.7.1 图文 / 3.7.2 贴图自动分页） |

## 使用铁律（先读，四条）

### 1. 认证：X-Api-Key，不要把 Key 写进代码

```bash
export GZHUB_API_KEY="sk-gzh-xxxxxxxxxxxx"        # 控制台「API 密钥」页创建
```

所有请求带 header `X-Api-Key: sk-gzh-xxx`。Key 无效/未传返回 `401`。**没有 Key 时先引导用户注册创建，不要瞎猜硬调。**

> API Key 获取地址：https://gzhhub.qlcloud.top/user-center/apikey

### 2. 统一响应：判 code，别只看 HTTP 状态码

```json
{ "code": 200, "msg": "success", "data": {} }          // 成功
{ "code": 200, "data": [], "total": 100, "page": 1 }   // 分页成功（total 与 data 平级）
{ "code": 400, "msg": "积分不足，请充值" }               // 失败：HTTP 状态码与 code 一致，msg 是原因
```

关键错误码：`400` 参数错/业务失败/积分不足 · `401` Key 无效 · `404` 资源不存在 · `422` 请求体格式错。**遇到 400 先读 `msg`**，错误信息都是中文人话（如"文章已存在，请勿重复导入"）。积分不足（`msg="积分不足，请充值"`）时**停止重试**并提示用户到控制台充值——开放 API 没有余额查询接口，不要试图查余额。批量写操作串行执行、失败即停，不要并发轰炸。

### 3. 字数口径：公众号编辑器口径，不是字符数

标题等字数限制按**全角（汉字/全角标点）1 字、半角（字母/数字/半角符号/空格）0.5 字**计算：
- 图文（news）标题 ≤ 64 字 → 纯英文最多 128 字符
- 贴图（newspic）标题 ≤ 20 字 → 纯英文最多 40 字符
- 摘要 ≤ 120 字（同口径）

**生成内容后自查按此口径，别用 `len()` 数字符**，英文标题会冤枉超限。

### 4. 前置依赖：推送草稿箱需要用户已绑定公众号

推送草稿箱要求用户已在 GzhHub 控制台完成公众号授权（配置 AppID + AppSecret）。未绑定时返回 `msg="公众号凭证缺失..."`——此时引导用户去控制台「公众号授权」页配置，**API 无法代替完成绑定**（需要微信侧密钥）。注意：**正式发布不由 API 完成**——推送成功后告知用户到前端（或公众号后台）人工发布。

---

# 1 文章收藏（建知识库的写入侧）

## 1.1 导入文章

粘贴微信文章链接导入（同 URL 已存在时会报"文章已存在"，此时不要重试，改走 2.1 查已有文章）。

```bash
curl -X POST "https://api.qlcloud.top/gzhhub/v1/open/collections/articles/import" \
  -H "X-Api-Key: $GZHUB_API_KEY" -H "Content-Type: application/json" \
  -d '{"url": "https://mp.weixin.qq.com/s/xxxxxx"}'
```

```json
{ "code": 200, "msg": "success", "data": {
  "id": 123, "title": "...", "url": "...", "mp_id": "gh_xxx", "author": "...",
  "description": "...", "cover_image_url": "...", "publish_time": "2026-08-10 10:00:00",
  "ai_summary": null, "status": 1 } }
```

⚠️ **`ai_summary` 是异步生成的**：导入返回时必为 `null`，几秒后经 2.1/2.2 拿到。别在导入后立刻断言摘要为空是 bug。

## 1.2 删除文章

```bash
curl -X DELETE -H "X-Api-Key: $GZHUB_API_KEY" \
  "https://api.qlcloud.top/gzhhub/v1/open/collections/articles/delete?id=123"
```

---

# 2 文章检索（浏览 · 搜索 · 取正文）

**检索场景速查**（先对场景再调端点）：

| 你想知道 | 用哪个端点 |
|---|---|
| 关注了哪些公众号（含 mp_id / 文章数 / AI 简介） | 2.3 `/collections/feeds/list` |
| 分了哪几个收藏夹 | 2.4 `/collections/collections/list` |
| 某个公众号下有哪些文章 | 2.1 `/collections/articles/list?mp_id=gh_xxx`（mp_id 从 2.3 拿） |
| 按关键词搜文章（标题匹配，可叠加公众号/收藏夹筛选） | 2.1 `/collections/articles/list?keyword=AI` |
| 按文章 id 拿正文全文（content_md） | 2.2 `/collections/articles/get?id=123` |

典型链路：2.3 拿公众号列表 → 2.1 按 mp_id / keyword 筛文章 → 2.2 取正文。

## 2.1 文章列表 / 2.2 文章详情

```bash
# 列表（不含正文）：page/page_size(≤100)/keyword/mp_id/collection_id(0=全部)
curl -H "X-Api-Key: $GZHUB_API_KEY" \
  "https://api.qlcloud.top/gzhhub/v1/open/collections/articles/list?page=1&page_size=20&keyword=AI"

# 详情（含 content_md 全文）
curl -H "X-Api-Key: $GZHUB_API_KEY" \
  "https://api.qlcloud.top/gzhhub/v1/open/collections/articles/get?id=123"
```

列表项含 `mp_name`（公众号名，详情接口没有——列表由 Feed 表回填）。

## 2.3 公众号列表 / 2.4 收藏夹列表

```bash
curl -H "X-Api-Key: $GZHUB_API_KEY" "https://api.qlcloud.top/gzhhub/v1/open/collections/feeds/list"
curl -H "X-Api-Key: $GZHUB_API_KEY" "https://api.qlcloud.top/gzhhub/v1/open/collections/collections/list"
```

2.3 每项含 `mp_id / mp_name / mp_cover / ai_intro / article_count`——`mp_id` 是 2.1 按公众号筛文章的筛选值。

---

# 3 排版发布

## 3.1 获取已绑定公众号（推送前必调）

推送需要 `mp_id`，先调此接口拿到当前用户已绑定的公众号列表（返回仅含 `mp_id` / `mp_name`，**不含任何密钥**）：

```bash
curl -H "X-Api-Key: $GZHUB_API_KEY" "https://api.qlcloud.top/gzhhub/v1/open/accounts/list"
```

```json
{ "code": 200, "data": [ { "mp_id": "gh_xxx", "mp_name": "GzhHub" } ], "total": 1, "page": 1, "page_size": 20 }
```

未绑定任何公众号时 `data` 为空数组——引导用户去控制台「公众号授权」页绑定（API 无法代绑定）。拿到的 `mp_id` 即 3.7 推送的 `mp_id`。

## 3.2 图文主题 / 3.3 贴图主题

两接口均支持可选 query 参数 `category` 按分类筛选，**不传 = 返回全部**：

| 接口 | category 取值 |
|------|--------------|
| 3.2 `/themes/news/list` | tech / product / knowledge / news / essay |
| 3.3 `/themes/newspic/list` | classic / creative / retro / tech |

```bash
# 带筛选
curl -H "X-Api-Key: $GZHUB_API_KEY" "https://api.qlcloud.top/gzhhub/v1/open/themes/news/list?category=knowledge"
# 不带筛选（全部）
curl -H "X-Api-Key: $GZHUB_API_KEY" "https://api.qlcloud.top/gzhhub/v1/open/themes/newspic/list"
```

3.2 返回 `theme_id`（如 `default`）供 3.7.1 图文模式用；3.3 返回贴图主题（如 `theme-warm` 暖阳日记）供 3.7.2 贴图模式用。

## 3.4 上传图片（图床）

```bash
curl -X POST "https://api.qlcloud.top/gzhhub/v1/open/drafts/image" \
  -H "X-Api-Key: $GZHUB_API_KEY" \
  -F "file=@cover.jpg"
```

返回 `{url, id}`。图片直接上传即返回公网 URL。⚠️ **临时图床 7 天过期**：推送草稿箱后正文/封面图片会自动转存微信素材库，之后不再依赖图床——所以"上传 → 尽快推送"即可，不要囤图。

**正文内联图片同理**：Markdown 正文里 `![](...)` 的图片若来自本地文件，也必须先经本接口上传、拿公网 URL 替换原链接，再送 3.7 推送（见 3.7.1 说明）。

## 3.5 AI 生成摘要 / 3.6 AI 生成标题

```bash
curl -X POST "https://api.qlcloud.top/gzhhub/v1/open/drafts/digest" \
  -H "X-Api-Key: $GZHUB_API_KEY" -H "Content-Type: application/json" \
  -d '{"content": "# 标题\n\n正文 Markdown..."}'

curl -X POST "https://api.qlcloud.top/gzhhub/v1/open/drafts/title" \
  -H "X-Api-Key: $GZHUB_API_KEY" -H "Content-Type: application/json" \
  -d '{"content": "# 标题\n\n正文 Markdown...", "article_type": "news"}'
```

- `content` 至少 20 字（太短直接 400）
- 3.6 的 `article_type` 决定标题体裁口径，生成结果已按对应体裁**自动截断**，直接可用，无需再处理——作 3.7 的 `title` 即可
- 两者正文分别取前 2000 / 4000 字送 LLM

## 3.7 推送草稿箱（核心端点，双体裁）

### 3.7.1 图文模式（`article_type: "news"`，默认）

Markdown → HTML 渲染（主题 + 样式可配）→ 图片转存微信 → 推送草稿箱：

```bash
curl -X POST "https://api.qlcloud.top/gzhhub/v1/open/publish/draft" \
  -H "X-Api-Key: $GZHUB_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "mp_id": "gh_xxx",
    "title": "GzhHub 上线公告",
    "digest": "公众号文章一站式工具平台",
    "author": "GzhHub",
    "cover_url": "https://...",
    "content": "# 欢迎使用 GzhHub\n\n正文内容...",
    "theme_id": "default",
    "theme_config": { "primary_color": "#2563EB", "font_size": "16px", "show_caption": true }
  }'
```

- `mp_id`：用户已绑定的公众号（gh_xxx，先调 3.1 获取）
- `cover_url`：图文模式必填（先走 3.4 上传）
- `theme_config` 可整体省略（用主题内置默认值），每个键都是覆盖项，可只传需要改的：`primary_color / font / font_size / heading_styles / show_caption / cite_status / use_indent / use_justify`
- 响应 `data.media_id`

⚠️ **content 里的图片必须是公网 URL**：推送时后端会按 Markdown 中的图片地址下载并转存微信素材库，只能处理 `http(s)://` 公网链接。**本地链接（`file:///...`、`./images/x.png`、`C:\...` 等）后端无权限访问，会推送失败或图片裂开。** 若用户给的是本地 Markdown，Agent 须先把其中每张本地图片用 3.4 上传换取公网 URL，替换进 Markdown 后再调本接口。

### 3.7.2 贴图模式（`article_type: "newspic"`）

**调用方只传 Markdown**：服务端自动分页（与编辑器同算法）→ puppeteer 渲染 PNG → 逐张上传 → 推图片消息草稿。无需 cover_url（首张即封面）：

```bash
curl -X POST "https://api.qlcloud.top/gzhhub/v1/open/publish/draft" \
  -H "X-Api-Key: $GZHUB_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "mp_id": "gh_xxx",
    "title": "每日金句",
    "article_type": "newspic",
    "content": "# 每日金句\n\n把注意力放在你能改变的事情上。\n\n## 三条原则\n\n- 先完成，再完美\n- 输出是最好的输入\n\n---\n\n## 一段长文\n\n...",
    "theme_id": "theme-warm"
  }'
```

- `content` 语法：`#` 一级标题作封面、`##` 作章节标题、`---` 整行作显式分页符
- 主题统一由顶层 `theme_id` 指定（如 `theme-warm`）；`newspic_config` 只放定制项（kicker/date/quote/justify/platform），可整体省略
- 可选项：`kicker`（页眉徽标，默认"公众号贴图"）、`date`（页脚日期，默认今天）、`quote`（页脚签名）、`justify`（两端对齐）、`platform`（默认 1080×1440）
- 最多 20 张 PNG（微信上限），超了报错让用户精简
- 响应 `data.wechat_newspic_id` + `media_id` + `image_count`

**图文 vs 贴图怎么选**：长文深度内容用图文；金句/清单/卡片类轻内容用贴图（手机端展示更精致）。
