# Qianliu — 千流云原子能力 Skills

| skill | 功能 |
| --- | --- |
| qianliu-asr | 语音转文字（录音转写/说话人识别，另有实时 wss 档） |
| qianliu-tts | 语音克隆与合成（音色库/定制音色/声音克隆） |
| qianliu-image | 图像生成/编辑 |
| qianliu-parse | 文档解析（Office/PDF/图片 → Markdown） |
| qianliu-rag | 知识库 RAG（入库/带出处问答/语义检索） |
| qianliu-search | 实时联网检索（web_search / img_search） |
| qianliu-memory | 长期记忆（retain/recall/reflect） |

## 安装

```bash
# 一键装全部 7 个（路径指向 qianliu/ 子目录，不会带出仓库里其它 skill）
npx skills add hougeai/skills/tree/main/qianliu

# 免交互
npx skills add hougeai/skills/tree/main/qianliu --all

# 只装某一个
npx skills add hougeai/skills --skill qianliu-asr
```
