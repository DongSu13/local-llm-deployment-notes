# 客户端与接口连接

| 接入方式 | 本机地址 | 模型名 |
| --- | --- | --- |
| Chatbox 等客户端的 Ollama 提供方 | `http://127.0.0.1:11434` | `ollama list` 中的完整标签 |
| OpenAI 兼容客户端 | `http://127.0.0.1:11434/v1` | 同上 |
| 本仓库 Python 示例 | SDK 默认的本地 Ollama 地址 | 按脚本指定模型 |

OpenAI 兼容接入说明：[Ollama 官方文档](https://docs.ollama.com/openai)。客户端可能要求填写非空 API Key，占位值不构成身份认证；本地默认 Ollama 服务不需要真实云端 API Key。使用前检查客户端是否自动拼接 `/v1`，避免重复路径。

本仓库仅链接 [Chatbox](https://github.com/ChatboxAI/chatbox)，没有复制客户端源码、设置或聊天记录，也没有完成本次实际客户端验收。

