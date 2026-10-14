# 本地 SFT / LoRA / QLoRA

训练入口来自 [Hugging Face TRL v0.15.2](https://github.com/huggingface/trl/blob/fc2b041b58f6fbe766dceaec819bc5a8f9d209da/trl/scripts/sft.py)，按 [Apache-2.0](LICENSE) 保留源码和版权。只调整了源码注释中的命令路径和本地保存示例，训练逻辑保持上游实现。

这部分是新增微调参考源码。本地未找到早期项目对应的训练脚本、适配器或评测结果，不能将本目录当作历史训练完成证明。

## 文件

| 文件 | 作用 |
| --- | --- |
| [sft.py](sft.py) | 加载模型与公开数据集、构建 SFTTrainer、训练并保存产物 |
| [configs/lora.yaml](configs/lora.yaml) | DeepSeek 蒸馏模型的 LoRA 配置 |
| [configs/qlora.yaml](configs/qlora.yaml) | 4-bit NF4 基础模型 + LoRA 配置 |
| [requirements.txt](requirements.txt) | LoRA 训练依赖版本 |
| [requirements-qlora.txt](requirements-qlora.txt) | 在训练依赖上增加 bitsandbytes |
| [reference/model_config.py](reference/model_config.py) | 对应上游 ModelConfig 参数定义，供阅读 |
| [reference/sft_config.py](reference/sft_config.py) | 对应上游 SFTConfig 参数定义，供阅读 |

`reference/` 仅保存参数定义参考；运行时使用安装的 TRL 包，不直接导入这些参考文件。

## 模型与数据

基础模型：[DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)。数据集：[trl-lib/Capybara](https://huggingface.co/datasets/trl-lib/Capybara)。模型和数据来自公开资源，本仓库不复制它们。执行训练命令时会联网下载，请按它们各自的许可使用。

配置中的模型版本为 `main`，数据集也没有固定 revision；因此训练数据与权重并非完全可复现快照。正式实验时应记录实际模型/数据版本、随机种子、硬件、依赖、提示格式和划分。

默认 10 步、序列长度 512、batch size 1，是启动检查用的保守取值，不是调优结论，也不是最低显存承诺。默认不评估，不能由训练结束推断模型质量提升。

## LoRA 安装与运行

推荐使用具备兼容 NVIDIA GPU、驱动和 CUDA PyTorch 的环境。FP16 配置不能直接视为通用 CPU 训练配置。依据 [PyTorch 官方安装说明](https://pytorch.org/get-started/locally/) 安装适合机器的 PyTorch 2.6.0 CUDA 构建，再安装其余版本依赖。

Windows 中从仓库根目录执行：

```powershell
py -3.12 -m venv .venv-training
# 在这个环境中先按官方说明安装合适的 CUDA PyTorch 构建
.\.venv-training\Scripts\python.exe -m pip install -r finetuning\requirements.txt
.\.venv-training\Scripts\python.exe finetuning\sft.py --config finetuning\configs\lora.yaml
```

推理和训练使用不同环境，避免训练依赖覆盖普通推理环境。

## QLoRA 安装与运行

该版本的 bitsandbytes 路径优先使用支持的 Linux / WSL2 NVIDIA CUDA 环境，不能仅凭安装成功认定 GPU 后端可用。在仓库根目录中：

```bash
python3.12 -m venv .venv-training
# 在这个环境中先按官方说明安装合适的 CUDA PyTorch 构建
.venv-training/bin/python -m pip install -r finetuning/requirements-qlora.txt
.venv-training/bin/python finetuning/sft.py --config finetuning/configs/qlora.yaml
```

LoRA 更新低秩适配器；QLoRA 在此基础上以 4-bit 量化加载冻结的基础模型。两者都会保存适配器相关产物，不等于重新训练并保存完整基础模型。

## 保存与后续部署

输出分别位于 `outputs/lora_smoke` 和 `outputs/qlora_smoke`。配置关闭 `push_to_hub`，并设置 `report_to: none`，不主动上传训练产物或外部日志。

适配器首先应与同一基础模型通过 Transformers / PEFT 加载并验证。Ollama 支持的适配器与导入格式还取决于基础模型架构和服务端版本，不能把任意训练目录直接当作 Ollama 模型使用。转换、合并、量化和导入需单独验证；本次没有执行这些步骤。

本目录提供可继续验证的训练源码与配置，尚无真实训练曲线、checkpoint 或效果对比。

从数据检查、参数选择到适配器验证和同条件评估，见 [实验流程](../docs/experiment-workflow.md)；已完成检查与待验证阶段见 [验证记录](../docs/verification.md)。
