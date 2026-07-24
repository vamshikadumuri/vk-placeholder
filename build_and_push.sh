#!/usr/bin/env bash
set -euo pipefail

# Run this on a build host that HAS egress (or an internal PyPI/registry mirror).
# The resulting image is fully self-contained; the runtime env is air-gapped.

# ---- edit these -------------------------------------------------------------
REGION="${REGION:-asia-south1}"
PROJECT="${PROJECT:-your-project}"
REPO="${REPO:-redteam}"                 # Artifact Registry repo
MODEL_TAG="${MODEL_TAG:-8b-v3}"         # <-- carry the MLflow version, e.g. 8b-v3 / 24b-v2
IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}/dolphin:${MODEL_TAG}"
# -----------------------------------------------------------------------------

# 1. Get weights out of MLflow first (produces ./models/dolphin):
#    python export_from_mlflow.py --model-uri models:/dolphin-8b/3 --out models/dolphin

# 2. Build. MODEL_SRC must be a path under the build context.
docker build -t "${IMAGE}" --build-arg MODEL_SRC=models/dolphin .

# 3. Push to Artifact Registry.
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
docker push "${IMAGE}"

echo "Pushed: ${IMAGE}"
echo "Hand this URI to infra along with deploy_commands.sh"
