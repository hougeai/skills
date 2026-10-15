---
name: image-prompter
description: 用 21 套工业级填空模板 + 541 个实测案例，把生图意图转成可直接投喂 gpt-image-2 的生产级 prompt。适用于海报/封面、信息图、知识卡片、UI 截图、商品图、品牌视觉、古风插画等图像生成 prompt 的撰写与优化。当用户要"生成一张图/封面/信息图/prompt"时加载本技能。
---

# GPT-Image-2 提示词风格库

本技能把 gpt-image-2 生图意图转成生产级 prompt。四层数据自包含，无需外部仓库：

| 层 | 文件 | 内容 |
|---|---|---|
| 索引 | `references/style-library.md` | 22 个模板的选型规则（use-when / guidance / pitfalls）+ 分类/风格/场景标签 |
| 全文 | `references/templates.md` | 21 套可直接复制填空的 prompt 模板正文（text 版 + JSON 版 + 避坑指南） |
| 元数据 | `data/style-library.json` | 模板 / 分类 / 风格 / 场景的结构化定义 |
| 实例 | `data/cases.json` | 541 个实测成功案例的完整 prompt（作者为 @freestylefly/awesome-gpt-image-2，MIT） |

## 工作流

1. **识别意图**：判断用户要什么（海报封面 / 信息图 / UI 截图 / 商品图 / 品牌 / 摄影 / 插画 / 角色 / 古风 / 文档出版物）。
2. **选模板**：先读 `references/style-library.md` 的 Selection Rules 和 Template Index，按 分类 → 风格标签 → 场景标签 的顺序匹配，确定 1 个模板（拿不准时给用户 2-3 个方向让 TA 选）。
3. **取模板全文**：到 `references/templates.md` 找对应锚点小节（`#tpl-ui`、`#tpl-infographic`、`#tpl-poster`、`#tpl-product`、`#tpl-brand`、`#tpl-photo`、`#tpl-illustration`、`#tpl-character`、`#tpl-scene`、`#tpl-history`、`#tpl-document`、`#tpl-other`），优先用该模板下的专用模板（如概念字体海报、自然科普海报），JSON 版适合 Agent 结构化调用。
4. **查案例**：按模板条目里的 Example cases 编号，从 `data/cases.json` 提取真实 prompt 做参照：
   ```bash
   python3 -c "import json; d=json.load(open('<skill路径>/data/cases.json')); print(json.dumps([c for c in d['cases'] if c['id'] in (17,2,4)], ensure_ascii=False, indent=1))"
   ```
   也可按分类/风格模糊筛选相近案例。
5. **产出 prompt**：填空模板 + 参照案例，按六段结构输出最终 prompt——主体任务 / 构图版式 / 视觉风格材质 / 文字与标签要求 / 画幅与输出格式 / 约束与负面细节。中文请求输出中文 prompt，英文请求输出英文 prompt。
6. **先给可复制的 prompt**，再附简短约束说明（指定文字必须逐字准确、比例、层级、避免的伪影）。

## 铁律

- 模板里的 `[占位符]` 必须全部替换为具体内容，禁止留空。
- 画面文字（标题/标签）必须逐字写死在 prompt 里，并加"禁止乱码、拼写完全正确"约束。
- 信息图模块 3-5 个、每模块 1-2 句短文案；禁止把大段正文塞进画面。
- 单张成品图时明确 "single poster only"，禁止 moodboard / 过程稿拼贴。
- 各模板自带的"避坑指南"必须遵守。
