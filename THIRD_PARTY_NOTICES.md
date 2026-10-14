# 源码来源与许可证

| 内容 | 上游 | 固定版本 | 许可证 |
| --- | --- | --- | --- |
| Python 推理示例 | [ollama/ollama-python](https://github.com/ollama/ollama-python) | v0.6.3，提交 `8785556559ec1d045d27a1ba9d9cc7330c3d3cb1` | [MIT](examples/ollama/LICENSE) |
| SFT 入口与参数定义参考 | [huggingface/trl](https://github.com/huggingface/trl) | v0.15.2，提交 `fc2b041b58f6fbe766dceaec819bc5a8f9d209da` | [Apache-2.0](finetuning/LICENSE) |

第三方作者署名和许可证保留在对应源码/目录中，不将第三方训练框架或示例宣称为本仓库原创。文件级来源、原始哈希、整理后哈希和修改列表见 [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)。

本地 Modelfile 只提取历史配置的 FROM / PARAMETER 行；LoRA / QLoRA YAML 是本次整理的新参考配置，不是历史实验参数记录。PEFT、Transformers、PyTorch 等训练依赖及公开模型/数据使用各自许可证，本仓库没有打包分发它们。
