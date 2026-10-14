# Local LLM Deployment

Ollama / DeepSeek 本地部署参数配置示例。

## 使用

安装并启动 [Ollama](https://ollama.com/)，在本目录执行：

```powershell
ollama pull deepseek-r1:1.5b
ollama create deepseek-local-demo -f .\Modelfile
ollama run deepseek-local-demo
```

本配置保留 `temperature 0.9`、`num_ctx 4096` 与停止字符串 `用户：`。停止字符串可能截断回答；参数未经过性能对照验证。这是推理配置，不是模型权重微调。本次上传仅完成静态检查，未重新运行模型。

仓库仅包含配置源码和必要说明，不包含个人资料、凭证、聊天记录、数据集、模型权重或第三方安装包。Ollama 与 DeepSeek 属于各自的第三方项目。

## English

Minimal Ollama / DeepSeek deployment configuration. Install and start Ollama, then run the commands above. The stop string may truncate matching output. These are inference parameters, not weight fine-tuning. Only static checks were performed for this upload; model execution was not repeated.
