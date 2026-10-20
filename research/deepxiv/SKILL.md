---
name: deepxiv
description: 学术论文搜索与原文下载工具。用于搜索 arXiv/PMC 论文、获取摘要、阅读具体章节，以及下载论文 PDF 和 LaTeX 源文件到 raw/ 目录。触发场景：用户要求搜索学术论文、查找文献、读论文、查热门论文、下载论文原文。
---

# deepxiv — 学术论文搜索与原文下载

两部分能力：**搜索阅读**用 DeepXiv CLI（解析后的 markdown），**原文下载**用 arXiv 官方端点（PDF / LaTeX 源码）。

| 需求 | 用什么 |
|------|--------|
| 搜索、快速筛选、日常阅读 | deepxiv 命令（md，省 token 分层读） |
| 离线存档、精读公式图表、审稿对照 | 原文下载（PDF / LaTeX） |

## 安装

```bash
pip install deepxiv-sdk
```

## 一、搜索

```bash
# 搜索论文
deepxiv search "YOLO object detection" --limit 10

# 快速摘要
deepxiv paper 2507.12727 --brief

# 看论文结构（所有章节概览）
deepxiv paper 2507.12727 --head

# 读具体章节
deepxiv paper 2507.12727 --section Introduction

# 全文
deepxiv paper 2507.12727

# 热门论文
deepxiv trending --days 7 --limit 10

# 查 token 状态
deepxiv token
```

**参数**：`--limit N` 结果数量；`--format json` 程序处理用；`--section <名>` 读指定章节。

## 二、原文下载（PDF / LaTeX）

arXiv 官方端点，无需 token：

| 格式 | 端点 | 用途 |
|------|------|------|
| PDF | `https://arxiv.org/pdf/<arxiv_id>` | 日常阅读、批注、存档 |
| LaTeX | `https://arxiv.org/e-print/<arxiv_id>` | 公式/图表源码、精确排版对照 |

### 一键下齐 PDF + LaTeX（推荐）

```bash
# 以 RemoteCLIP (2306.11029) 为例
download_paper() {
  local ID=$1 NAME=$2 DATE=$3
  # PDF
  curl -L --retry 3 -o raw/${DATE}-${NAME}.pdf "https://arxiv.org/pdf/${ID}"
  # LaTeX
  curl -L --retry 3 -o /tmp/${NAME}.tar.gz "https://arxiv.org/e-print/${ID}"
  mkdir -p raw/${DATE}-${NAME}-latex
  tar -xzf /tmp/${NAME}.tar.gz -C raw/${DATE}-${NAME}-latex 2>/dev/null \
    || gunzip -c /tmp/${NAME}.tar.gz > raw/${DATE}-${NAME}-latex/main.tex
  rm -f /tmp/${NAME}.tar.gz
  sleep 3   # arXiv 限速保护
}

download_paper 2306.11029 remoteclip 2023-06-19
```

### 只下单一格式

```bash
# 只下 PDF
curl -L --retry 3 -o raw/2023-06-19-remoteclip.pdf "https://arxiv.org/pdf/2306.11029"

# 只下 LaTeX
curl -L --retry 3 -o /tmp/rc.tar.gz "https://arxiv.org/e-print/2306.11029"
mkdir -p raw/2023-06-19-remoteclip-latex
tar -xzf /tmp/rc.tar.gz -C raw/2023-06-19-remoteclip-latex && rm /tmp/rc.tar.gz
```

### 目录规范（与 paperNotes 工作流对齐）

```
raw/
├── 2023-06-19-remoteclip.md            # md 笔记（deepxiv 生成）
├── 2023-06-19-remoteclip.pdf           # PDF 原文
└── 2023-06-19-remoteclip-latex/        # LaTeX 源码目录
    ├── main.tex
    ├── figures/
    └── refs.bib
```

命名：`<发表日期>-<论文短名>` 三者保持一致，便于对应。

## 注意事项

- **分层阅读省 token**：先 `--brief` 快速筛选，确定要读再 `--section`；`--brief` ~500 tokens，单章节 ~1-5k，全文 ~10-50k
- **arXiv ID**：格式 `2507.12727`（非 `arXiv:2507.12727`）；deepxiv 日限 1000 次
- **不是所有论文都有 LaTeX 源码**：少数作者只上传 PDF，e-print 端点会返回 PDF（`file` 命令判断），跳过 LaTeX 即可
- **arXiv 限速**：批量下载加 `--retry 3`，每篇 sleep ≥3s
- **版本**：默认最新版；要特定版本在 ID 后加 `vN`

## 错误处理

| 现象 | 原因 | 解决 |
|------|------|------|
| deepxiv `NotFoundError` | arXiv ID 格式错误 | 核对 ID 格式 |
| deepxiv `RateLimitError` | 超日限 | 等明天或申请更高限额 |
| 下载 404 | ID 错误或论文被撤回 | 核对 arxiv ID |
| LaTeX 下载得到 PDF | 作者未上传 LaTeX 源码 | 跳过，用 PDF/markdown 阅读 |
| tar 解压失败 | 实际是单一 gzip .tex（老论文常见） | `gunzip -c xx.tar.gz > main.tex` |
| PDF 只有几十 KB | 下载被拦截成 HTML 提示页 | `file` 检查，稍后重试 |
