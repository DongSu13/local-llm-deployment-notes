# Local LLM Deployment & Fine-Tuning

[中文](README.md) | [English](README.en.md)

围绕 DeepSeek 的本地部署、Python 推理与参数高效微调，整理 Ollama 配置、16 个推理示例，以及 Hugging Face TRL / PEFT 的 SFT、LoRA 和 QLoRA 参考流程。

## 项目背景与来源

从早期本地 Ollama 配置出发，把模型创建、应用调用、训练配置和产物验证整理成可阅读的源码目录。历史材料保留在 [Modelfile](Modelfile)；新增推理示例和训练入口来自固定版本的上游项目，逐项保留来源和许可证。

文档组织参考 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)、[QLoRA](https://github.com/artidoro/qlora)、[PEFT](https://github.com/huggingface/peft) 的功能、环境、快速开始、数据和评估结构，也沿用已有项目对来源与验证范围的说明方式。

## 功能与方法

| 流程 | 模型 / 方法 | 入口 | 输出 |
| --- | --- | --- | --- |
| 本地模型创建 | Ollama `deepseek-r1:1.5b` + 推理参数 | [Modelfile](Modelfile) | 本机 `deepseek-local-demo` 标签 |
| 文本推理 | 对话、流式、历史、异步 | [Python 示例](examples/ollama/README.md) | 终端响应 |
| 专项 API | 结构化输出、工具调用、嵌入、模型管理 | [能力与模型对应表](examples/ollama/README.md) | JSON、工具结果、向量或模型信息 |
| LoRA SFT | DeepSeek-R1-Distill-Qwen-1.5B，未量化基础模型 | [lora.yaml](finetuning/configs/lora.yaml) | 本地适配器目录 |
| QLoRA SFT | 同一基础模型，4-bit NF4 + 双重量化 | [qlora.yaml](finetuning/configs/qlora.yaml) | 本地适配器目录 |

工具和结构化输出示例保留上游的 Llama 模型；具体标签和下载前提见示例目录。Ollama 的推理模型文件与 Transformers 的训练模型格式不同。

## 代码结构

```text
.
├── Modelfile                 # 历史本地推理参数
├── requirements.txt          # Ollama Python SDK
├── examples/ollama/          # 16 个 API 示例与 MIT 许可证
├── finetuning/
│   ├── sft.py               # TRL SFT 训练入口
│   ├── configs/             # LoRA / QLoRA 配置
│   ├── reference/           # 上游参数定义，供阅读
│   └── requirements*.txt    # 训练环境依赖
├── docs/                    # 部署、客户端、实验和验证指南
├── THIRD_PARTY_NOTICES.md    # 来源、版本、许可证
└── SOURCE_MANIFEST.json      # 第三方文件哈希和修改记录
```

## 环境要求

| 用途 | 软件与硬件前提 |
| --- | --- |
| Ollama 推理 | Python 3.12、Ollama 服务端、所选模型；CPU / GPU 资源取决于模型和上下文 |
| LoRA 训练 | 独立 Python 3.12 环境、兼容 NVIDIA GPU 与 CUDA PyTorch；默认 FP16 |
| QLoRA 训练 | 上述训练环境及 bitsandbytes；优先使用受支持的 Linux / WSL2 CUDA 环境 |

推理 SDK 固定为 `ollama==0.6.3`；训练固定为 PyTorch 2.6.0、Transformers 4.49.0、TRL 0.15.2、PEFT 0.14.0。详细依赖和 GPU 安装前提见 [微调指南](finetuning/README.md)。显存需求需在实际环境测量。

## 快速开始：本地推理

安装并启动 [Ollama](https://ollama.com/)，从仓库根目录执行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull deepseek-r1:1.5b
ollama create deepseek-local-demo -f .\Modelfile
.\.venv\Scripts\python.exe .\examples\ollama\chat.py
.\.venv\Scripts\python.exe .\examples\ollama\chat-stream.py
```

Python SDK 不包含服务端或模型权重。后续可按 [部署指南](docs/local-deployment.md) 检查服务、选择 Docker 方式和排查故障；按 [客户端接入](docs/client-integration.md) 连接本地服务。

## 快速开始：本地微调

基础模型使用 Transformers 格式的 [DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)，数据使用公开的 [trl-lib/Capybara](https://huggingface.co/datasets/trl-lib/Capybara)。执行训练会下载这些资源。

LoRA：创建独立环境后，先按 [PyTorch 安装说明](https://pytorch.org/get-started/locally/) 在该环境安装兼容的 CUDA 构建，再安装其余依赖和启动训练：

```powershell
py -3.12 -m venv .venv-training
# 先在 .venv-training 中安装兼容的 CUDA PyTorch
.\.venv-training\Scripts\python.exe -m pip install -r finetuning\requirements.txt
.\.venv-training\Scripts\python.exe finetuning\sft.py --config finetuning\configs\lora.yaml
```

QLoRA：在兼容的 Linux / WSL2 CUDA 环境中：

```bash
python3.12 -m venv .venv-training
# 先在 .venv-training 中安装兼容的 CUDA PyTorch
.venv-training/bin/python -m pip install -r finetuning/requirements-qlora.txt
.venv-training/bin/python finetuning/sft.py --config finetuning/configs/qlora.yaml
```

两个配置均为 **10 步启动检查**：序列长度 512、batch size 1、梯度累积 4、LoRA rank 8。默认关闭评估、Hub 上传和外部日志报告，产物保存到 `outputs/lora_smoke` 或 `outputs/qlora_smoke`。完整数据准备、参数含义与后续验证见 [微调指南](finetuning/README.md) 和 [实验流程](docs/experiment-workflow.md)。

## 验证与结果范围

16 个推理示例已通过合成 HTTP 响应的离线执行检查；两份微调配置已通过字段与模拟训练流程检查。详细方法见 [验证记录](docs/verification.md)。

尚未进行真实模型推理、GPU 训练、适配器导入或质量评估。配置中的模型和数据 revision 也未形成完全固定的实验快照。

## 来源与许可

本仓库自行编写的源码、配置和文档默认采用 [Apache-2.0](LICENSE)。第三方内容沿用各自许可证：

- Ollama Python 示例：v0.6.3，[MIT](examples/ollama/LICENSE)。
- TRL SFT 入口和参数定义：v0.15.2，[Apache-2.0](finetuning/LICENSE)。
- 本地配置及本次编写的使用文档与第三方代码分开注明；具体修改见 [来源说明](THIRD_PARTY_NOTICES.md) 与 [文件清单](SOURCE_MANIFEST.json)。
