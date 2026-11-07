import pandas as pd
import pickle
import re
import torch
import numpy as np
from transformers import DistilBertTokenizer, DistilBertModel

# LOAD MODEL
model = pickle.load(open("model.pkl", "rb"))

# LOAD CSV
df = pd.read_csv("flipkart_reviews_clean.csv")

# CLEAN TEXT
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# BERT SETUP
device = torch.device("cpu")

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
bert.eval()

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )

def get_embeddings(texts):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert(**inputs)
    return mean_pooling(outputs, inputs["attention_mask"]).numpy()

# PREPARE DATA
df = df[df["review_text"].notna()]
texts = df["review_text"].tolist()
cleaned = [clean_text(t) for t in texts]

# EMBEDDINGS
X = get_embeddings(cleaned)

# PREDICT
preds = model.predict(X)

df["prediction"] = preds

# RESULTS
total = len(df)
fake = int(np.sum(preds))
genuine = total - fake

print("\n===== MODEL OUTPUT ON REAL DATA =====")
print(f"Total reviews: {total}")
print(f"Fake reviews: {fake}")
print(f"Genuine reviews: {genuine}")
print(f"Fake %: {round((fake/total)*100, 2)}%")

print("\nSample predictions:")
print(df[["review_text", "prediction"]].head(10))

# SAVE
df.to_csv("predicted_reviews.csv", index=False)
print("\nSaved predictions to predicted_reviews.csv")