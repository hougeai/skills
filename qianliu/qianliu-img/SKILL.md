---
name: qianliu-image
description: 千流云图像生成（文生图 / 图像编辑）。当用户要求生成图片、海报、人像、电商图，或编辑照片（换背景、抠图、转证件照、风格转换、高清放大、多图合成）时使用本技能。两个计费档位：img-flash（极速）与 img-pro（匠心画质）。
---

# 千流云图像生成 Skill

OpenAI Images 兼容 API，**同步返回**（一次请求直接拿到图片永久 URL，无需任务轮询）。

## 鉴权

```
Authorization: Bearer sk-ql-xxxxxxxx
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 端点

Base URL：`https://api.qlcloud.top/gateway/img/v1`

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| POST | `/images/generations` | 文生图（t2i） |
| POST | `/images/edits` | 图像编辑（i2i：改背景/抠图/证件照/风格化/多图合成） |

响应（两个端点同构）：

```json
{ "created": 1789000000, "data": [{ "url": "https://pub-xxx.r2.dev/img/xxxx-0.png", "seed": 0 }] }
```

`data[0].url` 为**永久地址**（已转存对象存储），可直接下载/Markdown 引用。每次调用固定返回 1 张。

## 模型档位（model 参数）

| model | 适用 |
| --- | --- |
| `img-flash` | 极速档：快速出图，2K 高清，支持比例：1:1、3:4、4:3、16:9、9:16、2:3、3:2、21:9 |
| `img-pro` | 匠心档：顶级画质、中文文字渲染、精准编辑，支持比例：2:3、3:4、3:2、4:3、1:1、9:16、16:9 |

两个档位**都同时支持**文生图与图像编辑，**按次计费，单价以「接入指南」页目录为准**。默认建议：日常用 img-flash，用户强调画质/文字渲染/编辑精度时用 img-pro。

## 文生图

```bash
curl https://api.qlcloud.top/gateway/img/v1/images/generations \
  -H "Authorization: Bearer sk-ql-xxxxxxxx" \
  -H "Content-Type: application/json" \
  --max-time 300 \
  -d '{
    "model": "img-pro",
    "prompt": "一只在陶土色背景前的橘猫，极简插画风格",
    "ratio": "1:1"
  }'
```

- `ratio`（语义比例）与 `size`（显式尺寸，如 `2048x2048`）二选一；都传时 size 优先；都不传由模型默认。
- 生成耗时通常 10–120s，**务必设置 300s 以上超时**。

## 图像编辑

参考图支持两种形态（可混用，最多 3 张：`image` 主图 + `image2`/`image3`）：

1. **公网 URL**：`"image": "https://example.com/cat.png"`
2. **base64 data URL**：本地文件先编码（单张 ≤ 4MB）：

```bash
B64=$(base64 -w0 cat.png)  # macOS 用 base64 -i cat.png
curl https://api.qlcloud.top/gateway/img/v1/images/edits \
  -H "Authorization: Bearer sk-ql-xxxxxxxx" \
  -H "Content-Type: application/json" \
  --max-time 300 \
  -d "{
    \"model\": \"img-pro\",
    \"prompt\": \"把背景改成海滩日落，保持主体完全不变\",
    \"image\": \"data:image/png;base64,${B64}\"
  }"
```

## 预设指令（高频编辑场景，直接用作 prompt 或按需改写）

- **一键抠图**：将画面主体完整抠出，彻底移除背景，背景替换为纯白色，保持主体轮廓、颜色、材质和细节完全不变，边缘干净无残留，不要在主体上添加或丢失任何元素
- **高清放大**：以超高清画质重新绘制这张图片，保持构图、主体、颜色、光影和风格完全不变，全面提升分辨率、锐度和细节质感，修复模糊、噪点、压缩伪影和锯齿，边缘清晰干净，纹理细腻自然，不添加、不删除、不改变任何元素
- **电商场景图**：保持商品主体的形状、颜色、材质、文字和细节完全不变，将背景替换为简约高级的电商摄影棚场景：柔和的纯色渐变背景搭配自然光影和轻微倒影，专业商业摄影质感，突出商品主体
- **照片转插画**：将这张照片转换为精美的日系动漫插画风格，保持人物五官特征、姿势、构图和场景布局完全一致，色彩清新明亮，线条干净，细节丰富，像新海诚动画电影的画面质感
- **转证件照**：将这张人像照片转换为标准证件照：保持人物五官、脸型和发型特征完全不变，调整为正面朝向镜头、表情自然端庄，肩部以上居中构图，背景替换为纯白色，光线均匀柔和无阴影，专业证件照质感，不添加、不删除、不改变任何面部特征

## 错误处理

错误形态：`{"error": {"message": "...", "code": <http_status>}}`

| code | 含义 | 处理 |
| --- | --- | --- |
| 400 | 参数错误（prompt 为空、尺寸不支持、模型不支持该模式） | 按本文档核对参数 |
| 401 | API Key 无效或已吊销 | 让用户到控制台检查 Key |
| 402 | 余额不足 | 提醒用户充值，不要重试 |
| 404 | model 不存在 | 只用 `img-flash` / `img-pro` |
| 429 | 触发限流（Key 每分钟额度）或生成排队已满 | 等待 30–60s 后重试，勿并发猛打 |
| 502 | 上游图像服务异常 | 稍后重试 1–2 次，持续失败则放弃并告知用户 |

注意：高峰期请求可能在服务端排队（并发闸门），表现为等待变长——属正常现象，保持单次请求等待即可，**不要**用并发重试来「加速」。
