# Skills

## 目录结构

```
skills/
├── creator/                   # 自媒体/内容创作（公众号/图文/短视频）
│   ├── gzh-hub/               # 公众号创作工作台：检索/导入/排版推送草稿箱
│   ├── image-prompter/        # 生图提示词库：21 套模板 + 541 实测案例
│   └── lieflat-less-ai-tone/  # 去 AI 味：结构/翻译腔/人机对比检测脚本
├── external/                  # 外部收藏（git 不追踪）：按 external/README.md 清单按需 clone
├── qianliu/                   # 千流云原子能力 skills ×7（见 qianliu/README.md）
├── research/                  # 研究类（论文/专利/技术报告）
│   ├── deepxiv/               # arXiv/PMC 论文搜索与阅读
│   ├── semantic-scholar/      # 学术搜索/引用关系，全学科 2 亿+论文（.env: SS_API_KEY）
│   └── top-conference-digest/ # 顶会论文摘要：PapersWithCode 抓取 + LLM 分析
├── README.md                  # 目录索引：一句话说明 + 安装方式（人看的入口）
└── .gitignore                 # **/.env —— 各 skill 的密钥不进仓库
```

## 安装

```bash
# 安装仓库全部 skills（交互式选择 agent）
npx skills add hougeai/skills

# 只装某一个（skill 名 = 目录名）
npx skills add hougeai/skills --skill gzh-hub
npx skills add hougeai/skills --skill gzh-hub -g   # -g 全局（~/.agents/skills/，各 agent 目录自动建符号链接）

# 只装某个系列全套（示例：千流云 7 个，多个 --skill 参数指定）
npx skills add hougeai/skills --skill qianliu-asr --skill qianliu-tts --skill qianliu-image --skill qianliu-parse --skill qianliu-rag --skill qianliu-search --skill qianliu-memory
```

## 更新

```bash
npx skills update               # 更新全部
npx skills update gzh-hub       # 只更新指定 skill
```