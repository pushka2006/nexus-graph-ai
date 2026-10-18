# NEXUS GRAPH AI - AI Model Setup & Strategy

## Model Architecture
- **Primary Fast Instruction Model (CPU / Edge)**: `Qwen/Qwen2.5-0.5B-Instruct` (Hugging Face) — Verified live locally
- **Full Instruction Model (GPU / Workstation)**: `Qwen/Qwen2.5-3B-Instruct` (Hugging Face)
- **Primary Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Supported Providers**:
  1. `huggingface`: Direct local PyTorch inference via `transformers` and `accelerate`. Uses `torch.inference_mode()` with prompt grounding.
  2. `vllm`: High-throughput local inference server using OpenAI-compatible API protocol.
  3. `openai`: Remote OpenAI-compatible API endpoint (e.g. self-hosted vLLM, LM Studio, Ollama, or OpenAI).
  4. `mock`: Deterministic domain-grounded mock adapter for headless CI environments without model downloads.

## Configuration (`.env`)
```bash
# Model Selection
LLM_PROVIDER=huggingface   # Options: 'huggingface', 'openai', 'vllm', 'mock'
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Hardware & Device Settings
HF_DEVICE=cpu              # 'cpu' or 'cuda'
DEVICE_MAP=auto            # 'auto', 'cuda:0', 'cpu'
TORCH_DTYPE=float32        # 'float16' for GPU, 'float32' for CPU

# Remote OpenAI/vLLM Settings (used if LLM_PROVIDER=openai or vllm)
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
```

## Running with Hugging Face Locally (Verified Setup)
1. Install PyTorch and transformers into the backend virtualenv:
   ```powershell
   backend\.venv\Scripts\pip install torch transformers sentence-transformers
   ```
2. On Windows CPU, `backend/app/llm/adapter.py` is configured with `low_cpu_mem_usage=False` to prevent memory mapping exceptions (`Errno 22`), and uses `torch.inference_mode()` with `eval()` for clean, fast inference.
3. The weights are automatically cached to `~/.cache/huggingface/hub/` on first run.

## Diagnostic Health Endpoint
Verify the running model and latency at any time:
```bash
curl http://localhost:8080/api/v1/health/llm
```
Response:
```json
{
  "status": "ready",
  "provider": "huggingface",
  "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
  "latency_ms": 24100.5,
  "test_response": "NEXUS GRAPH AI operational",
  "error": null
}
```
