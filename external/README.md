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

### video-shotcraft

- **仓库**：https://github.com/Vincentwei1021/video-shotcraft
- **用途**：程序型产品宣传片 skill——真实页面截图 + 124 张镜头配方卡（150 shots）+ Remotion 代码绘制 + 2.5D 运镜 + BGM 卡点 + 声音设计 → 1920×1080 MP4，可开浏览器工作台二次编辑、导出剪映工程；与 anything2explainer（MG 讲解）、video-talkcraft（口播）同作者三部曲
- **备注**：Apache-2.0（音频各有授权；Remotion 引擎个人/小团队免费，公司可能需付费）
```bash
git clone --depth 1 https://github.com/Vincentwei1021/video-shotcraft.git /tmp/video-shotcraft
cp -r /tmp/video-shotcraft external/creator/video-shotcraft
rm -rf /tmp/video-shotcraft
```

### ian-xiaohei-illustrations

- **仓库**：https://github.com/helloianneo/ian-xiaohei-illustrations
- **用途**：聚焦型中文正文配图 skill——把文章里的判断/流程/状态/隐喻画成 16:9 白底黑线"小黑"手绘解释图（黑色实心小角色参与核心动作，少量红橙蓝中文批注），先出 shot list 再逐张生图，自带风格 DNA、结构类型、prompt 模板与 QA checklist
- **备注**：MIT；只取 `ian-xiaohei-illustrations/` 子目录（14M，含风格校准样图）；本 skill 不生图——产出结构化提示词，调宿主内置 image_gen 逐张生成后按 QA 清单校验；小黑为作者 IP，直接可用，要自有 IP 只换 `references/xiaohei-ip.md`、`style-dna.md` 和 `assets/examples/`；与 ainosleep-stickman-illustrations 同类不同 IP

```bash
git clone --depth 1 https://github.com/helloianneo/ian-xiaohei-illustrations.git /tmp/xiaohei
cp -r /tmp/xiaohei/ian-xiaohei-illustrations external/creator/ian-xiaohei-illustrations
rm -rf /tmp/xiaohei
```

### ainosleep-stickman-illustrations

- **仓库**：https://github.com/ainosleep/ainosleep-stickman-illustrations
- **用途**：聚焦型中文正文配图 skill——把文章里的判断/流程/状态/隐喻变成 16:9 白底黑线火柴人（AINoSleep IP）手绘解释图；先出 shot list 再逐张生图，自带风格 DNA、动作库、结构类型、prompt 模板与 QA checklist（含中文短标注 + 错字兜底规则）；两种用法：只输出shot list + prompt，或直接生成正文配图。
- **备注**：与 image-prompter（通用 gpt-image-2 模板库）互补——本库是单一 IP 专用、对中文渲染做了显式处理；只取 skill 子目录（4.4M，含 assets 参考板与合格样图，供风格校准，必带），根目录 README/examples 为分享文档不入

```bash
git clone --depth 1 https://github.com/ainosleep/ainosleep-stickman-illustrations.git /tmp/stickman
cp -r /tmp/stickman/ainosleep-stickman-illustrations external/creator/ainosleep-stickman-illustrations
rm -rf /tmp/stickman
```

### guizang-material-illustration

- **仓库**：https://github.com/op7418/guizang-material-illustration
- **用途**：中文解释图/图表美化 skill——歸藏材质 3D 风（IKB 蓝、Swiss 构图），把概念/流程/机制画成带中文标签的图内文字解释图；支持图表截图语义抽取重画、冷门概念先查参考再统一风格；调宿主内置生图
- **备注**：与 xiaohei/stickman 同赛道不同风格；配套 guizang-social-card-skill 管外层卡片排版（未收）

```bash
git clone --depth 1 https://github.com/op7418/guizang-material-illustration.git /tmp/guizang-mi
cp -r /tmp/guizang-mi external/creator/guizang-material-illustration
rm -rf /tmp/guizang-mi/.git
```

### human-writing

- **仓库**：https://github.com/KKKKhazix/human-writing
- **用途**：中文"活人感"写作 skill——治 AI 长文空泛：动笔前材料门禁（非虚构需 ≥5 件具体材料，凑不齐就缩短/短答，绝不灌字数）、按体裁分参考（公众号/知乎/小说/口播等）、成稿后 revision 清单 + `check_prose.py` 查翻案句/AI 排比/句长变异/连词密度
- **备注**：MIT；与 `creator/lieflat-less-ai-tone`（去 AI 味，偏事后检测）互补——本库是完整起草工作流（材料→成稿→审稿），lieflat 可留作终检；只取 skill 子目录（140K，含 references 5 篇 + check_prose.py + 蒸馏版 dist），用前手动软链到 `~/.claude/skills/human-writing`

```bash
git clone --depth 1 https://github.com/KKKKhazix/human-writing.git /tmp/human-writing
cp -r /tmp/human-writing/human-writing external/creator/human-writing
rm -rf /tmp/human-writing
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

### ui-skills

- **仓库**：https://github.com/ibelick/ui-skills
- **用途**：UI skill 聚合注册库（406 个第三方 skill 索引）；自带 8 个自包含 skill：baseline-ui（去 AI 味排版清理）、fixing-accessibility / fixing-metadata / fixing-motion-performance（无障碍 / 元数据 / 动效性能体检）、improve-ui（只读审计出实现计划）、create-design-md（从产品反推 DESIGN.md）、component-canvas（组件画布）
- **备注**：MIT；收自带 `skills/` 8 个（120K）；其余 398 个 agent 经 ui-skills-root 走 `npx ui-skills get <名>` 按需自拉

```bash
git clone --depth 1 https://github.com/ibelick/ui-skills.git /tmp/ui-skills
cp -r /tmp/ui-skills/skills external/design/ui-skills
rm -rf /tmp/ui-skills
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

## tools

### geolook

- **仓库**：https://github.com/aigclink/geolook
- **用途**：GEO（生成式引擎优化）全流程自托管平台——给产品网址/材料，做站点六维体检（访问→定向→理解→可引用四层依赖链）、AI 答案跨 17 引擎采样（10 API + 7 手动）、自动推导品牌事实/竞品/问题库、生成带验收标准的工单、产出可部署资产（llms.txt/JSON-LD/定义块/FAQ/大纲）、自动验收闭环并打包客户交付物；国内+海外双市场并行，证据锚定公开实证（602 prompts / 21,143 citations / 187,818 条去重 CN 引用，官网仅占引用 1.37%）
- **备注**：MIT；既是自托管 Web 看板（Python CLI `geo.py ui` → 127.0.0.1:8765，仅 requests/bs4/lxml 三依赖、无数据库无账号、断网可用）也是 Claude Code skill；零 Key 也能跑（自动采样跳过，改人工采样表）；本仓库整仓拷贝（42M，含 `.git` 与 `work/` 运行产物示例）；已修正 SKILL.md 中 3 处作者硬编码路径 `/Users/brucejan/geo` 为相对 `<skill_dir>/`；商业用途无限制；要用时手动软链 `external/tools/geolook` 到 `~/.claude/skills/geo`

```bash
git clone --depth 1 https://github.com/aigclink/geolook.git /tmp/geolook
cp -r /tmp/geolook external/tools/geolook
rm -rf /tmp/geolook
```

### i-have-adhd

- **仓库**：https://github.com/ayghri/i-have-adhd
- **用途**：ADHD 友好的输出风格技能——行动优先、编号分步、每轮重述进度、具体时间估计；用 `/i-have-adhd` 开启，"stop adhd mode" 关闭（MIT）
- **备注**：仓库本体含评测脚本（888K），这里只取 `skills/i-have-adhd/`（SKILL.md + agents/）；原归 productivity，现并入 tools

```bash
git clone --depth 1 https://github.com/ayghri/i-have-adhd.git /tmp/i-have-adhd
cp -r /tmp/i-have-adhd/skills/i-have-adhd external/tools/i-have-adhd
rm -rf /tmp/i-have-adhd
```

### dashi-ppt

- **仓库**：https://github.com/chuspeeism/dashi-ppt-skill
- **用途**：程序型 PPT skill——内置完整 Node.js 生成器（12 套主题 × 1020 版式 × 20 种页面角色），Agent 把需求整理成 JSON 计划调本地生成器，产出浏览器可编辑（改字/换图/滑杆调版式）的 HTML PPT，可导出可编辑 PPTX/PDF；AGPL-3.0（导出引擎 html-deck-to-pptx 为专有组件）
- **备注**：仓库 160M（.git 占 101M），这里只取 `skills/dashi-ppt/`（59M，skill 本体自包含，含内置生成器 project/）；运行需 Node.js 20+，导出 PPTX/PDF 需本机 Chrome/Chromium；10 页实测约 10 万 token；原归 productivity，现并入 tools

```bash
git clone --depth 1 https://github.com/chuspeeism/dashi-ppt-skill.git /tmp/dashi-ppt-skill
cp -r /tmp/dashi-ppt-skill/skills/dashi-ppt external/tools/dashi-ppt
rm -rf /tmp/dashi-ppt-skill
```

### ponytail

- **仓库**：https://github.com/DietrichGebert/ponytail
- **用途**：编码型 agent skill——"懒散资深工程师"：只写必要代码、优先复用已有能力，但验证/安全/错误处理绝不省；带 `/ponytail-review`（审 diff）、`/ponytail-audit`（全仓排优先级）等命令
- **备注**：MIT；收上游 `skills/` 全部 6 个 skill

```bash
git clone --depth 1 https://github.com/DietrichGebert/ponytail.git /tmp/ponytail
cp -r /tmp/ponytail/skills external/tools/ponytail
rm -rf /tmp/ponytail
```

### translate-book

- **仓库**：https://github.com/deusyu/translate-book
- **用途**：整本书翻译 skill——PDF/DOCX/EPUB → Calibre 转 Markdown 分块 → 8 并行子代理各带独立上下文翻译 → SHA-256 清单校验 → Pandoc/Calibre 出 HTML/DOCX/EPUB/PDF；含术语表跨块一致、邻块指代上下文、断点续跑、术语变更只重译受影响块
- **备注**：MIT；整仓即 skill（896K，tests 样书 11M 未收）；用时要装 Calibre + Pandoc + `pip install pypandoc`；不吃独立 API key，翻译走宿主 agent 自身额度

```bash
git clone --depth 1 https://github.com/deusyu/translate-book.git /tmp/translate-book
cp -r /tmp/translate-book external/tools/translate-book
rm -rf /tmp/translate-book/.git /tmp/translate-book/tests
```

### council

- **仓库**：https://github.com/0xNyk/council-of-high-intelligence
- **用途**：多人审议决策 skill——18 个思想家人设对问题多轮辩论出裁决（盲评→匿名质询→加权计票）
- **备注**：MIT；跨宿主（Codex/Gemini/OpenCode 各有 SKILL 变体）；收 SKILL + agents/（18 议员，即原生 subagent 定义）+ scripts/ + configs/（432K）；装法：`agents/*.md` 拷 `~/.claude/agents/`、目录软链 `~/.claude/skills/council`，然后 `/council --triad <域> 问题`

```bash
git clone --depth 1 https://github.com/0xNyk/council-of-high-intelligence.git /tmp/council
cp -r /tmp/council external/tools/council
rm -rf /tmp/council/.git /tmp/council/assets
```

### ai-website-cloner-template

- **仓库**：https://github.com/JCodesMore/ai-website-cloner-template
- **用途**：网站临摹模板——让 agent 开浏览器观察源站（双端全状态、实测样式、下载真素材）后手写 React 组件临摹，同视口对比修差，产出可维护 Next.js 代码
- **备注**：MIT；通用 skill 在 `.agents/skills/clone-website/`（Codex/Cursor/OpenCode 直接读；Claude Code 对话里点名引用该 SKILL.md 即可），整仓即用无需安装；Node 24+，先 `npm install && npm run check`；复刻质量取决于模型（推荐 Opus）

```bash
git clone --depth 1 https://github.com/JCodesMore/ai-website-cloner-template.git /tmp/awct
cp -r /tmp/awct external/tools/ai-website-cloner-template
rm -rf /tmp/awct/.git
```


