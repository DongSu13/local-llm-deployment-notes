# 本地部署与环境检查

## 原生安装

从 [Ollama](https://ollama.com/) 安装对应平台版本并启动服务。

```powershell
ollama --version
ollama list
Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags'
```

服务可达后再执行模型下载和根目录的 Modelfile 创建命令。Python 客户端安装不会自动启动 Ollama。

## Docker 方式

Ollama 官方支持通过容器运行服务，参考 [官方 Docker 文档](https://docs.ollama.com/docker)。下面的 CPU 路径把端口限定在本机：

```powershell
docker run -d --name ollama -v ollama:/root/.ollama -p 127.0.0.1:11434:11434 ollama/ollama
docker exec ollama ollama pull deepseek-r1:1.5b
```

容器里的模型管理与原生 Windows 安装分别存储。使用容器时，可通过本机端口调用 Python SDK；创建自定义标签还需要将 Modelfile 提供给容器内 CLI，或使用 SDK 的创建接口。上面的容器命令并未自动创建 `deepseek-local-demo`。

GPU 路径取决于宿主机和驱动条件，按官方文档配置，不将某个 GPU 环境假定为所有机器均可使用。本次没有运行该容器命令，也没有实测 GPU、内存占用或生成速度。

## 模型和参数

本地 Modelfile 保留早期取值：temperature 0.9、num_ctx 4096、stop `用户：`。它们不是调优实验结论。停止字符串出现在输出中时可能截断回答；参数设置不会训练模型权重。

模型体积、量化和上下文影响资源需求。运行 1.5B 的基础示例与运行工具调用的 8B 示例是不同资源条件，不应混用评测结论。

## 常见故障

| 情况 | 检查 |
| --- | --- |
| 连接被拒绝 | 服务是否启动；是否使用正确端口 |
| 模型不存在 | `ollama list` 中是否有脚本指定的完整标签 |
| 未创建 demo 标签 | 先执行根 README 的 `ollama create` 命令 |
| 回答中途停止 | 是否命中了 Modelfile 的 stop 字符串 |
| 结构化输出校验失败 | 所选模型是否支持此用法；返回内容是否满足 Schema |
| 工具调用没有返回 | 所选模型的能力和返回消息；不能假定每个模型都会调用工具 |
