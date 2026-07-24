#!/usr/bin/env python3
"""Materialize raw HF weights from MLflow into a plain directory for vLLM.

vLLM wants a directory of HF files (config.json, tokenizer.*, *.safetensors) —
NOT an mlflow pyfunc/transformers wrapper. This downloads the registered model
artifact and locates that directory.

Usage:
  python export_from_mlflow.py --model-uri models:/dolphin-8b/3 --out models/dolphin
  python export_from_mlflow.py --model-uri runs:/<run_id>/model --out models/dolphin

Keep the version you exported (e.g. dolphin-8b/3) — use it as the image tag so the
deployed container traces back to a registered model version (governance lineage).
"""
import argparse
import os
import shutil
import sys
from mlflow.artifacts import download_artifacts


def find_hf_root(path: str) -> str:
    """Return the dir containing config.json (mlflow.transformers nests it,
    often under .../model or .../components/model)."""
    for root, _dirs, files in os.walk(path):
        if "config.json" in files and any(f.endswith(".safetensors") or f == "pytorch_model.bin" for f in files):
            return root
    # Fallback: config.json alone (weights may be sharded index only)
    for root, _dirs, files in os.walk(path):
        if "config.json" in files:
            return root
    raise SystemExit(f"Could not find an HF model dir (config.json) under {path}. "
                     "If MLflow only stored a pointer to GCS, fetch the weights from there instead.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-uri", required=True,
                    help="models:/<name>/<version> or runs:/<run_id>/<artifact_path>")
    ap.add_argument("--out", default="models/dolphin")
    args = ap.parse_args()

    print(f"Downloading artifacts for {args.model_uri} ...", file=sys.stderr)
    local = download_artifacts(artifact_uri=args.model_uri)
    hf_root = find_hf_root(local)
    print(f"HF weights found at: {hf_root}", file=sys.stderr)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    if os.path.abspath(hf_root) != os.path.abspath(args.out):
        if os.path.exists(args.out):
            shutil.rmtree(args.out)
        shutil.copytree(hf_root, args.out)
    print(f"Exported to: {args.out}", file=sys.stderr)

    # Sanity list — confirm tokenizer + weights are present before you build.
    for f in sorted(os.listdir(args.out)):
        print("  ", f, file=sys.stderr)


if __name__ == "__main__":
    main()
