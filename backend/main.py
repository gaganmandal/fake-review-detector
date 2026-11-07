
# main.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import pickle
# import re
# import torch
# import numpy as np
# import pandas as pd

# from transformers import DistilBertTokenizer, DistilBertModel

# # ✅ NEW IMPORTS
# from scraper_playwright import get_reviews
# from cleaner import run as clean_data


# # =========================
# # APP INIT
# # =========================
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # DEVICE
# # =========================
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # =========================
# # LOAD BERT
# # =========================
# tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
# bert.to(device)
# bert.eval()

# for param in bert.parameters():
#     param.requires_grad = False

# # =========================
# # LOAD ML MODEL
# # =========================
# model = pickle.load(open("model.pkl", "rb"))

# # =========================
# # LOAD MODEL METRICS
# # =========================
# results_df = pd.read_csv("model_results.csv")

# model_results = {}
# for _, row in results_df.iterrows():
#     model_results[row["Model"]] = {
#         "accuracy": float(row["Accuracy"]),
#         "precision": float(row["Precision"]),
#         "recall": float(row["Recall"]),
#         "f1": float(row["F1 Score"]),
#     }

# # =========================
# # CLEAN TEXT (FOR MODEL)
# # =========================
# def clean_text(text):
#     text = str(text).lower()
#     text = re.sub(r"http\S+", "", text)
#     text = re.sub(r"[^a-zA-Z\s]", " ", text)
#     text = re.sub(r"\s+", " ", text).strip()
#     return text

# # =========================
# # MEAN POOLING
# # =========================
# def mean_pooling(model_output, attention_mask):
#     token_embeddings = model_output.last_hidden_state
#     input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
#     return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
#         input_mask_expanded.sum(1), min=1e-9
#     )

# # =========================
# # EMBEDDINGS
# # =========================
# def get_embeddings_batch(texts, batch_size=16):
#     all_embeddings = []

#     for i in range(0, len(texts), batch_size):
#         batch = texts[i:i + batch_size]

#         inputs = tokenizer(
#             batch,
#             return_tensors="pt",
#             truncation=True,
#             padding=True,
#             max_length=128
#         )

#         inputs = {k: v.to(device) for k, v in inputs.items()}

#         with torch.no_grad():
#             outputs = bert(**inputs)

#         embeddings = mean_pooling(outputs, inputs["attention_mask"]).cpu().numpy()
#         all_embeddings.append(embeddings)

#     return np.vstack(all_embeddings)

# # =========================
# # API ROUTES
# # =========================

# @app.get("/")
# def home():
#     return {"message": "Fake Review Detection API Running 🚀"}


# @app.get("/model-accuracy")
# def get_model_accuracy():
#     return pd.read_csv("model_results.csv").to_dict(orient="records")


# @app.post("/analyze")
# def analyze(data: dict):

#     url = data.get("url")

#     if not url:
#         return {"error": "URL is required"}

#     print("\n🚀 Starting Full Pipeline...")

#     # =========================
#     # STEP 1: SCRAPE
#     # =========================
#     print("📥 Scraping reviews...")
#     get_reviews(url)

#     # =========================
#     # STEP 2: CLEAN
#     # =========================
#     print("🧹 Cleaning reviews...")
#     clean_data("flipkart_blocks.csv", "flipkart_reviews_clean.csv")

#     # =========================
#     # STEP 3: LOAD CLEAN DATA
#     # =========================
#     df = pd.read_csv("flipkart_reviews_clean.csv")

#     if df.empty:
#         return {
#             "total": 0,
#             "fake": 0,
#             "genuine": 0,
#             "fake_percent": 0,
#             "models": model_results
#         }

#     reviews = df["review_text"].tolist()

#     print(f"📊 Total clean reviews: {len(reviews)}")

#     # =========================
#     # STEP 4: EMBEDDINGS
#     # =========================
#     cleaned = [clean_text(r) for r in reviews]
#     X = get_embeddings_batch(cleaned)

#     # =========================
#     # STEP 5: PREDICTION
#     # =========================
#     print("🤖 Running predictions...")
#     preds = model.predict(X)

#     fake = int(np.sum(preds))
#     genuine = len(preds) - fake

#     # =========================
#     # RESPONSE
#     # =========================
#     return {
#         "total": len(reviews),
#         "fake": fake,
#         "genuine": genuine,
#         "fake_percent": round((fake / len(reviews)) * 100, 2),

#         "models": model_results,

#         "sample": [
#             {"review": r, "label": int(p)}
#             for r, p in zip(reviews[:10], preds[:10])
#         ],

#         # 🔥 ADVANCED INSIGHTS (VERY IMPORTANT FOR UI)
#         "insights": {
#             "avg_rating": round(df["rating"].mean(), 2) if "rating" in df else None,
#             "verified_percent": round(df["verified"].mean() * 100, 2) if "verified" in df else None,
#             "total_reviews_used": len(reviews)
#         }
#     }

# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import torch
import numpy as np
import pandas as pd

# ✅ NEW MODEL IMPORT
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# ✅ EXISTING IMPORTS
from scraper_playwright import get_reviews
from cleaner import run as clean_data


# =========================
# APP INIT
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DEVICE
# =========================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# LOAD TRAINED MODEL
# =========================
MODEL_PATH = "fake_review_model"

tokenizer = RobertaTokenizer.from_pretrained(MODEL_PATH)
model = RobertaForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(device)
model.eval()


# =========================
# LOAD MODEL METRICS
# =========================
results_df = pd.read_csv("model_results.csv")

model_results = {}
for _, row in results_df.iterrows():
    model_results[row["Model"]] = {
        "accuracy": float(row["Accuracy"]),
        "precision": float(row["Precision"]),
        "recall": float(row["Recall"]),
        "f1": float(row["F1 Score"]),
    }


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# API ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "Fake Review Detection API Running 🚀"}


@app.get("/model-accuracy")
def get_model_accuracy():
    return pd.read_csv("model_results.csv").to_dict(orient="records")
    


@app.post("/analyze")
def analyze(data: dict):

    url = data.get("url")

    if not url:
        return {"error": "URL is required"}

    print("\n🚀 Starting Full Pipeline...")

    # =========================
    # STEP 1: SCRAPE
    # =========================
    print("📥 Scraping reviews...")
    get_reviews(url)

    # =========================
    # STEP 2: CLEAN
    # =========================
    print("🧹 Cleaning reviews...")
    clean_data("flipkart_blocks.csv", "flipkart_reviews_clean.csv")

    # =========================
    # STEP 3: LOAD CLEAN DATA
    # =========================
    df = pd.read_csv("flipkart_reviews_clean.csv")

    if df.empty:
        return {
            "total": 0,
            "fake": 0,
            "genuine": 0,
            "fake_percent": 0,
            "models": model_results
        }

    reviews = df["review_text"].tolist()

    print(f"📊 Total clean reviews: {len(reviews)}")

    # =========================
    # STEP 4: PREP INPUT
    # =========================
    cleaned = [clean_text(r) for r in reviews]

    if "rating" in df.columns:
        inputs_text = [
            f"Rating: {rating} Review: {text}"
            for text, rating in zip(cleaned, df["rating"].tolist())
        ]
    else:
        inputs_text = cleaned

    inputs = tokenizer(
        inputs_text,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    # =========================
    # STEP 5: PREDICTION
    # =========================
    print("🤖 Running predictions...")

    with torch.no_grad():
        outputs = model(**inputs)

    preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()

    fake = int(np.sum(preds))
    genuine = len(preds) - fake

    # =========================
    # RESPONSE (ONLY CHANGE HERE)
    # =========================
    return {
        "total": len(reviews),
        "fake": fake,
        "genuine": genuine,
        "fake_percent": round((fake / len(reviews)) * 100, 2),

        "models": model_results,

        # ✅ FULL REVIEWS ADDED (UPGRADE)
        "reviews": [
            {
                "review": r,
                "label": int(p),
                "rating": float(df["rating"].iloc[i]) if "rating" in df else None,
                "verified": bool(df["verified"].iloc[i]) if "verified" in df else None,
            }
            for i, (r, p) in enumerate(zip(reviews, preds))
        ],

        "insights": {
            "avg_rating": round(df["rating"].mean(), 2) if "rating" in df else None,
            "verified_percent": round(df["verified"].mean() * 100, 2) if "verified" in df else None,
            "total_reviews_used": len(reviews)
        }
    }