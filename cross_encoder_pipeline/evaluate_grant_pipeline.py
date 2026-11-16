import os
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    cohen_kappa_score
)
from sklearn.preprocessing import label_binarize
from sentence_transformers import CrossEncoder

def safe_get_column(df, possible_names, default=""):
    """Searches a dataframe for any of the possible column names case-insensitively."""
    for name in possible_names:
        if name in df.columns:
            return df[name].astype(str)
        for col in df.columns:
            if col.strip().lower() == name.strip().lower():
                return df[col].astype(str)
    return pd.Series([default] * len(df))

def evaluate_pipeline():
    print("--- Starting Multi-Metric Grant Pipeline Evaluation ---")
    
    # 1. Locate test dataset
    test_file = None
    for candidate in ["Ardook_hidden_test_grants.xlsx", "ardook_hidden_test_labels.xlsx", "synthetic_grant_recommendations_balanced_120.xlsx"]:
        if os.path.exists(candidate):
            test_file = candidate
            break
            
    if not test_file:
        raise FileNotFoundError("Could not find any test dataset file.")
    
    print(f"Loading dataset from: {test_file}")
    df = pd.read_excel(test_file)

    # 2. Extract columns dynamically
    prog_col = safe_get_column(df, ['Program', 'Grant Name', 'Title'], default="Unknown Program")
    reqs_col = safe_get_column(df, ['Core Requirements', 'Requirements', 'Description'], default="")
    disq_col = safe_get_column(df, ['Key Concern / Disqualifier', 'Disqualifier', 'Concerns'], default="")
    
    has_ground_truth = any(col.strip().lower() in ['fit', 'label', 'score'] for col in df.columns)
    fit_col = safe_get_column(df, ['Fit', 'Label', 'Score'], default="Moderate")

    fit_mapping = {"Poor": 0, "Moderate": 1, "Strong": 2, "Excellent": 3}
    inv_fit_mapping = {0: "Poor", 1: "Moderate", 2: "Strong", 3: "Excellent"}
    true_labels = fit_col.map(lambda x: fit_mapping.get(str(x).strip(), 1)).values

    # 3. Load model using absolute path
    model_path = os.path.abspath("./grant_cross_encoder_finetuned")
    if not os.path.exists(model_path) or not os.path.exists(os.path.join(model_path, "config.json")):
        raise FileNotFoundError(f"Model directory or config.json not found at {model_path}. Complete fine-tuning first.")
        
    print(f"Loading CrossEncoder model from: {model_path}")
    model = CrossEncoder(model_path, local_files_only=True)
    
    # 4. Generate predictions
    org_profile = "We are an early-stage, women-led technology startup and social impact venture focused on digital accessibility, caregiver support, and inclusive software tools."
    
    pairs = []
    for i in range(len(df)):
        grant_text = f"Program: {prog_col.iloc[i]} | Requirements: {reqs_col.iloc[i]} | Disqualifier: {disq_col.iloc[i]}"
        pairs.append([org_profile, grant_text])
    
    print(f"Evaluating {len(pairs)} grant pairs...")
    preds = model.predict(pairs)
    pred_labels = np.digitize(preds, bins=[0.2, 0.5, 0.8])

    # Attach predictions to dataframe and save detailed Excel file
    df['Predicted_Score'] = preds
    df['Predicted_Fit'] = [inv_fit_mapping[val] for val in pred_labels]
    df['Utility'] = ['Useful' if val >= 2 else 'Not Useful' for val in pred_labels]

    predictions_output_file = "grant_predictions_detailed.xlsx"
    df.to_excel(predictions_output_file, index=False)
    print(f"\n✅ Detailed predictions saved to: {predictions_output_file}")

    # Utility breakdown summary
    useful_count = int((pred_labels >= 2).sum())
    not_useful_count = int((pred_labels < 2).sum())
    print(f"   • Likely Useful Grants     : {useful_count}")
    print(f"   • Likely Not Useful Grants : {not_useful_count}")

    # 5. Compute and save metrics if ground-truth labels exist
    metrics_rows = [
        {"Category": "Summary Counts", "Metric": "Total Grants Evaluated", "Value": len(df)},
        {"Category": "Summary Counts", "Metric": "Likely Useful (Strong/Excellent)", "Value": useful_count},
        {"Category": "Summary Counts", "Metric": "Likely Not Useful (Poor/Moderate)", "Value": not_useful_count},
    ]

    if has_ground_truth:
        acc = accuracy_score(true_labels, pred_labels)
        balanced_acc = balanced_accuracy_score(true_labels, pred_labels)
        precision_macro = precision_score(true_labels, pred_labels, average='macro', zero_division=0)
        recall_macro = recall_score(true_labels, pred_labels, average='macro', zero_division=0)
        macro_f1 = f1_score(true_labels, pred_labels, average='macro', zero_division=0)
        qwk = cohen_kappa_score(true_labels, pred_labels, weights='quadratic')
        
        try:
            sigmoid_preds = 1 / (1 + np.exp(-preds))
            y_bin = label_binarize(true_labels, classes=[0, 1, 2, 3])
            y_score = np.vstack([1 - sigmoid_preds, sigmoid_preds * 0.33, sigmoid_preds * 0.66, sigmoid_preds]).T
            roc_auc_multi = roc_auc_score(y_bin, y_score, multi_class='ovr', average='macro')
        except Exception:
            roc_auc_multi = 0.0

        # Binary classification metrics (Viable >= 2 vs Non-Viable < 2)
        bin_true = (true_labels >= 2).astype(int)
        bin_pred = (pred_labels >= 2).astype(int)

        bin_acc = accuracy_score(bin_true, bin_pred)
        bin_balanced_acc = balanced_accuracy_score(bin_true, bin_pred)
        bin_prec = precision_score(bin_true, bin_pred, zero_division=0)
        bin_rec = recall_score(bin_true, bin_pred, zero_division=0)
        bin_f1 = f1_score(bin_true, bin_pred, zero_division=0)
        
        try:
            bin_roc_auc = roc_auc_score(bin_true, sigmoid_preds)
        except Exception:
            bin_roc_auc = 0.0

        actual_poor = (true_labels == 0)
        false_positives_poor = np.sum((pred_labels >= 2) & actual_poor)
        fpr_poor = false_positives_poor / np.sum(actual_poor) if np.sum(actual_poor) > 0 else 0.0

        metrics_rows.extend([
            {"Category": "Ordinal / Multi-Class", "Metric": "Accuracy", "Value": round(acc, 4)},
            {"Category": "Ordinal / Multi-Class", "Metric": "Balanced Accuracy", "Value": round(balanced_acc, 4)},
            {"Category": "Ordinal / Multi-Class", "Metric": "Macro Precision", "Value": round(precision_macro, 4)},
            {"Category": "Ordinal / Multi-Class", "Metric": "Macro Recall", "Value": round(recall_macro, 4)},
            {"Category": "Ordinal / Multi-Class", "Metric": "Macro-F1 Score", "Value": round(macro_f1, 4)},
            {"Category": "Ordinal / Multi-Class", "Metric": "Quadratic Weighted Kappa (QWK)", "Value": round(qwk, 4)},
            {"Category": "Ordinal / Multi-Class", "Metric": "Macro ROC-AUC (OvR)", "Value": round(roc_auc_multi, 4)},
            {"Category": "Binary Classification", "Metric": "Binary Accuracy", "Value": round(bin_acc, 4)},
            {"Category": "Binary Classification", "Metric": "Binary Balanced Accuracy", "Value": round(bin_balanced_acc, 4)},
            {"Category": "Binary Classification", "Metric": "Binary Precision", "Value": round(bin_prec, 4)},
            {"Category": "Binary Classification", "Metric": "Binary Recall", "Value": round(bin_rec, 4)},
            {"Category": "Binary Classification", "Metric": "Binary F1-Score", "Value": round(bin_f1, 4)},
            {"Category": "Binary Classification", "Metric": "Binary ROC-AUC", "Value": round(bin_roc_auc, 4)},
            {"Category": "Business Constraint", "Metric": "False Positive Rate (Poor Fit)", "Value": round(fpr_poor, 4)},
        ])
    else:
        print("⚠️ No ground-truth 'Fit' column found in test file; skipping ground-truth metric calculations.")

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_output_file = "evaluation_metrics_summary.csv"
    metrics_df.to_csv(metrics_output_file, index=False)
    print(f"✅ Evaluation metrics summary saved to: {metrics_output_file}")

if __name__ == "__main__":
    evaluate_pipeline()
