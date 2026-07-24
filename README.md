# Dolphin serving — deploy bundle

One vLLM image (OpenAI-compatible), env-driven, serves either model. Infra only
runs `deploy_commands.sh`; the ML team owns everything up to the pushed image.

## Files
| File | Owner | Purpose |
|---|---|---|
| `export_from_mlflow.py` | ML | MLflow registry → raw HF weights dir |
| `Dockerfile` + `entrypoint.sh` | ML | vLLM + baked weights + offline env |
| `build_and_push.sh` | ML | build, tag w/ MLflow version, push to Artifact Registry |
| `deploy_commands.sh` | **Infra** | the actual `gcloud run deploy` blocks |
| `gce_startup.sh` | **Infra** | GCE GPU-VM alternative (A100/H100) |
| `smoke_test.sh` | Infra | verify the endpoint is alive |

## Workflow
1. `python export_from_mlflow.py --model-uri models:/dolphin-8b/3 --out models/dolphin`
2. `MODEL_TAG=8b-v3 ./build_and_push.sh`  (on an egress-capable build host)
3. Hand infra the image URI + the matching block in `deploy_commands.sh`.

## Sizing — one GPU per Cloud Run instance, no tensor parallel on Cloud Run
| Model | fp16 | Fits L4 (24 GB)? | Path |
|---|---|---|---|
| Dolphin 8B | ~16 GB | yes | **A** — Cloud Run L4 |
| Dolphin 24B | ~48 GB | no | **B** — Cloud Run RTX PRO 6000 (96 GB), or **C** — AWQ→L4 |
| (Hermes 70B later) | ~140 GB | no | GCE 2x GPU, `TP_SIZE=2` |

L4 needs ≥4 CPU / 16 GiB; RTX PRO 6000 needs ≥20 CPU / 80 GiB.

## Gotcha 1 — CUDA driver vs image (only affects the L4 paths, A and C)
The image is CUDA 12.9. Cloud Run's **L4 runs driver 535.x (CUDA 12.2)**; the
**RTX PRO 6000 runs 580.x (CUDA 13.0)**.
- RTX PRO 6000 (Path B): newer driver runs the 12.9 image fine, and the cu129
  build carries the Blackwell kernels that card needs. Clean.
- L4 (Paths A/C): a 12.9 userspace on a 12.2 driver relies on CUDA 12.x
  minor-version forward-compatibility. It *usually* works, but **validate that a
  test revision actually boots** before handing off. If it errors on a
  CUDA driver/runtime mismatch, either add NVIDIA's forward-compat packages to
  `LD_LIBRARY_PATH` (Cloud Run documents this) or pin an older vLLM tag built
  against CUDA ≤12.4.

## Gotcha 2 — startup probe
vLLM opens its port only after weights load into VRAM (30–90s). Cloud Run's
default health check can fail the revision on deploy. Raise the startup probe
(see the note at the bottom of `deploy_commands.sh`). Most common failure mode.

## Weights: bake vs mount
- **8B:** bake into the image (simple, self-contained). ~24 GB image.
- **24B fp16:** ~48 GB baked can hit Artifact Registry layer limits. Prefer
  mounting weights from an in-VPC GCS volume (image stays ~8 GB), or if baking,
  split the `.safetensors` across multiple `COPY` layers. AWQ (Path C) is small
  enough to bake safely.

## Runtime egress: none
The container never calls out (`HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`,
usage-stats off). State this to infra so they don't provision egress.
