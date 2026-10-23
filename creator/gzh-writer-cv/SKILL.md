---
name: gzh-writer-cv
description: 「视觉与低空智能」公众号推文撰写。把论文解读文章改写成公众号推文，或就一个技术话题写原创推文。含本号写作规范：短句、无公式、裸链接、配图规则、AI 味黑名单、标题打法。触发场景：写公众号推文、发公众号、改写成推文、给视觉与低空智能号投稿。
version: 1.0.0
---

# gzh-writer-cv · 视觉与低空智能公众号推文

读者定位与写作口吻见 `references/style-guide.md`「读者与定位」。

## 铁律

全部写作规则**只维护在 `references/style-guide.md`**，冲突以它为准，本文件不重复。成稿后用 `scripts/check_prose.py` 机器自检，改法见 style-guide 的「怎么改」。

## skill 构成

```
gzh-writer-cv/
├── SKILL.md                    # 流程与执行步骤（写作规则统一在 style-guide）
├── references/style-guide.md   # 唯一写作参考（读者定位、材料关卡、标题、结构、句法、禁止清单、怎么改）
└── scripts/check_prose.py      # 成稿硬禁令检查脚本（只报警）
```

写作部分自包含：检测靠 `scripts/check_prose.py`，改法靠 `references/style-guide.md`。配图环节借两个外部 skill，`gzh-handdrawn` 出提示词，`qianliu-img` 出图。

## 流程

### Step 1 备料

- 首选素材是 `readings/YYYY-MM-DD-<slug>.md` 解读文章（里面的数字已核实过，配图已备好入仓）
- 需要补一手来源时按 paperNotes 的来源优先级取：arXiv LaTeX > 官方博客 > 仓库 README > 公众号文章
- 下载境外源超时时加代理（clone 仓库同理）：`export https_proxy=http://127.0.0.1:<本机代理端口>`
- 列材料清单：至少 5 件具体材料，凑不满就先补材料或写短文（材料类型与要求见 style-guide「动笔前第一关」）
- 查重：`search_file` 看 `gzh/` 下有没有同 slug 的推文

### Step 2 出标题

出 3 个候选，每个附 1-2 句理由，等用户挑。标题打法和红线见 references/style-guide.md。

### Step 3 撰文

**唯一写作参考是 `references/style-guide.md`，动笔前读一遍**（读者定位、材料关卡、标题打法、结构骨架、公式处理、段落与句子规则、禁止清单都在里面）。

章节结构严格沿用解读文章的章节，规则见 style-guide「结构」。

### Step 4 机器检查与清理

```bash
python3 scripts/check_prose.py gzh/YYYY-MM-DD-<slug>.md
```

脚本只报警不改文。覆盖两类：

- **公众号渲染约束**：公式源码、markdown 嵌入链接、`---` 分隔线、本地图片路径、超过 4 行的段落、超过 40 字的句子、字数区间
- **AI 味与句法**：翻案腔、破折号、提示性冒号、顿号罗列、同构排比、相邻句同款、名词化、序数小标题、拟人喻体、概括词盖数据、段首零主语评论、翻译腔五种，以及黑话、模型路标、抒情词等词表命中

按提示回改，改法见 references/style-guide.md 的「怎么改」：只改命中处，最小改动，数字和事实一个不动。改完重跑，直到「需要修改」清零、「需要人工判断」逐条看过。

### Step 5 自检

脚本查不了的只剩五项人检：**标题、摘要、数字溯源、配图、获得感**。标准逐条见 style-guide「成稿自检」表对应行，任何一项不过就回去改，改完重跑脚本。

### Step 6 落盘与推送

**落盘**：`gzh/YYYY-MM-DD-<slug>.md`，`<slug>` 与解读文章文件名一致。

**配图**分两路：

**A. 论文配图（正文插图）**
- 直接复用解读文章的配图 `readings/assets/<slug>/`，一张不落（规则见 style-guide「结构」「配图」）
- 推送前把每张本地图传 gzh-hub 图床（端点 3.4）换云端 URL，回填进 md，最终 md 里不许留本地路径

**B. 封面图（必须有）**
- 加载 `gzh-handdrawn` skill 生成封面提示词（21:9 封面）
- 提示词拿到后调 `qianliu-img` skill 出图，提示词原样传过去
- 出图档位用 `img-pro`，请求比例 21:9；比例不在支持列表里时千流云内部会处理（如落到 16:9），**以实际返回为准直接用 `data[0].url`，禁止自己 pad、裁切或转传图床**
- 千流云返回的 `data[0].url` 是公网地址，**直接写进 md 当封面图，不用下载入仓，也不用再传 gzh-hub**
- 需要 API Key（`QIANLIU_API_KEY`，形如 `sk-ql-xxxx`）时问用户要，没有就让用户到 https://console.qlcloud.top/keys 创建
- 封面图放在开头段之后，md 里写 `![封面](url)`；同时留作推送时的 `cover_url`

**推送**：
- 推送前调 gzh-hub 3.1 拿本号 `mp_id`；本号固定主题 `theme_id: emerald`（翠序，2026-10-23 选定），不再每次查 3.2，除非用户要求换主题
- news 体裁 `cover_url` 必填，用 B 路出的封面图 URL
- 把标题、摘要、配图数、字数报给确认后再推
- **只推草稿箱**，正式发布由用户在后台操作

## 归档路径

```
gzh/                          # 本号推文成稿
├── YYYY-MM-DD-<slug>.md      # 与 readings/ 解读文章一一对应
```