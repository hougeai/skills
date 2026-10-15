---
name: qianliu-tts
description: 千流云语音克隆与合成（文字转语音）。当用户要求把文字读出来、生成配音、合成语音/旁白，用指定风格音色（温柔女声、阳光男声、方言等）说话，或克隆自己/他人的声音说话，或需要边生成边播放的流式合成时使用本技能。三个计费档位：tts-flash（丰富音色库）、tts-design（自然语言定制音色）、tts-clone（声音克隆）。
---

# 千流云语音合成接入指南

Base URL：`https://api.qlcloud.top/gateway/tts/v1`（OpenAI Audio 兼容形态）

## 鉴权

```
Authorization: Bearer sk-ql-***
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 音色列表 `GET /voices`

返回按档位分组的可用音色（统一响应协议 `{code, msg, data}`，`data` = `[{model, name, voices: [{id, name, desc}]}]`）——**合成的 `voice` 字段取这里的 id**；可选 query `?model=tts-flash` 过滤单档。

```bash
curl https://api.qlcloud.top/gateway/tts/v1/voices -H "Authorization: Bearer sk-ql-***"
```

## 语音合成 `POST /audio/speech`

JSON 请求体：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `model` | 是 | 档位 id：`tts-flash` / `tts-design` |
| `input` | 是 | 合成文本，≤ 2000 字符 |
| `voice` | 档相关 | `tts-flash` 传音色 id（见下表）；`tts-design` 免传（描述写在文本前缀） |

响应：完整音频二进制，同步返回——格式随档位：`tts-flash` 为 `audio/mpeg`（MP3），`tts-design` 为 `audio/wav`（48kHz）。按字符计费（单价 × 字符数 / 1000）。

## 档位与音色

| 档位 | 音色 |
| --- | --- |
| `tts-flash` | `zh-xiaoxia`（小夏·温柔女声）/ `zh-xiaoyang`（小阳·阳光男声）/ `zh-yunyang`（闻铮·新闻男声）/ `zh-tiandou`（甜豆·活泼少女）/ `zh-yuefeng`（岳峰·沉稳男声）/ `zh-tiezi`（铁子·东北话）/ `zh-qinniu`（秦妞·陕西话）/ `en-annie`（安妮·美式英语女声）/ `en-gavin`（盖文·美式英语男声） |
| `tts-design` | 无固定音色——文本前缀写描述：`(温柔的女声，语速平缓)正文…` |
| `tts-clone` | 我的克隆声音（voice_id，见「声音克隆」节；**流式合成目前仅支持本档**） |

计费：**按千字符**（克隆建档按个，重复样本幂等不计费），失败不计费；**单价以「接入指南」页目录为准**。

**方言要点**：方言音色的合成文本直接写方言词句效果更佳（粤语写「伙計，唔該…」而非「伙计，麻烦…」）。

## 声音克隆（tts-clone 配套）

```bash
# ① 克隆创建（multipart；text=样本转写必填；consent=true 授权声明必填）→ voice_id
curl -X POST https://api.qlcloud.top/gateway/tts/v1/audio/voices \
  -H "Authorization: Bearer sk-ql-***" \
  -F "file=@样本.wav" -F "text=样本里说的内容" -F "name=我的声音" -F "consent=true"
# ② 我的声音列表 / 删除
curl https://api.qlcloud.top/gateway/tts/v1/audio/voices -H "Authorization: Bearer sk-ql-***"
curl -X DELETE https://api.qlcloud.top/gateway/tts/v1/audio/voices/{voice_id} -H "Authorization: Bearer sk-ql-***"
# ③ 用 voice_id 合成（同 POST /audio/speech，model=tts-clone, voice=voice_id）
```

样本要求：wav 格式、3-10 秒清晰人声、≤ 10MB；克隆声音 30 天未使用自动清理（每次合成成功自动续期）。

## 流式合成 `WSS /audio/realtime`（句级流式，边生成边播放；v1 仅 tts-clone 克隆声音）

面向**对话/朗读客户端的实时播报场景**：LLM 出一句发一句、收帧即播，支持对话打断（barge-in）。计费按会话聚合（成功句字符累计，连接结束统一结算；失败/取消句不计费）。

> **Agent 生成音频文件请勿使用本端点**——文字转语音一律用上方同步接口 `POST /audio/speech`。
> 需要开发流式合成客户端时，事件协议（`input.text` / `input.cancel` / 音频帧格式）与示例代码见接入指南：https://tts.qlcloud.top/docs

## 调用示例

```bash
curl https://api.qlcloud.top/gateway/tts/v1/audio/speech \
  -H "Authorization: Bearer sk-ql-***" \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-flash", "input": "你好，欢迎使用千流云语音合成", "voice": "zh-xiaoxia"}' \
  -o speech.wav
```

```python
import httpx

resp = httpx.post(
    "https://api.qlcloud.top/gateway/tts/v1/audio/speech",
    headers={"Authorization": "Bearer sk-ql-***"},
    json={"model": "tts-design", "input": "(温柔的女声，语速平缓)今晚的月色真美。"},
    timeout=180,
)
with open("speech.wav", "wb") as f:
    f.write(resp.content)
```

## 错误码

| 状态码 | 含义 | 处理 |
| --- | --- | --- |
| 400 | 参数错误（文本为空/超 2000 字/音色 id 不存在） | 核对字段；音色 id 取上表 |
| 401 | API Key 无效或已吊销 | 控制台检查 Key 状态 |
| 402 | 余额不足 | 控制台钱包充值 |
| 404 | 模型不存在或未上架 | 取上表 model_id |
| 429 | 限流（按 Key 每分钟额度） | 降低并发 |
| 502 | 上游合成服务异常 | 稍后重试 |
