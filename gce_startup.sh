#!/usr/bin/env bash
set -euo pipefail

# GCE GPU-instance path. Use when you don't want Cloud Run's single-GPU ceiling —
# e.g. 24B fp16 on 1x A100 80 GB (a2-ultragpu-1g), or later 70B on 2x GPUs (TP=2).
# Attach this as the VM's startup-script. Use a GPU image that already has the
# NVIDIA driver + container toolkit (GCE "Deep Learning" GPU image or COS-GPU).
# The VM's service account needs roles/artifactregistry.reader.

IMAGE="asia-south1-docker.pkg.dev/your-project/redteam/dolphin:24b-v2"

gcloud auth configure-docker asia-south1-docker.pkg.dev --quiet
docker pull "${IMAGE}"

docker run -d --name dolphin --restart=always \
  --gpus all --ipc=host \
  -p 8000:8000 \
  -e PORT=8000 \
  -e SERVED_MODEL_NAME=dolphin-24b \
  -e MAX_MODEL_LEN=16384 \
  -e GPU_MEM_UTIL=0.90 \
  -e TP_SIZE=1 \
  "${IMAGE}"

# For 2-GPU tensor parallel (e.g. 70B or 2x L4 for 24B), set TP_SIZE=2 and
# ensure --ipc=host (already set) so PyTorch shared memory works.
