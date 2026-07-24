# --- Base -------------------------------------------------------------------
# v0.25.0 built against CUDA 12.9. This tag is what carries Blackwell kernels,
# which the RTX PRO 6000 (24B path) needs. The L4 (8B path) driver is older
# (CUDA 12.2) — see the CUDA note in README before you hand this off.
ARG VLLM_TAG=v0.25.0-cu129-ubuntu2404
FROM vllm/vllm-openai:${VLLM_TAG}

# --- Weights ----------------------------------------------------------------
# Bake the HF weights produced by export_from_mlflow.py.
# For the 24B fp16 (~48 GB) you may prefer a mounted GCS volume instead of
# baking — see "Weights: bake vs mount" in README (Artifact Registry layer limits).
ARG MODEL_SRC=models/dolphin
COPY ${MODEL_SRC} /models/dolphin

# --- Air-gap discipline: never phone home -----------------------------------
ENV HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    VLLM_NO_USAGE_STATS=1 \
    DO_NOT_TRACK=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Cloud Run routes to $PORT (8080). GCE overrides to 8000 at run time.
ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
