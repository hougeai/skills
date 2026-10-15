---
name: qianliu-asr
description: 千流云语音转文字（录音转写 / 说话人识别）。当用户要求把音频、会议录音、访谈、课程视频音轨转成文字文稿，或需要区分「谁在什么时候说话」（角色标注 + 时间戳）时使用本技能。三个计费档位：asr-flash（极速）、asr-pro（精度）、asr-diarize（说话人识别），另有实时转写两档（wss）。
---

# 千流云语音转文字 Skill

OpenAI Audio 兼容 API，**同步返回**（一次请求直接拿到转写文稿，无需任务轮询）。

## 鉴权

```
Authorization: Bearer sk-ql-xxxxxxxx
```

如果用户没有提供 Key，引导其到 `https://console.qlcloud.top/keys` 创建。
不要把用户的 Key 写进任何会被提交/分享的文件或日志中。

## 端点

Base URL：`https://api.qlcloud.top/gateway/asr/v1`

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| POST | `/audio/transcriptions` | 音频转写（multipart：`file` 音频二进制 + `model` 档位 id） |
| WSS | `/audio/realtime?model=asr-realtime-flash` | 实时流式转写（Authorization 头鉴权；档位见下） |

限制：单个音频 **≤ 50MB、≤ 1 小时**。长音频耗时与时长正相关，**务必设置 600s 超时**。

标准档位响应：

```json
{ "duration": 13.73, "text": "转写文稿全文……", "usage": { "type": "duration", "seconds": 14 } }
```

## 模型档位（model 参数）

| model | 适用 |
| --- | --- |
| `asr-flash` | 极速档：秒级出稿，标点完整，日常纪要首选 |
| `asr-pro` | 匠心档：标点、断句、专名更准确，正式文稿与长音频选它 |
| `asr-diarize` | 说话人识别：区分「谁在什么时候说话」，响应额外返回 segments |
| `asr-realtime-flash` | 实时轻量档（wss）：中英日韩粤多语言，跨语言会议即时转写 |
| `asr-realtime-pro` | 实时精准档（wss）：真流式文字只增不改、字幕稳定不闪，中英高准确率 |

计费：**按秒（单价 × `usage.seconds`），成功才计费，失败不扣；单价以「接入指南」页目录为准**。默认建议：日常用 asr-flash；正式文稿/长音频用 asr-pro；需要角色区分用 asr-diarize。

## 音频转写（asr-flash / asr-pro）

```bash
curl https://api.qlcloud.top/gateway/asr/v1/audio/transcriptions \
  -H "Authorization: Bearer sk-ql-xxxxxxxx" \
  -F "file=@会议录音.mp3" \
  -F "model=asr-pro" \
  --max-time 600
```

## 说话人识别（asr-diarize）

同一端点，`model=asr-diarize`。响应额外带 `segments` 明细；`text` 为带时间戳的拼接文稿：

```json
{
  "duration": 1693.85,
  "segments": [
    { "start": 0.0, "end": 8.92, "speaker": "SPEAKER_00", "text": "……" }
  ],
  "text": "SPEAKER_00 [00:00:00.000 -> 00:00:08.920]\n……\n\nSPEAKER_01 [00:00:08.920 -> 00:00:13.680]\n……",
  "usage": { "type": "duration", "seconds": 1694 }
}
```

## 实时流式转写（asr-realtime-flash / asr-realtime-pro）

WSS `/audio/realtime`，面向**客户端程序的实时字幕场景**（边说边出字）。协议为 OpenAI Realtime，握手带 `Authorization: Bearer sk-ql-xxxxxxxx`；计费按秒 × 会话时长，单次最长 120 分钟。

> **Agent 批量转写请勿使用本端点**——音频文件转写一律用上方同步接口。
> 需要开发实时转写客户端时，协议细节（上下行消息、两档差异、热词定制）与示例代码见接入指南：https://asr.qlcloud.top/docs

## 错误处理

错误形态：`{"error": {"message": "...", "code": <http_status>}}`

| code | 含义 | 处理 |
| --- | --- | --- |
| 400 | 参数错误（缺少文件、文件为空、超过 50MB） | 核对 multipart 字段；压缩或切分音频 |
| 401 | API Key 无效或已吊销 | 让用户到控制台检查 Key |
| 402 | 余额不足 | 提醒用户充值，不要重试 |
| 404 | model 不存在 | 只用上方档位表中的 model_id |
| 429 | 触发限流（Key 每分钟额度） | 等待 30–60s 后重试，勿并发猛打 |
| 502 | 上游转写服务异常 | 稍后重试 1–2 次，持续失败则放弃并告知用户 |

成功判别：**HTTP 200 即成功**（响应无 status 字段）。
