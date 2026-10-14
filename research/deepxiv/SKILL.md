---
name: deepxiv
description: 学术论文搜索与阅读工具。用于搜索 arXiv/PMC 论文、获取摘要、阅读具体章节。触发场景：用户要求搜索学术论文、查找文献、读论文、查热门论文。
---

# deepxiv — 学术论文搜索与阅读

使用 DeepXiv CLI 搜索和阅读 arXiv/PMC 学术论文。

## 安装

```bash
pip install deepxiv-sdk
```

## 使用

```bash
# 搜索论文
deepxiv search "YOLO object detection" --limit 10

# 快速摘要
deepxiv paper 2507.12727 --brief

# 看论文结构（所有章节概览）
deepxiv paper 2507.12727 --head

# 读具体章节
deepxiv paper 2507.12727 --section Introduction
deepxiv paper 2507.12727 --section Experiments

# 全文
deepxiv paper 2507.12727

# 热门论文
deepxiv trending --days 7 --limit 10

# 查 token 状态
deepxiv token
```

## 参数

- `--limit N` — 返回结果数量
- `--format json` — JSON 格式输出（程序处理用）
- `--section <章节名>` — 读取指定章节（Introduction/Methods/Experiments 等）

## 注意事项

- **分层阅读**：先 `--brief` 快速筛选，确定要读再 `--section` 读具体章节
- **token 成本**：`--brief` ~500 tokens，`--head` ~1-2k，单章节 ~1-5k，全文 ~10-50k
- **arXiv ID**：格式 `2507.12727`（非 `arXiv:2507.12727`）
- **日限**：默认 1000 次/天

## 错误处理

- `NotFoundError`: 检查 arXiv ID 格式
- `RateLimitError`: 等明天或申请更高限额