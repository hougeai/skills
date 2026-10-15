# External — 外部收藏的 Skill

不纳入本仓库 git 追踪，按需 clone，随时可从上游更新。按本仓库分类组织：`external/<分类>/<skill 名>`。

> 放置标准：**来源是外部仓库 → external；自己写的 → 对应分类目录。** 只看来源，不看体积。

> 统一用 `--depth 1` 浅克隆（只要最新文件、不要历史，省时省空间）；`git pull` 更新不受影响。

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
