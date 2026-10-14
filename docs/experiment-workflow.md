# 从启动检查到可比较的微调实验

本指南说明如何继续验证现有 LoRA / QLoRA 配置。仓库当前没有真实训练结果；依赖安装与启动命令见 [微调指南](../finetuning/README.md)。

## 1. 确认数据与提示格式

默认入口通过 `load_dataset(dataset_name, name=dataset_config)` 读取公开 Hugging Face 数据集，当前选择 `trl-lib/Capybara` 的 `train` 划分。评估关闭时不读取测试划分。原始数据不存入仓库。

TRL 支持多种 SFT 数据格式；当前流程使用会话消息。下面是格式示意，并非本地个人聊天记录：

```json
{"messages": [{"role": "user", "content": "解释什么是梯度累积。"}, {"role": "assistant", "content": "多次小批量反向传播后再执行一次参数更新。"}]}
```

检查角色、空消息、重复样本、序列长度和基础模型的 chat template。长度 512 会限制训练输入；应检查截断后回答是否完整。正式数据应按任务和来源划分训练、验证、测试集，避免同一会话跨集合泄漏。

当前入口并未实现读取任意本地 JSON 文件的 CLI；仅把 `dataset_name` 改成文件路径不足以保证正确加载。若后续加入自己的数据，需要适配加载参数和字段，并先做格式检查。

## 2. 理解两份配置

| 参数 | LoRA | QLoRA | 含义 |
| --- | --- | --- | --- |
| 基础模型加载 | FP16，不量化 | 4-bit NF4，双重量化 | 改变基础模型加载方式 |
| `use_peft` | true | true | 训练适配器 |
| `lora_r` / `lora_alpha` | 8 / 16 | 8 / 16 | 适配器秩与缩放 |
| `lora_target_modules` | all-linear | all-linear | 由 PEFT 选择支持的线性层 |
| `learning_rate` | 0.0002 | 0.0002 | 启动配置，后续按验证集调整 |
| `max_seq_length` | 512 | 512 | 训练序列上限 |
| batch / 梯度累积 | 1 / 4 | 1 / 4 | 单进程名义有效 batch 为 4 |
| `max_steps` | 10 | 10 | 参数更新步数，优先于 epoch 设置 |
| `eval_strategy` | no | no | 启动阶段关闭质量评估 |

这组参数便于检查入口，不是最佳参数结论。QLoRA 配置使用 `adamw_torch`，并未启用论文中所有优化器与实验设定。

## 3. 检查本地训练产物

启动成功后检查 `outputs/lora_smoke` 或 `outputs/qlora_smoke`。PEFT 保存通常包含 `adapter_config.json` 与适配器权重，也可能有 tokenizer、训练参数和 checkpoint。实际文件以运行环境及 trainer 保存结果为准。

首先用 Transformers / PEFT 与相同基础模型加载适配器，检查模型、tokenizer、chat template 和固定测试提示。之后再验证合并、量化、转换及 Ollama 导入；训练目录不能直接视为通用 Ollama 模型文件。

## 4. 建立同条件比较

扩大训练步数前，先记录基础模型的输出。基础模型与适配器模型使用同一套独立测试提示、提示模板、采样设置、生成长度和评价规则；分别保存回答。按任务选择准确率、格式遵循、人工评分等指标，并注明样本数。

需要启用训练中评估时，先确认数据集实际存在对应划分，再配置 `dataset_test_split`、`eval_strategy` 和相关评估间隔。最终测试集应保留到模型选择之后。对于推理模型，通用会话 SFT 也可能改变原有推理行为，应同时检查目标任务和原有能力。

每次实验在本地记录：

- 模型、tokenizer 和数据的实际 revision / 指纹；当前入口未统一固定这些版本。
- 依赖、GPU / CUDA、随机种子、数据划分、模板和完整训练参数。
- 训练与验证损失、时间、峰值显存、checkpoint 与适配器位置。
- 测试集评价规则、基础模型与适配器模型结果及失败样例。

`outputs/`、`data/`、`adapters/` 和权重文件已被 `.gitignore` 排除。仓库里的结果描述应依据实际实验填写，避免用启动检查或上游论文数字代替自己的测量。
