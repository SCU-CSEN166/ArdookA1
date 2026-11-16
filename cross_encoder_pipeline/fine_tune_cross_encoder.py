import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import pandas as pd
from torch.utils.data import DataLoader
from sentence_transformers import CrossEncoder, InputExample
from sklearn.model_selection import train_test_split

print("--- Starting Fine-Tuning Pipeline ---")

# 1. Ensure absolute output directory exists upfront
output_dir = os.path.abspath("grant_cross_encoder_finetuned")
os.makedirs(output_dir, exist_ok=True)
print(f"Target output directory created/verified at: {output_dir}")

# 2. Load data
training_file = "cross_encoder_training_ready.xlsx" if os.path.exists("cross_encoder_training_ready.xlsx") else "synthetic_grant_recommendations_balanced_120.xlsx"
df = pd.read_excel(training_file)

s1_col = 'Sentence_1' if 'Sentence_1' in df.columns else df.columns[0]
s2_col = 'Sentence_2' if 'Sentence_2' in df.columns else df.columns[1]
label_col = 'Label' if 'Label' in df.columns else df.columns[2]

examples = [
    InputExample(texts=[str(row[s1_col]), str(row[s2_col])], label=float(row[label_col]))
    for _, row in df.iterrows()
]

train_exs, val_exs = train_test_split(examples, test_size=0.2, random_state=42)
train_dataloader = DataLoader(train_exs, shuffle=True, batch_size=8)

# 3. Train model
print("Initializing model...")
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', num_labels=1)

print("Starting training epochs...")
model.fit(
    train_dataloader=train_dataloader,
    epochs=3,
    warmup_steps=10,
    output_path=output_dir
)

# 4. Manual Fallback: Ensure config and weights are explicitly saved if fit() missed them
if not os.path.exists(os.path.join(output_dir, "config.json")):
    print("⚠️ `model.fit()` did not write config.json. Executing manual save fallback...")
    model.model.save_pretrained(output_dir)
    model.tokenizer.save_pretrained(output_dir)

# 5. Final validation check
if os.path.exists(output_dir) and os.path.exists(os.path.join(output_dir, "config.json")):
    print(f"SUCCESS: Model successfully written and verified at {output_dir}")
    print("Files in directory:", os.listdir(output_dir))
else:
    raise RuntimeError(f"CRITICAL ERROR: Failed to write model files to {output_dir}!")
