#train_model
# ==============================
# IMPORTS
# ==============================
import pandas as pd
import pickle
import re
import torch
import numpy as np
from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data.csv")

# ==============================
# CLEAN TEXT (UPDATED)
# ==============================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["text_"] = df["text_"].apply(clean_text)

texts = df["text_"].tolist()

# ==============================
# LABEL FIX (IMPORTANT)
# ==============================
# CG = fake (1), OR = genuine (0)
labels = df["label"].map({"CG": 1, "OR": 0}).values

# ==============================
# LOAD BERT
# ==============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert = DistilBertModel.from_pretrained("distilbert-base-uncased")

bert.to(device)
bert.eval()

# ==============================
# MEAN POOLING
# ==============================
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# ==============================
# EMBEDDINGS
# ==============================
def get_embeddings_batch(texts, batch_size=32):
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]

        inputs = tokenizer(
            batch,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )

        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = bert(**inputs)

        embeddings = mean_pooling(outputs, inputs["attention_mask"]).cpu().numpy()
        all_embeddings.append(embeddings)

    return np.vstack(all_embeddings)

X = get_embeddings_batch(texts)
y = np.array(labels)

# ==============================
# TRAIN
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

# ==============================
# SAVE
# ==============================
pickle.dump(model, open("model.pkl", "wb"))
print("Model saved ✅")