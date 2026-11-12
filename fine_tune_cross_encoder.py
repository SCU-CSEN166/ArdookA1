import pandas as pd
from torch.utils.data import DataLoader
from sentence_transformers import CrossEncoder, InputExample
from sklearn.model_selection import train_test_split

# Load prepared data
df = pd.read_excel("cross_encoder_training_ready.xlsx")

examples = [
    InputExample(texts=[row["Sentence_1"], row["Sentence_2"]], label=float(row["Label"]))
    for _, row in df.iterrows()
]

# Train/validation split
train_exs, val_exs = train_test_split(examples, test_size=0.2, random_state=42)
train_dataloader = DataLoader(train_exs, shuffle=True, batch_size=8)

# Initialize model
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', num_labels=1)

print("Starting Cross-Encoder fine-tuning...")
model.fit(
    train_dataloader=train_dataloader,
    eval_dataloader=DataLoader(val_exs, batch_size=8),
    epochs=3,
    warmup_steps=50,
    output_path="grant_cross_encoder_finetuned"
)
print("Fine-tuning complete! Model saved to grant_cross_encoder_finetuned")