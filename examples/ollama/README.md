# Ollama Python 应用示例

来源：[ollama/ollama-python v0.6.3](https://github.com/ollama/ollama-python/tree/8785556559ec1d045d27a1ba9d9cc7330c3d3cb1/examples)。许可证：[MIT](LICENSE)。基础文本示例的默认模型改为本仓库创建的 `deepseek-local-demo`；`ps.py` 使用可从模型注册表下载的 `deepseek-r1:1.5b`。其他调整详见根目录的来源清单。

运行前完成根 README 的环境安装和 Modelfile 创建。所有命令从仓库根目录执行：

```powershell
.\.venv\Scripts\python.exe .\examples\ollama\chat.py
```

## 基础应用与模型管理

| 文件 | 功能 | 模型 / 前提 |
| --- | --- | --- |
| [chat.py](chat.py) | 非流式对话 | `deepseek-local-demo` |
| [chat-stream.py](chat-stream.py) | 逐段输出响应 | `deepseek-local-demo` |
| [chat-with-history.py](chat-with-history.py) | 在内存中追加会话历史 | `deepseek-local-demo`；使用 Ctrl+C 结束交互 |
| [generate.py](generate.py) | 单次文本生成 | `deepseek-local-demo` |
| [generate-stream.py](generate-stream.py) | 流式文本生成 | `deepseek-local-demo` |
| [async-chat.py](async-chat.py) | 异步对话请求 | `deepseek-local-demo` |
| [async-generate.py](async-generate.py) | 异步文本生成 | `deepseek-local-demo` |
| [list.py](list.py) | 列出已下载模型及量化信息 | 不需要提前运行推理 |
| [show.py](show.py) | 查看模型模板、参数及能力 | 已创建 `deepseek-local-demo` |
| [ps.py](ps.py) | 拉取模型、触发推理、查看运行资源字段 | `deepseek-r1:1.5b`；执行时可能联网下载模型 |
| [create.py](create.py) | 通过客户端 API 创建 `my-assistant` 标签 | 已创建 `deepseek-local-demo`；会修改本地模型列表 |

## 专项能力

| 文件 | 功能 | 上游保留的模型 |
| --- | --- | --- |
| [structured-outputs.py](structured-outputs.py) | JSON Schema + Pydantic 校验 | `llama3.1:8b` |
| [async-structured-outputs.py](async-structured-outputs.py) | 异步结构化输出 | `llama3.1:8b` |
| [tools.py](tools.py) | 函数调用与工具结果回传 | `llama3.1` |
| [async-tools.py](async-tools.py) | 异步工具调用与回传 | `llama3.1` |
| [embed.py](embed.py) | 获取文本嵌入 | `llama3.2` |

专项示例运行前，按脚本里的模型名执行 `ollama pull <模型名>`。8B 等模型需要更多资源；不要为运行基础对话而一次性下载所有模型。结构化输出会校验返回 JSON；模型返回不合规内容时可能抛出校验错误。示例用于说明调用流程，不是稳定性或模型效果保证。

`chat-with-history.py` 将会话历史保存在进程内存中，退出后不持久化。
