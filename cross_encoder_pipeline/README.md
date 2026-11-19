This repository contains an end-to-end machine learning pipeline that fine-tunes a cross-encoder (ms-marco-MiniLM-L-6-v2) to score and classify grant opportunities based on organizational fit, then evaluates performance and exports detailed predictions.

# 1. Prerequisites/setup #
Before running the pipeline, make sure your computer/test environment has Python 3.9+ installed.

Download the following files and put them in the same project folder:
1. fine_tune_cross_encoder.py (Model training script)
2. evaluate_grant_pipeline.py (Evaluation and prediction export script) 
3. run_pipeline.sh (Automated master script for Mac/Linux/HPC)
4. Your training dataset (cross_encoder_training_ready.xlsx or synthetic_grant_recommendations_balanced_120.xlsx) 
5. Your target test dataset (Ardook_hidden_test_grants.xlsx)

   
# 2. Installing Required Libraries #
Using WAVE OpenOnDemand should be sufficient for running this pipeline. I personally requested 32 GB and no GPUs were needed. 

Open a Jupyter notebook and a terminal in your browser, navigate to your project folder, and install the following Python packages. 

```
cd /path/to/your/project_folder

# Optional but recommended: create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install torch pandas numpy scikit-learn sentence-transformers openpyxl

```

# 3. Running Pipeline #

**Option A: Automatic Run**

Uses Bash script to do important steps automatically, such as training the model.

```
Bash

chmod +x run_pipeline.sh
./run_pipeline.sh
```

**Option B: Manual Run**

Run the following steps separately:
1. Fine-tune model

```
Bash

python fine_tune_cross_encoder.py
```

2. Run evaluation
```
Bash

python evaluate_grant_pipeline.py

```
# 4. Expected Output #

Once the pipeline completes, two output files will be generated in your project folder:

Output File Descriptions:

grant_predictions_detailed.xlsx
Contains every grant from your test file along with its raw model score (Predicted_Score), fit tier (Poor, Moderate, Strong, Excellent), and binary recommendation (Useful vs. Not Useful).

evaluation_metrics_summary.csv
Contains counts of useful vs. non-useful grants. If the test dataset included ground-truth Fit labels, this file also lists full ordinal metrics (Accuracy, Balanced Accuracy, Macro-F1, QWK, ROC-AUC), binary metrics, and the False Positive Rate for poor fits.

# 5. Customization/Troubleshooting #

Changing grant preadsheet: Drop any .xlsx file into the folder and update the candidate filename list near the top of evaluate_grant_pipeline.py. The script automatically maps common column variations (such as Program, Grant Name, or Title, and Core Requirements or Requirements).

Changing the organizational profile: Open evaluate_grant_pipeline.py and edit the org_profile string variable to tailor recommendations to a different startup or organization.

No GPU available: If running on a standard laptop without an NVIDIA GPU, remove or comment out os.environ["CUDA_VISIBLE_DEVICES"] = "0" at the top of fine_tune_cross_encoder.py so PyTorch defaults cleanly to the CPU.

Excel read errors (Missing optional dependency 'openpyxl'): Run pip install openpyxl in the terminal and re-run the script.


