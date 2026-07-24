#!/usr/bin/env bash
set -euo pipefail

# One image, both models. Everything is env-driven so infra never edits the image.
# Cloud Run injects $PORT (default 8080). GCE sets PORT=8000 in the run command.

exec python3 -m vllm.entrypoints.openai.api_server \
  --model "${MODEL_PATH:-/models/dolphin}" \
  --served-model-name "${SERVED_MODEL_NAME:-dolphin}" \
  --host 0.0.0.0 \
  --port "${PORT:-8080}" \
  --max-model-len "${MAX_MODEL_LEN:-16384}" \
  --gpu-memory-utilization "${GPU_MEM_UTIL:-0.92}" \
  --tensor-parallel-size "${TP_SIZE:-1}" \
  ${QUANTIZATION:+--quantization ${QUANTIZATION}} \
  ${EXTRA_ARGS:-}
