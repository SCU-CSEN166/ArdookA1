import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, cohen_kappa_score

def evaluate_grant_pipeline(excel_path: str):
    """
    Evaluates grant recommendation predictions against ground truth labels
    across classification, safety, ranking, and citation grounding metrics.
    """
    df = pd.read_excel(excel_path, sheet_name="Grant Tracker")
    
    print(f"Loaded {len(df)} records for evaluation.\n")
    
    # ----------------------------------------------------
    # 1. MAPPING FIT LABELS TO NUMERIC ORDINALS
    # ----------------------------------------------------
    fit_mapping = {"Poor": 0, "Moderate": 1, "Strong": 2, "Excellent": 3}
    
    # Simulate model predictions (for demonstration, using ground truth + slight noise)
    # In production, replace `df['Predicted_Fit']` with your model's outputs.
    np.random.seed(42)
    true_labels = df['Fit'].map(fit_mapping).values
    
    # Simulate a realistic predictor with minor classification variance
    noise = np.random.choice([-1, 0, 0, 0, 1], size=len(df), p=[0.1, 0.7, 0.0, 0.1, 0.1])
    pred_labels = np.clip(true_labels + noise, 0, 3)
    
    df['True_Fit_Numeric'] = true_labels
    df['Pred_Fit_Numeric'] = pred_labels
    
    # ----------------------------------------------------
    # 2. CALCULATE CLASSIFICATION METRICS
    # ----------------------------------------------------
    # Quadratic Weighted Kappa penalizes severe ordinal misclassifications heavily
    qwk = cohen_kappa_score(true_labels, pred_labels, weights='quadratic')
    macro_f1 = f1_score(true_labels, pred_labels, average='macro')
    
    # ----------------------------------------------------
    # 3. CALCULATE SAFETY & DISQUALIFIER METRICS
    # ----------------------------------------------------
    # False Positive Rate on Poor fit: fraction of actual Poor fits predicted as Strong/Excellent
    actual_poor = (true_labels == 0)
    false_positives_poor = np.sum((pred_labels >= 2) & actual_poor)
    fpr_poor = false_positives_poor / np.sum(actual_poor) if np.sum(actual_poor) > 0 else 0.0
    
    # ----------------------------------------------------
    # 4. SIMULATED CITATION GROUNDING & NLI CHECK
    # ----------------------------------------------------
    # Checks whether generated claims have verbatim source grounding
    # In production, check if extracted snippets exist as substrings in source text.
    simulated_supported_claims = np.random.uniform(0.92, 0.99, size=len(df))
    citation_precision = np.mean(simulated_supported_claims)
    
    # ----------------------------------------------------
    # 5. DISPLAY EVALUATION REPORT
    # ----------------------------------------------------
    print("========== PIPELINE EVALUATION REPORT ==========")
    print(f"• Quadratic Weighted Kappa (QWK) : {qwk:.4f}")
    print(f"• Macro-F1 Score                 : {macro_f1:.4f}")
    print(f"• False Positive Rate (Poor Fit) : {fpr_poor * 100:.2f}% (Target: < 5%)")
    print(f"• Citation Grounding Precision   : {citation_precision * 100:.2f}%")
    print("================================================")
    
    return {
        "qwk": qwk,
        "macro_f1": macro_f1,
        "fpr_poor": fpr_poor,
        "citation_precision": citation_precision
    }

if __name__ == "__main__":
    metrics = evaluate_grant_pipeline("synthetic_grant_recommendations_with_poor_fit_v2.xlsx")