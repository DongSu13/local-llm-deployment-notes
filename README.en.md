# Local LLM Deployment & Fine-Tuning

[中文](README.md) | [English](README.en.md)

A source collection for local DeepSeek deployment, Python inference, and parameter-efficient fine-tuning: an Ollama configuration, 16 inference examples, and Hugging Face TRL / PEFT workflows for SFT, LoRA, and QLoRA.

## Background and sources

This repository starts with a historical local Ollama configuration and organizes model creation, API usage, training configuration, and output validation. [Modelfile](Modelfile) retains the historical inference settings. Additional inference and training sources come from pinned upstream releases with attribution and licenses.

The documentation follows the features, requirements, quickstart, data, and evaluation structure used by [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), [QLoRA](https://github.com/artidoro/qlora), and [PEFT](https://github.com/huggingface/peft), alongside the source and validation conventions of existing local projects.

## Features and methods

| Workflow | Model / method | Entry point | Output |
| --- | --- | --- | --- |
| Local model creation | Ollama `deepseek-r1:1.5b` with inference settings | [Modelfile](Modelfile) | Local `deepseek-local-demo` tag |
| Text inference | Chat, streaming, history, async requests | [Python examples](examples/ollama/README.md) | Terminal responses |
| Specialized APIs | Structured output, tools, embeddings, model management | [Model and capability mapping](examples/ollama/README.md) | JSON, tool results, vectors, model information |
| LoRA SFT | DeepSeek-R1-Distill-Qwen-1.5B, unquantized base | [lora.yaml](finetuning/configs/lora.yaml) | Local adapter directory |
| QLoRA SFT | Same base, 4-bit NF4 with nested quantization | [qlora.yaml](finetuning/configs/qlora.yaml) | Local adapter directory |

Tool and structured-output examples retain upstream Llama defaults. See the example guide for exact tags and downloads. Ollama inference files and Transformers training checkpoints use different formats.

## Source layout

```text
.
├── Modelfile                 # Historical inference settings
├── requirements.txt          # Ollama Python SDK
├── examples/ollama/          # 16 API examples and MIT license
├── finetuning/
│   ├── sft.py               # TRL SFT entry point
│   ├── configs/             # LoRA / QLoRA configurations
│   ├── reference/           # Upstream parameter definitions for reading
│   └── requirements*.txt    # Training dependencies
├── docs/                    # Deployment, clients, experiments, validation
├── THIRD_PARTY_NOTICES.md    # Sources, versions, licenses
└── SOURCE_MANIFEST.json      # Upstream file hashes and modifications
```

## Requirements

| Use | Software and hardware |
| --- | --- |
| Ollama inference | Python 3.12, running Ollama service, chosen model; CPU / GPU needs depend on model and context |
| LoRA training | Separate Python 3.12 environment, compatible NVIDIA GPU and CUDA PyTorch; FP16 defaults |
| QLoRA training | Training requirements plus bitsandbytes; supported Linux / WSL2 CUDA environment recommended |

Inference pins `ollama==0.6.3`. Training pins PyTorch 2.6.0, Transformers 4.49.0, TRL 0.15.2, and PEFT 0.14.0. See the [training guide](finetuning/README.md) for dependencies and GPU installation prerequisites. Memory requirements need measurement on the target machine.

## Quickstart: local inference

Install and start [Ollama](https://ollama.com/), then run from the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull deepseek-r1:1.5b
ollama create deepseek-local-demo -f .\Modelfile
.\.venv\Scripts\python.exe .\examples\ollama\chat.py
.\.venv\Scripts\python.exe .\examples\ollama\chat-stream.py
```

The SDK does not install the service or model weights. Continue with [deployment and troubleshooting](docs/local-deployment.md) or [client integration](docs/client-integration.md).

## Quickstart: local fine-tuning

Training uses the Transformers checkpoint [DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) and public [trl-lib/Capybara](https://huggingface.co/datasets/trl-lib/Capybara) dataset. Running training downloads these resources.

For LoRA, create the environment below, install a compatible CUDA PyTorch build in it following the [official instructions](https://pytorch.org/get-started/locally/), then install dependencies and train:

```powershell
py -3.12 -m venv .venv-training
# Install compatible CUDA PyTorch in .venv-training first
.\.venv-training\Scripts\python.exe -m pip install -r finetuning\requirements.txt
.\.venv-training\Scripts\python.exe finetuning\sft.py --config finetuning\configs\lora.yaml
```

For QLoRA, use a compatible Linux / WSL2 CUDA environment:

```bash
python3.12 -m venv .venv-training
# Install compatible CUDA PyTorch in .venv-training first
.venv-training/bin/python -m pip install -r finetuning/requirements-qlora.txt
.venv-training/bin/python finetuning/sft.py --config finetuning/configs/qlora.yaml
```

Both configurations are **10-step startup checks** with sequence length 512, batch size 1, gradient accumulation 4, and LoRA rank 8. Evaluation, Hub uploads, and external reporting are disabled. Outputs go to `outputs/lora_smoke` or `outputs/qlora_smoke`. See the [training guide](finetuning/README.md) and [experiment workflow](docs/experiment-workflow.md) for data preparation, parameters, and validation.

## Validation and results

All 16 inference examples passed offline execution with synthetic HTTP responses. Both training configurations passed field and mocked training-flow checks. Methods are documented in the [verification record](docs/verification.md).

Live model inference, GPU training, adapter import, and quality evaluation have not been performed. No historical training scripts, adapters, or evaluation records were found locally; the added training references do not establish past training results. Model and dataset revisions are not a fully pinned experiment snapshot.

## Sources and licensing

- Ollama Python examples: v0.6.3, [MIT](examples/ollama/LICENSE).
- TRL SFT entry point and parameter definitions: v0.15.2, [Apache-2.0](finetuning/LICENSE).
- Local configuration and newly written documentation are identified separately from upstream code. See [notices](THIRD_PARTY_NOTICES.md) and the [file manifest](SOURCE_MANIFEST.json) for modifications.

Only source, configuration, and technical documentation are included. Personal files, credentials, real server information, chat histories, datasets, and model weights are excluded.
