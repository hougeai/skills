# External — 外部收藏的 Skill

不纳入本仓库 git 追踪，按需 clone，随时可从上游更新。按本仓库分类组织：`external/<分类>/<skill 名>`。

> 放置标准：**来源是外部仓库 → external；自己写的 → 对应分类目录。** 只看来源，不看体积。

> 统一用 `--depth 1` 浅克隆（只要最新文件、不要历史，省时省空间）；`git pull` 更新不受影响。

## creator

### anything2explainer

- **仓库**：https://github.com/Vincentwei1021/anything2explainer
- **用途**：程序型视频 skill——给主题或文章，产出 1280×720 黑底 MG 风格讲解视频（Remotion 代码绘制，带 TTS 配音/字幕/章节进度条，中英文均可）；流程含调研 → 解说词 → 分镜 → 多 agent 并行构建镜头 → 量化 QC，附 9 阶段规范、动效词表与一条完整样片（examples/rag）作质量标尺
- **备注**：每片预留 ≥5GB 磁盘、耗时 1–3 小时（agent 并行构建）；运行需 Node 18+ / ffmpeg / Python venv（edge-tts 等），脚本为 macOS zsh 开发、Linux 应可用；视觉风格固定（幕底点阵波/星点二选一）。
```bash
git clone --depth 1 https://github.com/Vincentwei1021/anything2explainer.git /tmp/anything2explainer
cp -r /tmp/anything2explainer external/creator/anything2explainer
rm -rf /tmp/anything2explainer
```

### video-talkcraft

- **仓库**：https://github.com/Vincentwei1021/video-talkcraft
- **用途**：程序型口播视频 skill——给口播稿 + 成品配音，本机做字级时间戳对齐、写 SHOTBOOK 分镜、用 Remotion 渲出带动效的解说成片（动态字卡 / 证据截图 / 运镜 / 素排字幕 / 影视级音效，全部锁在人声上）；108 张参数化动效配方卡、七层反 PPT 镜头系统、三重验收（机器闸 + 独立审片）
- **备注**：PolyForm Noncommercial——非商业免费，商业使用需作者授权（同 anything2explainer 作者）；与 anything2explainer 互补：后者是无主播 MG 讲解，本库是口播/人物出镜类横屏视频；运行需 Node 18+ / ffmpeg / Python 3.10+（默认 FireRedASR 时间戳模型 767MB 首次运行自动下载，不在仓库内；不想下本地模型，可用云端 ASR做字级时间戳对齐与配音，免本地模型依赖）；

```bash
git clone --depth 1 https://github.com/Vincentwei1021/video-talkcraft.git /tmp/video-talkcraft
cp -r /tmp/video-talkcraft external/creator/video-talkcraft
rm -rf /tmp/video-talkcraft
```

## design

### logo-design

- **仓库**：https://github.com/kaankiziltug/logo-design-skill
- **用途**：Logo 与品牌标识设计全流程：brief → 概念 → SVG 制作 → 测试 → 交付规范；含 1400+ 真实 SVG logo 库与审计脚本

```bash
git clone --depth 1 https://github.com/kaankiziltug/logo-design-skill.git
cp -r logo-design-skill/skills/logo-design external/design/logo-design
rm -rf logo-design-skill
```

### awesome-design-md

- **仓库**：https://github.com/VoltAgent/awesome-design-md
- **用途**：84 个真实网站的 DESIGN.md 设计系统文档合集（Google Stitch 格式：色彩/字体/组件/布局/Do&Don't），拷进项目根目录让 Agent 生成视觉一致的 UI；MIT

```bash
git clone --depth 1 https://github.com/VoltAgent/awesome-design-md.git external/design/awesome-design-md
```

## productivity

### i-have-adhd

- **仓库**：https://github.com/ayghri/i-have-adhd
- **用途**：ADHD 友好的输出风格技能——行动优先、编号分步、每轮重述进度、具体时间估计；用 `/i-have-adhd` 开启，"stop adhd mode" 关闭（MIT）
- **备注**：仓库本体含评测脚本（888K），这里只取 `skills/i-have-adhd/`（SKILL.md + agents/）

```bash
git clone --depth 1 https://github.com/ayghri/i-have-adhd.git /tmp/i-have-adhd
cp -r /tmp/i-have-adhd/skills/i-have-adhd external/productivity/i-have-adhd
rm -rf /tmp/i-have-adhd
```

### dashi-ppt

- **仓库**：https://github.com/chuspeeism/dashi-ppt-skill
- **用途**：程序型 PPT skill——内置完整 Node.js 生成器（12 套主题 × 1020 版式 × 20 种页面角色），Agent 把需求整理成 JSON 计划调本地生成器，产出浏览器可编辑（改字/换图/滑杆调版式）的 HTML PPT，可导出可编辑 PPTX/PDF；AGPL-3.0（导出引擎 html-deck-to-pptx 为专有组件）
- **备注**：仓库 160M（.git 占 101M），这里只取 `skills/dashi-ppt/`（59M，skill 本体自包含，含内置生成器 project/）；运行需 Node.js 20+，导出 PPTX/PDF 需本机 Chrome/Chromium；10 页实测约 10 万 token

```bash
git clone --depth 1 https://github.com/chuspeeism/dashi-ppt-skill.git /tmp/dashi-ppt-skill
cp -r /tmp/dashi-ppt-skill/skills/dashi-ppt external/productivity/dashi-ppt
rm -rf /tmp/dashi-ppt-skill
```

## research

### figures4papers

- **仓库**：https://github.com/ChenLiu-1996/figures4papers
- **用途**：出版级 matplotlib 科研绘图 skill（scientific-figure-making）——柱状对比/成分分解/雷达/趋势/热力图/多面板的统一规范，含 API 封装（apply_publication_style、调色板、PDF/SVG 导出）与 8 个 Nature/ICML/NeurIPS 级真实成图项目作 few-shot

```bash
git clone --depth 1 https://github.com/ChenLiu-1996/figures4papers.git external/research/figures4papers
```

### patent-disclosure-skill

- **仓库**：https://github.com/handsomestWei/patent-disclosure-skill
- **用途**：中国专利 skill 包——交底书/申请文件编写、专利解读、专利地图、审查答复等（9 个子技能，MIT）

```bash
git clone --depth 1 https://github.com/handsomestWei/patent-disclosure-skill.git external/research/patent-disclosure-skill
```
