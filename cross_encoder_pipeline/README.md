This repository contains an end-to-end machine learning pipeline that fine-tunes a cross-encoder (ms-marco-MiniLM-L-6-v2) to score and classify grant opportunities based on organizational fit, then evaluates performance and exports detailed predictions.

# 1. Prerequisites/setup #
Before running the pipeline, make sure your computer/test environment has Python 3.9+ installed.

Download the following files and put them in the same project folder:
1. fine_tune_cross_encoder.py (Model training script)
2. evaluate_grant_pipeline.py (Evaluation and prediction export script) 
3. run_pipeline.sh (Automated master script for Mac/Linux/HPC)
4. Your training dataset (cross_encoder_training_ready.xlsx or synthetic_grant_recommendations_balanced_120.xlsx) 
5. Your target test dataset (Ardook_hidden_test_grants.xlsx)

   
#2. Installing Required Libraries
Using WAVE OpenOnDemand should be sufficient for running this pipeline—I personally requested 32 GB and no GPUs were needed. 
