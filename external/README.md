# External — 外部收藏的 Skill

不纳入本仓库 git 追踪，按需 clone，随时可从上游更新。按本仓库分类组织：`external/<分类>/<skill 名>`。

> 统一用 `--depth 1` 浅克隆（只要最新文件、不要历史，省时省空间）；`git pull` 更新不受影响。

## design

### logo-design

- **仓库**：https://github.com/kaankiziltug/logo-design-skill
- **用途**：Logo 与品牌标识设计全流程：brief → 概念 → SVG 制作 → 测试 → 交付规范；含 1400+ 真实 SVG logo 库与审计脚本
- **体积**：14M（含资源库，所以不进本仓库）

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

## research

### patent-disclosure-skill

- **仓库**：https://github.com/handsomestWei/patent-disclosure-skill
- **用途**：中国专利 skill 包——交底书/申请文件编写、专利解读、专利地图、审查答复等（9 个子技能，MIT）

```bash
git clone --depth 1 https://github.com/handsomestWei/patent-disclosure-skill.git external/research/patent-disclosure-skill
```
