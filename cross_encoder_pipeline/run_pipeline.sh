#!/bin/bash
set -e

echo "=== Starting Grant Pipeline with Ardook Target ==="
export CUDA_VISIBLE_DEVICES="0"

# Clean old run
rm -rf grant_cross_encoder_finetuned

echo "--- Step 1: Running Fine-Tuning ---"
python fine_tune_cross_encoder.py

echo "--- Step 2: Running Evaluation Pipeline ---"
python evaluate_grant_pipeline.py

echo "=== Pipeline Finished Successfully ==="
