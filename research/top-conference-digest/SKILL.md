---
name: top-conference-digest
description: 顶会论文整理：从 PapersWithCode API 抓取指定会议+task 的论文，关键词过滤后整理到顶会专题
---

# Top Conference Digest — 顶会论文整理

## 使用场景

用户说「抓取 CVPR 2026 的 object detection 论文」时，执行此 skill。

## 工作流

### 1. 抓取 + 过滤

```bash
python3 scripts/top-conf-digest.py --conference cvpr-2026 --task object-detection
```

> 在本 skill 目录下执行；脚本内部按自身位置定位路径，输出目录不存在会自动创建。

脚本从 PapersWithCode API 分页拉取全部论文，用 `INCLUDE_KEYWORDS` / `EXCLUDE_KEYWORDS` 过滤，输出 JSON 到 `data/digest-{conference}-{task}.json`。

### 2. LLM 分析 + 输出（⚠️ 必须用 LLM，不能用 Python 硬编码）

读取 `digest-{conference}-{task}.json`，**用 LLM 逐篇分析**生成推荐度和中文摘要。

**输出** `digest-{conference}-{task}-sum.json`，字段：
- `recommendation`: ⭐值得深入 / 📖可浏览 / ⏭不推荐
- `reason`: 推荐理由
- `summary_cn`: 中文摘要精简版（<150字，纯中文无英文）

### 3. 检查 + 生成 VitePress 页面

```bash
python3 scripts/digest-check.py --conference {conference} --task {task}
```

脚本读取 `data/digest-{conference}-{task}-sum.json`，**自动剔除 ⏭不推荐**，生成 `data/{conference}.md` 并更新 `data/index.md`。

## 输出格式

```markdown
## task-slug

### 1. [标题](arxiv或openaccess链接)
- **作者**: ...
- **推荐度**: ⭐值得深入 / 📖可浏览 / ⏭不推荐
- **推荐理由**: ...
> 摘要精简版

---
```

## 数据文件

数据统一输出到本 skill 目录的 `data/`（脚本按自身位置自动定位，与执行时 cwd 无关，目录不存在会自动创建）：

- `data/digest-{conference}-{task}.json` — 原始过滤结果
- `data/digest-{conference}-{task}-sum.json` — 分析结果
- `data/{conference}.md` — 整理后的 VitePress 页面
- `data/index.md` — 各 task 索引
